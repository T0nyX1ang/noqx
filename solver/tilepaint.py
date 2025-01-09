"""The Nonogram solver."""

from typing import List

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type
from noqx.rule.shape import area_same_color
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
        assert isinstance(num, int), f"Clue at ({r}, {c}) must be an integer."

        if r == -1 and 0 <= c < puzzle.col:
            validate_type(pos, "sudoku_2")
            solver.add_program_line(count(num, color="gray", _type="col", _id=c))

        if c == -1 and 0 <= r < puzzle.row:
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
