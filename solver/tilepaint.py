"""The Tilepaint solver."""

from typing import List

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import area_same_color
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(area_same_color(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, (ar, _) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)

        if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
            validate_type(pos, "sudoku_2")
            solver.add_program_line(count(num, color="gray", _type="col", _id=c))

        if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
            validate_type(pos, "sudoku_1")
            solver.add_program_line(count(num, color="gray", _type="row", _id=r))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Tilepaint",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=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",
        }
    ],
}
