"""The Kurodoko solver."""

from typing import Dict, List

from .core.common import display, grid, shade_c
from .core.encoding import Encoding
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from .core.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="black"))
    solver.add_program_line(grid_color_connected(color="not black"))

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        else:
            num = int(clue)
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(bulb_src_color_connected((r, c), color="not black"))
            solver.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions
