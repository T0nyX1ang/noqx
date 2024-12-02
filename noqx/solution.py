"""Generate solutions for the given problem."""

from typing import List, Optional

from clingo import MessageCode
from clingo.control import Control
from clingo.solving import Model

from .logging import logger
from .penpa import Direction, Puzzle, Solution


def clingo_logging_handler(code: MessageCode, message: str) -> None:
    """Handle clingo logging."""
    logger.error(f"[Clingo] {code.name}: {message.strip()}")


class Config:
    """Configuration for the solver."""

    time_limit: int = 30
    max_solutions_to_find: int = 10
    parallel_threads: int = 1


class ClingoSolver:
    """A solver using clingo."""

    def __init__(self):
        """Initialize a solver."""
        self.clingo_instance: Control = Control(logger=clingo_logging_handler)
        self.program: str = ""
        self.model: List[str] = []
        self.puzzle: Optional[Puzzle] = None
        self.solutions: List[Solution] = []

    def register_puzzle(self, puzzle: Puzzle):
        """Register the puzzle to the solution."""
        self.puzzle = puzzle
        logger.debug("[Solver] Puzzle registered.")

    def store_model(self, model: Model):  # pragma: no cover
        """Store the model on solving."""
        self.model.append(str(model))

    def store_solutions(self, model_str: str):
        """Get the solution."""
        if self.puzzle is None:
            raise PermissionError("Puzzle not registered.")

        solution_data = tuple(str(model_str).split())  # raw solution converted from clingo
        solution = Solution(self.puzzle)

        for item in solution_data:
            _type, _data = item.replace("(", " ").replace(")", " ").split()
            data = _data.split(",")

            r, c = data[:2]  # ensure the first two elements of data is the row and column

            if _type.startswith("edge_"):
                for d in Direction:
                    if _type == f"edge_{d.value}":
                        solution.edge.add((int(r), int(c), d))

            elif _type.startswith("grid_"):
                grid_direction = str(data[2]).replace('"', "")
                if self.puzzle.puzzle_type == "hashi":
                    solution.line.add((int(r), int(c), f"{grid_direction}_{data[3]}"))
                else:
                    solution.line.add((int(r), int(c), grid_direction))

            elif _type.startswith("number"):
                if self.puzzle.puzzle_type == "easyasabc":  # convert penpa number to letter
                    solution.text[(int(r), int(c))] = self.puzzle.param["letters"][int(data[2]) - 1]
                else:
                    solution.text[(int(r), int(c))] = int(data[2])

            elif _type.startswith("content"):
                solution.text[(int(r), int(c))] = str(data[2]).replace('"', "")

            elif _type == "triangle":
                shaka_dict = {'"ul"': "1", '"ur"': "4", '"dl"': "2", '"dr"': "3"}
                solution.symbol[(int(r), int(c), Direction.CENTER)] = f"tri__{shaka_dict[data[2]]}"

            elif _type == "gray":
                solution.surface[(int(r), int(c))] = 8
            elif _type == "black":
                solution.surface[(int(r), int(c))] = 4

            elif len(data) == 2:
                solution.symbol[(int(r), int(c), Direction.CENTER)] = str(_type)

            else:  # pragma: no cover
                solution.text[(int(r), int(c))] = int(data[2])  # for debugging

        self.solutions.append(solution)

    def add_program_line(self, line: str):
        """Add a line to the program."""
        if line != "":
            self.program += line + "\n"

    def reset(self):
        """Reset the program."""
        self.clingo_instance = Control(logger=clingo_logging_handler)
        self.program = ""
        self.model = []
        self.puzzle = None
        self.solutions = []

    def solve(self):
        """Solve the problem."""
        self.clingo_instance.configuration.sat_prepro = 2
        self.clingo_instance.configuration.asp.trans_ext = "dynamic"  # type: ignore
        self.clingo_instance.configuration.asp.eq = 1  # type: ignore
        self.clingo_instance.configuration.solve.parallel_mode = Config.parallel_threads  # type: ignore
        self.clingo_instance.configuration.solve.models = Config.max_solutions_to_find  # type: ignore
        self.clingo_instance.add("base", [], self.program)
        self.clingo_instance.ground()
        with self.clingo_instance.solve(on_model=self.store_model, async_=True) as handle:  # type: ignore
            handle.wait(Config.time_limit)
            handle.cancel()

        for model_str in self.model:
            self.store_solutions(model_str)


solver = ClingoSolver()
