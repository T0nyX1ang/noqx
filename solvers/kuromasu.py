"""The Kuromasu solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import (
    avoid_adjacent,
    connected,
    count_lit_up,
    display,
    grid,
    lit_up,
    orth_adjacent,
    reachable,
    shade_c,
)
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(orth_adjacent())
    solver.add_program_line(avoid_adjacent(color="black"))
    solver.add_program_line(reachable(color="not black"))
    solver.add_program_line(connected(color="not black"))

    for (r, c), num in E.clues.items():
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(lit_up(r, c, color="not black"))
        solver.add_program_line(count_lit_up(num, r, c, color="not black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
