"""The Heyawake solver."""

from typing import List

from .core.common import area, count, display, grid, shade_c
from .core.helper import full_bfs
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.penpa import Direction, Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def avoid_diamond_pattern(color: str = "black") -> str:
    """Avoid diamond patterns (radius = 1)."""
    rule = f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), not grid(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), not grid(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), not grid(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), not grid(R, C + 1).\n"

    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))

    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="gray"))
    solver.add_program_line(grid_color_connected(color="not gray"))
    solver.add_program_line(avoid_diamond_pattern(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
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

    for r in range(puzzle.row):
        borders_in_row = [c for c in range(1, puzzle.col) if (r, c, Direction.LEFT) in puzzle.edge]
        for i in range(len(borders_in_row) - 1):
            b1, b2 = borders_in_row[i], borders_in_row[i + 1]
            solver.add_program_line(avoid_rect(1, b2 - b1 + 2, color="not gray", corner=(r, b1 - 1)))

    for c in range(puzzle.col):
        borders_in_col = [r for r in range(1, puzzle.row) if (r, c, Direction.TOP) in puzzle.edge]
        for i in range(len(borders_in_col) - 1):
            b1, b2 = borders_in_col[i], borders_in_col[i + 1]
            solver.add_program_line(avoid_rect(b2 - b1 + 2, 1, color="not gray", corner=(b1 - 1, c)))

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
