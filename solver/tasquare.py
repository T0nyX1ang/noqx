"""The Tasquare solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.penpa import Puzzle
from .core.neighbor import adjacent, count_adjacent
from .core.reachable import (
    count_reachable_src,
    grid_color_connected,
    grid_src_color_connected,
)
from .core.shape import all_rect
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(all_rect(color="black", square=True))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(f"not black({r}, {c}).")
        if isinstance(num, int):
            solver.add_program_line(grid_src_color_connected((r, c), color="black"))
            solver.add_program_line(count_reachable_src(num + 1, (r, c), color="black"))
        else:
            solver.add_program_line(count_adjacent(("gt", 0), (r, c), color="black"))

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions
