"""The Nurikabe solver."""

from typing import Dict, List

from .utilsx.common import display, grid, shade_c
from .utilsx.encoding import Encoding
from .utilsx.neighbor import adjacent
from .utilsx.reachable import (
    avoid_unknown_src,
    count_reachable_src,
    grid_color_connected,
    grid_src_color_connected,
)
from .utilsx.shape import avoid_rect
from .utilsx.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))

    all_src = []
    for (r, c), clue in E.clues.items():
        if isinstance(clue, int) or clue == "yellow":
            all_src.append((r, c))

    if not all_src:
        raise ValueError("No clues found.")

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        else:
            current_excluded = [src for src in all_src if src != (r, c)]
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color="not black"))

            if clue != "yellow":
                num = int(clue)
                solver.add_program_line(count_reachable_src(num, (r, c), color="not black"))

    solver.add_program_line(avoid_unknown_src(color="not black"))
    solver.add_program_line(display())
    solver.solve()

    return solver.solutions
