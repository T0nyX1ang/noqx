"""The Tasquare solver."""

from typing import List

from .utilsx.common import display, grid, shade_c
from .utilsx.encoding import Encoding
from .utilsx.neighbor import adjacent, count_adjacent
from .utilsx.reachable import (
    count_reachable_src,
    grid_color_connected,
    grid_src_color_connected,
)
from .utilsx.shape import all_rect
from .utilsx.solution import solver


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not black"))
    solver.add_program_line(all_rect(color="black", square=True))

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        elif clue == "yellow":
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(count_adjacent(("gt", 0), (r, c), color="black"))
        else:
            num = int(clue)
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(grid_src_color_connected((r, c), color="black"))
            solver.add_program_line(count_reachable_src(num + 1, (r, c), color="black"))

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions
