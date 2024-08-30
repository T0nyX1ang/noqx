"""The Star Battle solver."""

from typing import List

from .core.common import area, count, display, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.helper import full_bfs
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.param["stars"].isdigit(), "Invalid star count."
    num_stars = int(puzzle.param["stars"])

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="star__2__0"))

    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_adjacent_color(color="star__2__0", adj_type=8))

    solver.add_program_line(count(num_stars, color="star__2__0", _type="row"))
    solver.add_program_line(count(num_stars, color="star__2__0", _type="col"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count(num_stars, color="star__2__0", _type="area", _id=i))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"star__2__0({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not star__2__0({r}, {c}).")

    solver.add_program_line(display(item="star__2__0"))
    solver.solve()

    return solver.solutions
