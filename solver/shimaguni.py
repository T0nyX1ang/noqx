"""The Shimaguni solver."""

from typing import List

from .core.common import area, count, display, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.helper import full_bfs
from .core.neighbor import adjacent, area_adjacent, avoid_area_adjacent
from .core.reachable import area_color_connected
from .core.solution import solver


def adjacent_area_different_size(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to enforce that adjacent areas have different sizes.

    An adjacent area rule and an area rule should be defined first.
    """
    size_count = f"#count {{R, C: area(A, R, C), {color}(R, C) }} = N"
    size1_count = f"#count {{R, C: area(A1, R, C), {color}(R, C) }} = N1"
    return f":- area_adj_{adj_type}(A, A1), A < A1, {size_count}, {size1_count}, N = N1."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="gray", _type="area", _id=i))
        else:
            solver.add_program_line(count(("ge", 1), color="gray", _type="area", _id=i))

    solver.add_program_line(area_color_connected(color="gray"))
    solver.add_program_line(avoid_area_adjacent(color="gray"))
    solver.add_program_line(area_adjacent())
    solver.add_program_line(adjacent_area_different_size(color="gray"))
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
