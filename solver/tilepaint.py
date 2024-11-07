"""The Nonogram solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.shape import area_same_color
from noqx.solution import solver


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
        assert isinstance(num, int), "TOP clue must be an integer."
        solver.add_program_line(count(num, color="gray", _type="col", _id=c))

    for (r, c), clue in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.sudoku.items()):  # filter left number
        num = clue.get(1)
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
