"""The Nanro solver."""

from typing import List

from .core.common import area, count, display, fill_num, grid
from .core.penpa import Puzzle, Solution
from .core.helper import full_bfs
from .core.neighbor import adjacent, area_adjacent
from .core.reachable import grid_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def nanro_fill_constraint(color: str = "black") -> str:
    """Generate a constraint for the number filling in nanro."""
    return f":- number(R0, C0, N), area(A, R0, C0), #count {{ R, C : area(A, R, C), {color}(R, C) }} != N."


def nanro_avoid_adjacent() -> str:
    """Generate a rule to avoid adjacent cells with the same number."""
    area_adj = area_adjacent()
    area_adj = area_adj[area_adj.find(":-") : -1]
    return f"{area_adj}, number(R, C, N), number(R1, C1, N)."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not gray"))
    solver.add_program_line(avoid_rect(2, 2, color="not gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.sudoku)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i, color="gray"))

        if rc:
            data = puzzle.sudoku[rc].get(0)
            assert isinstance(data, int), "Signpost clue should be integer."
            solver.add_program_line(count(data, color="not gray", _type="area", _id=i))
        else:
            solver.add_program_line(count(("gt", 0), color="not gray", _type="area", _id=i))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(nanro_fill_constraint(color="not gray"))
    solver.add_program_line(nanro_avoid_adjacent())
    solver.add_program_line(display(item="gray", size=2))
    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions
