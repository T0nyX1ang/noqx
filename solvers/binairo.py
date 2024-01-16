"""The Binario solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import avoid_rect, count, display, grid, shade_c, unique_linecolor
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    if not (E.R % 2 == 0 and E.C % 2 == 0):
        raise ValueError("# rows and # columns must both be even!")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(count(E.R // 2, color="black", _type="row"))
    solver.add_program_line(count(E.C // 2, color="black", _type="col"))
    solver.add_program_line(unique_linecolor(colors=["black", "not black"], _type="row"))
    solver.add_program_line(unique_linecolor(colors=["black", "not black"], _type="col"))
    solver.add_program_line(avoid_rect(1, 3, color="black"))
    solver.add_program_line(avoid_rect(1, 3, color="not black"))
    solver.add_program_line(avoid_rect(3, 1, color="black"))
    solver.add_program_line(avoid_rect(3, 1, color="not black"))

    for (r, c), num in E.clues.items():
        if num == 1:
            solver.add_program_line(f"black({r}, {c}).")
        else:
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
