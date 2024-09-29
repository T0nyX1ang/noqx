"""The Cocktail Lamp solver."""

from typing import List

from .core.common import area, count, display, grid, shade_c
from .core.helper import full_bfs
from .core.neighbor import adjacent, avoid_area_adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import area_color_connected, grid_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_area_adjacent(color="gray"))
    solver.add_program_line(grid_color_connected(color="gray", adj_type=8, grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.text[rc]

            if data == "?":
                continue

            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="gray", _type="area", _id=i))

    solver.add_program_line(area_color_connected(color="gray", adj_type=4))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
