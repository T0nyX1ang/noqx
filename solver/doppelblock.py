"""The Doppelblock solver."""

from typing import List

from .core.common import count, display, fill_num, grid, unique_num
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.row == puzzle.col, "Doppelblock puzzles must be square."
    n = puzzle.row

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=range(1, n - 1), color="black"))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(count(2, _type="row", color="black"))
    solver.add_program_line(unique_num(_type="col", color="grid"))
    solver.add_program_line(count(2, _type="col", color="black"))

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top number
        assert isinstance(num, int), "TOP clue should be integer."
        begin_r = f"Rb = #min {{ R: black(R, {c}) }}"
        end_r = f"Re = #max {{ R: black(R, {c}) }}"
        solver.add_program_line(f":- {begin_r}, {end_r}, #sum {{ N: number(R, {c}, N), R > Rb, R < Re }} != {num}.")

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left number
        assert isinstance(num, int), "LEFT clue should be integer."
        begin_c = f"Cb = #min {{ C: black({r}, C) }}"
        end_c = f"Ce = #max {{ C: black({r}, C) }}"
        solver.add_program_line(f":- {begin_c}, {end_c}, #sum {{ N: number({r}, C, N), C > Cb, C < Ce }} != {num}.")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), num in filter(
        lambda x: x[0][0] < n and x[0][0] >= 0 and x[0][1] < n and x[0][1] >= 0, puzzle.text.items()
    ):  # filter center number
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))
    solver.add_program_line(display(item="black", size=2))
    solver.solve()

    return solver.solutions
