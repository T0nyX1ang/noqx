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
    """
    Given an edge id, returns the border coordinate of the edge.
    """
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
        self.mode = "shade"
        self.R, self.C = None, None

    def store_solutions(self, model: Model):
        """Get the solution."""
        solution = tuple(str(model).split())  # raw solution converted from clingo
        formatted: Dict[str, str] = {}
        if self.mode == "region":
            assert self.R is not None and self.C is not None
            region = [[None for _ in range(self.C)] for _ in range(self.R)]

        for item in solution:
            if self.mode == "shade":
                color, coords = item.replace("(", " ").replace(")", " ").split()
                r, c = coords.split(",")
                formatted[rc_to_grid(int(r), int(c))] = color.replace("color", "")
            elif self.mode == "region":
                _, coords = item.replace("(", " ").replace(")", " ").split()
                r, c, id = map(int, coords.split(","))
                region[r][c] = id
            elif self.mode == "number":
                raise NotImplementedError("Number mode not implemented!")

        if self.mode == "region":
            print(region)
            for r in range(self.R):
                for c in range(self.C):
                    if r and region[r][c] != region[r - 1][c]:
                        formatted[rcd_to_edge(r, c, Direction.TOP)] = "black"
                    if c and region[r][c] != region[r][c - 1]:
                        formatted[rcd_to_edge(r, c, Direction.LEFT)] = "black"
            for c in range(self.C):
                formatted[rcd_to_edge(0, c, Direction.TOP)] = "black"
                formatted[rcd_to_edge(self.R - 1, c, Direction.BOTTOM)] = "black"
            for r in range(self.R):
                formatted[rcd_to_edge(r, 0, Direction.LEFT)] = "black"
                formatted[rcd_to_edge(r, self.C - 1, Direction.RIGHT)] = "black"

        self.solutions.append(formatted)

    def add_program_line(self, line: str):
        """Add a line to the program."""
        self.program += line + "\n"

    def reset(self, mode: str = "shade", R: int = None, C: int = None):
        """Reset the program."""
        assert mode in ["shade", "region", "number"], "Mode must be in shade, region, number!"
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
