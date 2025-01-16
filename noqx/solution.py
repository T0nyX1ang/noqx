"""Generate solutions for the given problem."""

from copy import deepcopy
from typing import List, Optional

from clingo import MessageCode
from clingo.control import Control
from clingo.solving import Model

from noqx.logging import logger
from noqx.puzzle import Color, Direction, Point, Puzzle


def clingo_logging_handler(code: MessageCode, message: str) -> None:  # pragma: no cover
    """Handle clingo logging."""
    if code == MessageCode.RuntimeError:
        logger.error(f"[Clingo] {code.name}: {message.strip()}")
    else:
        logger.warning(f"[Clingo] {code.name}: {message.strip()}")


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
        self.solutions: List[Puzzle] = []

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
        solution = deepcopy(self.puzzle)
        solution.clear()

        for item in solution_data:
            _type, _data = item.replace("(", " ").replace(")", " ").split()
            data = _data.split(",")

            r, c = tuple(map(int, data[:2]))  # ensure the first two elements of data is the row and column

            if _type.startswith("edge_"):
                for d in Direction:
                    if _type == f"edge_{d.value}":
                        solution.edge[Point(r, c, d)] = True

            elif _type.startswith("grid_"):
                grid_direction = str(data[2]).replace('"', "")
                if self.puzzle.puzzle_name == "hashi":
                    solution.line[Point(r, c, pos=f"{grid_direction}_{data[3]}")] = True
                else:
                    solution.line[Point(r, c, pos=grid_direction)] = True

            elif _type.startswith("number"):
                if self.puzzle.puzzle_name == "easyasabc":  # convert penpa number to letter
                    solution.text[Point(r, c, Direction.CENTER, "normal")] = self.puzzle.param["letters"][int(data[2]) - 1]
                else:
                    solution.text[Point(r, c, Direction.CENTER, "normal")] = int(data[2])

            elif _type.startswith("content"):
                solution.text[Point(r, c, Direction.CENTER, "normal")] = str(data[2]).replace('"', "")

            elif _type == "triangle":
                shaka_dict = {'"ul"': "1", '"ur"': "4", '"dl"': "2", '"dr"': "3"}
                solution.symbol[Point(r, c, Direction.CENTER)] = f"tri__{shaka_dict[data[2]]}"

            elif _type == "gray":
                solution.surface[Point(r, c)] = Color.GRAY
            elif _type == "black":
                solution.surface[Point(r, c)] = Color.BLACK

            elif len(data) == 2:
                solution.symbol[Point(r, c, Direction.CENTER)] = str(_type)

            else:  # pragma: no cover
                solution.text[Point(r, c, Direction.CENTER, "normal")] = int(data[2])  # for debugging

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
        self.clingo_instance.add(program=self.program)
        self.clingo_instance.ground()
        with self.clingo_instance.solve(on_model=self.store_model, async_=True) as handle:  # type: ignore
            handle.wait(Config.time_limit)
            handle.cancel()

        for model_str in self.model:
            self.store_solutions(model_str)


solver = ClingoSolver()
