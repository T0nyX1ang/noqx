"""The Country Road solver."""

from typing import List

from .core.common import area, count, direction, display, fill_path, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.helper import full_bfs
from .core.loop import pass_area_once, single_loop
from .core.neighbor import adjacent, avoid_area_adjacent
from .core.reachable import grid_color_connected
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="country_road"))
    solver.add_program_line(fill_path(color="country_road"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="country_road", adj_type="loop"))
    solver.add_program_line(single_loop(color="country_road"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(pass_area_once(ar))
        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="country_road", _type="area", _id=i))

    solver.add_program_line(avoid_area_adjacent(color="not country_road", adj_type=4))
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
