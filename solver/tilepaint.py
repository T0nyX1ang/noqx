"""The Nonogram solver."""

from typing import List

from .core.common import area, count, display, grid, shade_c
from .core.helper import full_bfs
from .core.penpa import Puzzle, Solution
from .core.shape import area_same_color
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    top_clues = {}
    for c in range(puzzle.col):
        data = puzzle.sudoku.get((-1, c))
        data = data.get(2) if data else 0
        assert isinstance(data, int), "Clue must be an integer."
        top_clues[c] = (data,)

    left_clues = {}
    for r in range(puzzle.row):
        data = puzzle.sudoku.get((r, -1))
        data = data.get(1) if data else 0
        assert isinstance(data, int), "Clue must be an integer."
        left_clues[r] = (data,)

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(area_same_color(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, (ar, _) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c), clue in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.sudoku.items()):  # filter top number
        num = clue.get(2)
        if num is not None:
            assert isinstance(num, int), "TOP clue must be an integer."
            solver.add_program_line(count(num, color="gray", _type="col", _id=c))

    for (r, c), clue in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.sudoku.items()):  # filter left number
        num = clue.get(1)
        if num is not None:
            assert isinstance(num, int), "LEFT clue must be an integer."
            solver.add_program_line(count(num, color="gray", _type="row", _id=r))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
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
