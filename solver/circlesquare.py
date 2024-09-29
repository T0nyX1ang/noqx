"""The Circles and Squares solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.shape import all_rect, avoid_rect
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line("green(R, C) :- grid(R, C), not gray(R, C).")
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))
    solver.add_program_line(all_rect(color="green", square=True))

    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name == "circle_M__2__0":
            solver.add_program_line(f"gray({r}, {c}).")
        elif symbol_name == "circle_M__1__0":
            solver.add_program_line(f"not gray({r}, {c}).")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
