"""Generate solutions for the given problem."""

from typing import List, Optional

from clingo.control import Control
from clingo.solving import Model

from .penpa import Direction, Puzzle, Solution

MAX_SOLUTIONS_TO_FIND = 10


class ClingoSolver:
    """A solver using clingo."""

    def __init__(self):
        """Initialize a solver."""
        self.clingo_instance: Control = Control()
        self.program: str = ""
        self.puzzle: Optional[Puzzle] = None
        self.solutions: List[str] = []

    def register_puzzle(self, puzzle: Puzzle):
        """Register the puzzle to the solution."""
        self.puzzle = puzzle
        print("[Solver] Puzzle registered.")

    def store_solutions(self, model: Model):
        """Get the solution."""
        if self.puzzle is None:
            raise ValueError("Puzzle not registered.")

        solution_data = tuple(str(model).split())  # raw solution converted from clingo
        solution = Solution(self.puzzle)

        for item in solution_data:
            _type, _data = item.replace("(", " ").replace(")", " ").split()
            data = _data.split(",")
            r, c = data[:2]  # ensure the first two elements of data is the row and column

            if _type.startswith("vertical"):
                solution.edge.add((int(r), int(c), Direction.LEFT))
            elif _type.startswith("horizontal"):
                solution.edge.add((int(r), int(c), Direction.TOP))

            elif _type.startswith("number") or _type.startswith("content"):
                if self.puzzle.puzzle_type == "easyasabc":  # convert penpa number to letter
                    solution.text[(int(r), int(c))] = self.puzzle.param["letters"][int(data[2]) - 1]
                else:
                    solution.text[(int(r), int(c))] = int(data[2])

            elif _type == "triangle":
                solution.symbol[(int(r), int(c))] = f"tri__{data[2]}"

            elif _type == "gray":
                solution.surface[(int(r), int(c))] = 8
            elif _type == "black":
                solution.surface[(int(r), int(c))] = 4

            else:
                solution.symbol[(int(r), int(c))] = str(_type)

        self.solutions.append(str(solution))

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
        self.clingo_instance.solve(on_model=self.store_solutions)


solver = ClingoSolver()
