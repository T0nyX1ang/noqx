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
