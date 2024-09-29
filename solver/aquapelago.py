"""The Aquapelago solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.penpa import Puzzle, Solution
from .core.reachable import count_reachable_src, grid_color_connected, grid_src_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
    solver.add_program_line(avoid_rect(2, 2, color="not black"))
    solver.add_program_line(grid_color_connected(color="not black", adj_type=4, grid_size=(puzzle.row, puzzle.col)))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(grid_src_color_connected((r, c), color="black", adj_type=8))
        solver.add_program_line(count_reachable_src(num, (r, c), color="black", adj_type=8))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions
