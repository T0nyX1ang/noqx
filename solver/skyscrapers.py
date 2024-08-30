"""The Skyscrapers solver."""

from typing import List

from .core.common import display, fill_num, grid, unique_num
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.row == puzzle.col, "Doppelblock puzzles must be square."
    n = puzzle.row

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=range(1, n + 1)))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(unique_num(_type="col", color="grid"))

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top number
        assert isinstance(num, int), "TOP clue should be integer."
        solver.add_program_line(f"blocked_t(R, {c}) :- number(R, {c}, N), number(R1, {c}, N1), R1 < R, N1 > N.")
        solver.add_program_line(f":- #count {{ R: blocked_t(R, {c}) }} != {n - num}.")

    for (r, c), num in filter(lambda x: x[0][0] == n and x[0][1] >= 0, puzzle.text.items()):  # filter bottom number
        assert isinstance(num, int), "BOTTOM clue should be integer."
        solver.add_program_line(f"blocked_b(R, {c}) :- number(R, {c}, N), number(R1, {c}, N1), R1 > R, N1 > N.")
        solver.add_program_line(f":- #count {{ R: blocked_b(R, {c}) }} != {n - num}.")

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left number
        assert isinstance(num, int), "LEFT clue should be integer."
        solver.add_program_line(f"blocked_l({r}, C) :- number({r}, C, N), number({r}, C1, N1), C1 < C, N1 > N.")
        solver.add_program_line(f":- #count {{ C: blocked_l({r}, C) }} != {n - num}.")

    for (r, c), num in filter(lambda x: x[0][1] == n and x[0][0] >= 0, puzzle.text.items()):  # filter right number
        assert isinstance(num, int), "RIGHT clue should be integer."
        solver.add_program_line(f"blocked_r({r}, C) :- number({r}, C, N), number({r}, C1, N1), C1 > C, N1 > N.")
        solver.add_program_line(f":- #count {{ C: blocked_r({r}, C) }} != {n - num}.")

    for (r, c), num in filter(
        lambda x: x[0][0] < n and x[0][0] >= 0 and x[0][1] < n and x[0][1] >= 0, puzzle.text.items()
    ):  # filter center number
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions
