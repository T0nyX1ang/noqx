"""The Aqre solver."""

from typing import List

from .core.common import area, count, display, grid, shade_c
from .core.penpa import Puzzle
from .core.helper import full_bfs
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[str]:
    R, C = puzzle.row, puzzle.col
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(R, C))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    # solver.add_program_line(grid_color_connected(color="gray", grid_size=(R, C)))
    solver.add_program_line(grid_color_connected(color="gray"))
    solver.add_program_line(avoid_rect(4, 1, color="gray"))
    solver.add_program_line(avoid_rect(1, 4, color="gray"))
    solver.add_program_line(avoid_rect(4, 1, color="not gray"))
    solver.add_program_line(avoid_rect(1, 4, color="not gray"))

    areas = full_bfs(R, C, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="gray", _type="area", _id=i))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
