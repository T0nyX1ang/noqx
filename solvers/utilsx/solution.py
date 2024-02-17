"""Generate solutions for the given problem."""

from typing import Dict, List

from clingo.control import Control
from clingo.solving import Model

from .border import Direction
from .loops import ISOLATED, NON_DIRECTED, DIRECTED

MAX_SOLUTIONS_TO_FIND = 10


def rc_to_grid(r: int, c: int):
    """Convert row and column to compatible grid coordinates."""
    return f"{r*2+1},{c*2+1}"


def rcd_to_edge(r, c, d):
    """Given an edge id, returns the border coordinate of the edge."""
    data = {
        Direction.TOP: f"{r*2},{c*2+1}",
        Direction.LEFT: f"{r*2+1},{c*2}",
        Direction.BOTTOM: f"{r*2+2},{c*2+1}",
        Direction.RIGHT: f"{r*2+1},{c*2+2}",
    }
    return data[d]


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
            _type, _data = item.replace("(", " ").replace(")", " ").split()
            data = _data.split(",")
            if not _type in ["loop_sign"]:
                data = map(int, data)
            else:
                data[:-1] = map(int, data[:-1])

            if _type.startswith("vertical"):
                r, c = data
                formatted[rcd_to_edge(r, c, Direction.LEFT)] = "black"
            elif _type.startswith("horizontal"):
                r, c = data
                formatted[rcd_to_edge(r, c, Direction.TOP)] = "black"
            elif _type == "number":
                r, c, num = data
                formatted[rc_to_grid(r, c)] = num
            elif _type == "loop_sign":
                r, c, sign = data
                sign = sign.replace('"', "")
                formatted[rc_to_grid(r, c)] = f"{sign}.png"
            else:
                # color
                r, c = data
                formatted[rc_to_grid(r, c)] = _type.replace("color", "")

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
