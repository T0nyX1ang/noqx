"""The Yin-Yang solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import avoid_rect, connected, display, grid, orth_adjacent, shade_c
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(colors=["black", "white"]))
    solver.add_program_line(orth_adjacent())
    solver.add_program_line(connected(color="black"))
    solver.add_program_line(avoid_rect(rect_r=2, rect_c=2, color="black"))
    solver.add_program_line(connected(color="white"))
    solver.add_program_line(avoid_rect(rect_r=2, rect_c=2, color="white"))

    for (r, c), color in E.clues.items():
        color = "black" if color == "b" else "white"
        solver.add_program_line(f"color({r}, {c}, {color}).")

    solver.add_program_line(display())
    solver.solve()

    for solution in solver.solutions:
        for rc, color in solution.items():
            color = "black" if color == "1" else "white"
            solution[rc] += "_circle.png"

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
