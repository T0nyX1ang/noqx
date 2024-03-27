"""Generate solutions for the given problem."""

from typing import Dict, List

from clingo.control import Control
from clingo.solving import Model

from .coord import Direction, rc_to_grid, rcd_to_edge

MAX_SOLUTIONS_TO_FIND = 10


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
            if _type not in ["loop_sign", "triangle"]:
                data = map(int, data)
            else:
                data[:-1] = map(int, data[:-1])

            if _type.startswith("vertical"):
                r, c = data
                formatted[rcd_to_edge(r, c, Direction.LEFT)] = "black"
            elif _type.startswith("horizontal"):
                r, c = data
                formatted[rcd_to_edge(r, c, Direction.TOP)] = "black"
            elif _type.startswith("number"):
                r, c, num = data
                formatted[rc_to_grid(r, c)] = num
            elif _type == "loop_sign":
                r, c, sign = data
                sign = sign.replace('"', "")
                if sign != "":
                    formatted[rc_to_grid(r, c)] = f"{sign}.png"
            elif _type == "triangle":
                r, c, sign = data
                sign = sign.replace('"', "")
                dat2png = {
                    "ul": "top-left.png",
                    "ur": "top-right.png",
                    "dl": "bottom-left.png",
                    "dr": "bottom-right.png",
                }
                formatted[rc_to_grid(r, c)] = dat2png[sign]
            elif _type == "slant_code":
                r, c, code = data
                sign = ""
                sign += "tl" if code & 1 else ""
                sign += "tr" if code >> 1 & 1 else ""
                sign += "br" if code >> 3 & 1 else ""
                sign += "bl" if code >> 2 & 1 else ""
                if len(sign):
                    formatted[rc_to_grid(r, c)] = sign + ".png"
                # formatted[rc_to_grid(r, c)] = code
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
