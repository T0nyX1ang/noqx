"""The Canal View solver."""

from typing import Dict, List

from .core.common import display, grid, shade_c
from .core.encoding import Encoding
from .core.neighbor import adjacent
from .core.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from .core.shape import avoid_rect
from .core.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
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
