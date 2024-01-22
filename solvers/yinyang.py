"""The Yin-Yang solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import (
    adjacent,
    avoid_rect,
    connected,
    display,
    grid,
    shade_c,
)
from .utilsx.solutions import rc_to_grid, solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(connected(color="black"))
    solver.add_program_line(avoid_rect(rect_r=2, rect_c=2, color="black"))
    solver.add_program_line(connected(color="not black"))
    solver.add_program_line(avoid_rect(rect_r=2, rect_c=2, color="not black"))

    for (r, c), color in E.clues.items():
        color = "black" if color == "b" else "not black"
        solver.add_program_line(f"{color}({r}, {c}).")

    solver.add_program_line(display(color="black"))
    solver.solve()

    for solution in solver.solutions:
        for r in range(E.R):
            for c in range(E.C):
                rc = rc_to_grid(r, c)
                solution[rc] = "white_circle.png" if rc not in solution else "black_circle.png"

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
