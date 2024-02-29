"""The Tasquare solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import adjacent, count_region, region, shade_c, connected
from .utilsx.shape import all_rect
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(connected(color="not black"))
    solver.add_program_line(all_rect(color="black", square=True))

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        elif clue == "yellow":
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(region((r, c), color="black"))
            solver.add_program_line(count_region(2, (r, c), color="black", op="ge"))
        else:
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(region((r, c), color="black"))

            num = int(clue)
            solver.add_program_line(count_region(num + 1, (r, c), color="black"))

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
