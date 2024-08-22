"""The Box solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.penpa import Puzzle
from .core.solution import solver


def count_box_col(target: int, c: int, color: str = "black") -> str:
    """Generate a rule to count the number of 'boxes' in each column."""
    return f":- #sum {{ N: box_col(R, N), {color}(R, {c}) }} != {target}."


def count_box_row(target: int, r: int, color: str = "black") -> str:
    """Generate a rule to count the number of 'boxes' in each column."""
    return f":- #sum {{ N: box_row(C, N), {color}({r}, C) }} != {target}."


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for c in range(puzzle.col):
        target = puzzle.text.get((puzzle.row, c))
        assert isinstance(target, int), "BOTTOM clue must be an integer."
        solver.add_program_line(f"box_row({c}, {target}).")

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):
        assert isinstance(num, int), "LEFT clue must be an integer."
        solver.add_program_line(count_box_row(num, r, color="black"))

    for r in range(puzzle.row):
        target = puzzle.text.get((r, puzzle.col))
        assert isinstance(target, int), "RIGHT clue must be an integer."
        solver.add_program_line(f"box_col({r}, {target}).")

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):
        assert isinstance(num, int), "TOP clue must be an integer."
        solver.add_program_line(count_box_col(num, c, color="black"))

    solver.add_program_line(display())
    solver.solve()
    return solver.solutions
