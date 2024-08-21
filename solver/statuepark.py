"""The Statue Park solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.penpa import Puzzle
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.shape import OMINOES, all_shapes, count_shape, general_shape
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[str]:
    shapeset = puzzle.param["shapeset"]
    if shapeset == "tetro":
        omino_num, omino_count_type = 4, 1
    elif shapeset == "pento":
        omino_num, omino_count_type = 5, 1
    elif shapeset == "double_tetro":
        omino_num, omino_count_type = 4, 2
    else:
        raise AssertionError("Shape set not supported.")

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not gray"))

    solver.add_program_line(all_shapes(f"omino_{omino_num}", color="gray"))
    for i, o_shape in enumerate(OMINOES[omino_num].values()):
        solver.add_program_line(general_shape(f"omino_{omino_num}", i, o_shape, color="gray", adj_type=4))
        solver.add_program_line(count_shape(omino_count_type, name=f"omino_{omino_num}", _id=i, color="gray"))

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
