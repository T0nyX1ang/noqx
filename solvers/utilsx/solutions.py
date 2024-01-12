"""Generate solutions for the given problem."""

from typing import Dict, List

from clingo.control import Control
from clingo.solving import Model

MAX_SOLUTIONS_TO_FIND = 10


def rc_to_grid(r: int, c: int):
    """Convert row and column to compatible grid coordinates."""
    return f"{2*r+1},{2*c+1}"


class ClingoSolver:
    """A solver using clingo."""

    def __init__(self):
        """Initialize a solver."""
        self.clingo_instance: Control = Control()
        self.program: str = ""
        self.solutions: List[Dict[str, str]] = []

    def store_solutions(self, model: Model):
        """Get the solution."""
        solution = tuple(str(model).split())  # raw solution converted from clingo
        formatted: Dict[str, str] = {}

        for item in solution:
            r, c, color = item.replace("color(", "").replace(")", "").split(",")
            formatted[rc_to_grid(int(r), int(c))] = color

        self.solutions.append(formatted)

    def add_program_line(self, line: str):
        """Add a line to the program."""
        self.program += line + "\n"

    def reset(self):
        """Reset the program."""
        self.clingo_instance = Control()
        self.program = ""
        self.solutions = []

    def solve(self):
        """Solve the problem."""
        self.clingo_instance.configuration.sat_prepro = 2
        self.clingo_instance.configuration.asp.trans_ext = "dynamic"
        self.clingo_instance.configuration.asp.eq = 1
        self.clingo_instance.configuration.solve.models = MAX_SOLUTIONS_TO_FIND
        self.clingo_instance.add("base", [], self.program)
        self.clingo_instance.ground()
        self.clingo_instance.solve(on_model=self.store_solutions)


solver = ClingoSolver()
