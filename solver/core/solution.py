"""Generate solutions for the given problem."""

from typing import List, Optional

from clingo.control import Control
from clingo.solving import Model

from .const import logger
from .penpa import Direction, Puzzle, Solution

MAX_SOLUTIONS_TO_FIND = 10
TIMEOUT_LIMIT = 30


class ClingoSolver:
    """A solver using clingo."""

    def __init__(self):
        """Initialize a solver."""
        self.clingo_instance: Control = Control()
        self.program: str = ""
        self.puzzle: Optional[Puzzle] = None
        self.solutions: List[Solution] = []

    def register_puzzle(self, puzzle: Puzzle):
        """Register the puzzle to the solution."""
        self.puzzle = puzzle
        logger.debug("[Solver] Puzzle registered.")

    def store_solutions(self, model: Model):
        """Get the solution."""
        if self.puzzle is None:
            raise PermissionError("Puzzle not registered.")

        solution_data = tuple(str(model).split())  # raw solution converted from clingo
        solution = Solution(self.puzzle)

        for item in solution_data:
            _type, _data = item.replace("(", " ").replace(")", " ").split()
            data = _data.split(",")

            r, c = data[:2]  # ensure the first two elements of data is the row and column

            if _type.startswith("edge_"):
                if _type == "edge_left":
                    solution.edge.add((int(r), int(c), Direction.LEFT))
                elif _type == "edge_top":
                    solution.edge.add((int(r), int(c), Direction.TOP))
                elif _type == "edge_diag_up":
                    solution.edge.add((int(r), int(c), Direction.DIAG_UP))
                elif _type == "edge_diag_down":
                    solution.edge.add((int(r), int(c), Direction.DIAG_DOWN))

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
                solution.symbol[(int(r), int(c))] = f"tri__{shaka_dict[data[2]]}__0"

            elif _type == "gray":
                solution.surface[(int(r), int(c))] = 8
            elif _type == "black":
                solution.surface[(int(r), int(c))] = 4

            else:
                solution.symbol[(int(r), int(c))] = str(_type)

        self.solutions.append(solution)

    def add_program_line(self, line: str):
        """Add a line to the program."""
        self.program += line + "\n"

    def reset(self):
        """Reset the program."""
        self.clingo_instance = Control()
        self.program = ""
        self.puzzle = None
        self.solutions = []

    def solve(self):
        """Solve the problem."""
        self.clingo_instance.configuration.sat_prepro = 2
        self.clingo_instance.configuration.asp.trans_ext = "dynamic"  # type: ignore
        self.clingo_instance.configuration.asp.eq = 1  # type: ignore
        self.clingo_instance.configuration.solve.models = MAX_SOLUTIONS_TO_FIND  # type: ignore
        self.clingo_instance.add("base", [], self.program)
        self.clingo_instance.ground()
        with self.clingo_instance.solve(  # pylint: disable=not-context-manager
            on_model=self.store_solutions, async_=True
        ) as handle:
            handle.wait(TIMEOUT_LIMIT)
            handle.cancel()


solver = ClingoSolver()
