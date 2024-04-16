"""The Canal View solver."""

from typing import List

from . import utilsx
from .utilsx.common import display, grid
from .utilsx.encoding import Encoding
from .utilsx.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from .utilsx.rule import adjacent, shade_c
from .utilsx.shape import avoid_rect
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        else:
            num = int(clue)
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(bulb_src_color_connected((r, c), color="black"))
            solver.add_program_line(count_reachable_src(num + 1, (r, c), main_type="bulb", color="black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
