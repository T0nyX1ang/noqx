"""The Lits solver."""

from typing import List

from .utilsx.common import area, display, grid, shade_c
from .utilsx.encoding import Encoding, tag_encode
from .utilsx.helper import full_bfs
from .utilsx.neighbor import adjacent, area_adjacent
from .utilsx.reachable import grid_color_connected
from .utilsx.shape import OMINOES, all_shapes, avoid_rect, count_shape, general_shape
from .utilsx.solution import solver


def avoid_adjacent_same_omino(num: int = 4, color: str = "black", adj_type: int = 4) -> None:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An area adjacent rule, an omino rule should be defined first.
    """
    tag = tag_encode("belong_to_shape", "omino", num, color)
    return f":- area_adj_{adj_type}_{color}(A, A1), A < A1, {tag}(A, _, _, T, _), {tag}(A1, _, _, T, _)."


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="gray"))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for i, o_type in enumerate(["L", "I", "T", "S"]):
        o_shape = OMINOES[4][o_type]
        solver.add_program_line(general_shape("omino_4", i, o_shape, color="gray", _type="area", simple=True))

    solver.add_program_line(all_shapes("omino_4", color="gray", _type="area"))
    solver.add_program_line(count_shape(1, "omino_4", _id=None, color="gray", _type="area"))
    solver.add_program_line(area_adjacent(color="gray"))
    solver.add_program_line(avoid_adjacent_same_omino(4, color="gray"))

    for (r, c), clue in E.clues.items():
        if clue == "gray":
            solver.add_program_line(f"gray({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
