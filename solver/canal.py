"""The Canal View solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.penpa import Puzzle
from .core.neighbor import adjacent
from .core.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from .core.shape import avoid_rect
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(bulb_src_color_connected((r, c), color="black"))
        solver.add_program_line(count_reachable_src(num + 1, (r, c), main_type="bulb", color="black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions
