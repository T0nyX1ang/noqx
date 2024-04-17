"""The Nurimisaki solver."""

from typing import Dict, List, Tuple

from .utilsx.common import display, grid, shade_c
from .utilsx.encoding import Encoding
from .utilsx.neighbor import adjacent, count_adjacent
from .utilsx.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from .utilsx.shape import avoid_rect
from .utilsx.solution import solver


def avoid_unknown_misaki(known_cells: List[Tuple[int, int]], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to avoid dead ends that does not have a record.

    A grid rule and an adjacent rule should be defined first.
    """

    included = ", ".join(f"|R - {src_r}| + |C - {src_c}| != 0" for src_r, src_c in known_cells)
    main = f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }} = 1"

    if not known_cells:
        return f"{main}."
    return f"{main}, {included}."


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="not black"))

    all_src: List[Tuple[int, int]] = []
    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        elif clue == "yellow":
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(count_adjacent(1, (r, c), color="not black"))
            all_src.append((r, c))
        else:
            num = int(clue)
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(count_adjacent(1, (r, c), color="not black"))
            solver.add_program_line(bulb_src_color_connected((r, c), color="not black"))
            solver.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black"))
            all_src.append((r, c))

    solver.add_program_line(avoid_unknown_misaki(all_src, color="not black"))
    solver.add_program_line(display())
    solver.solve()

    return solver.solutions
