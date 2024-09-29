"""The Lits solver."""

from typing import List

from .core.common import area, display, grid, shade_c
from .core.helper import full_bfs, tag_encode
from .core.neighbor import adjacent, area_adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.shape import OMINOES, all_shapes, avoid_rect, count_shape, general_shape
from .core.solution import solver


def avoid_adjacent_same_omino(num: int = 4, color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An area adjacent rule, an omino rule should be defined first.
    """
    tag = tag_encode("belong_to_shape", "omino", num, color)
    return f":- area_adj_{adj_type}_{color}(A, A1), A < A1, {tag}(A, _, _, T, _), {tag}(A1, _, _, T, _)."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for i, o_type in enumerate(["L", "I", "T", "S"]):
        o_shape = OMINOES[4][o_type]
        solver.add_program_line(general_shape("omino_4", i, o_shape, color="gray", _type="area", simple=True))

    solver.add_program_line(all_shapes("omino_4", color="gray", _type="area"))
    solver.add_program_line(count_shape(1, "omino_4", _id=None, color="gray", _type="area"))
    solver.add_program_line(area_adjacent(color="gray"))
    solver.add_program_line(avoid_adjacent_same_omino(4, color="gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
