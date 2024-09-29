"""The Hitori solver."""

from typing import List

from .core.common import display, grid, shade_c, unique_num
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(unique_num(color="not black", _type="row"))
    solver.add_program_line(unique_num(color="not black", _type="col"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color())
    solver.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions
