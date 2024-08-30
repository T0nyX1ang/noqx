"""The Simple Loop solver."""

from typing import List

from .core.common import direction, display, fill_path, grid
from .core.penpa import Puzzle, Solution
from .core.loop import single_loop
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("simpleloop(R, C) :- grid(R, C), not black(R, C).")
    solver.add_program_line(fill_path(color="simpleloop"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="simpleloop", adj_type="loop"))
    solver.add_program_line(single_loop(color="simpleloop"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
