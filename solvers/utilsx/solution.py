"""Generate solutions for the given problem."""

from typing import Dict, List
from enum import Enum

from clingo.control import Control
from clingo.solving import Model

MAX_SOLUTIONS_TO_FIND = 10
Direction = Enum("Direction", "LEFT TOP RIGHT BOTTOM")


def rc_to_grid(r: int, c: int):
    """Convert row and column to compatible grid coordinates."""
    return f"{r*2+1},{c*2+1}"


def rcd_to_edge(r, c, d):
    """Given an edge id, returns the border coordinate of the edge."""
    if d == Direction.TOP:
        return f"{r*2},{c*2+1}"
    elif d == Direction.LEFT:
        return f"{r*2+1},{c*2}"
    elif d == Direction.BOTTOM:
        return f"{r*2+2},{c*2+1}"
    elif d == Direction.RIGHT:
        return f"{r*2+1},{c*2+2}"


class ClingoSolver:
    """A solver using clingo."""

    def __init__(self):
        """Initialize a solver."""
        self.clingo_instance: Control = Control()
        self.program: str = ""
        self.solutions: List[Dict[str, str]] = []
        self.mode, self.R, self.C = None, None, None

    def store_solutions(self, model: Model):
        """Get the solution."""
        solution = tuple(str(model).split())  # raw solution converted from clingo
        formatted: Dict[str, str] = {}

        for item in solution:
            if self.mode == "shade":
                color, coords = item.replace("(", " ").replace(")", " ").split()
                r, c = coords.split(",")
                formatted[rc_to_grid(int(r), int(c))] = color.replace("color", "")
            elif self.mode == "region":
                type, coords = item.replace("(", " ").replace(")", " ").split()
                r, c = map(int, coords.split(","))
                if type.startswith("vertical"):
                    formatted[rcd_to_edge(r, c, Direction.LEFT)] = "black"
                elif type.startswith("horizontal"):
                    formatted[rcd_to_edge(r, c, Direction.TOP)] = "black"
            elif self.mode == "number":
                _, coords = item.replace("(", " ").replace(")", " ").split()
                r, c, num = coords.replace("(", " ").replace(")", " ").split(",")
                formatted[rc_to_grid(int(r), int(c))] = int(num)

        self.solutions.append(formatted)

    def add_program_line(self, line: str):
        """Add a line to the program."""
        self.program += line + "\n"

    def reset(self, mode: str, R: int = None, C: int = None):
        """Reset the program."""
        assert mode in ["shade", "region", "number"], "Mode must be in 'shade', 'region' or 'number'"
        self.mode = mode
        self.R, self.C = R, C
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
