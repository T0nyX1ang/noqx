"""The Sudoku solver."""

from typing import List

from .core.common import area, display, fill_num, grid, unique_num
from .core.penpa import Puzzle
from .core.neighbor import adjacent
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[str]:
    assert puzzle.row == puzzle.col, "Doppelblock puzzles must be square."
    n = puzzle.row

    sep = {9: (3, 3), 8: (2, 4), 6: (2, 3), 4: (2, 2)}

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(n, n))
    solver.add_program_line(adjacent(_type="x"))

    seg_i, seg_j = sep[n]
    for i in range(n):
        for j in range(n):
            area_id = (i // seg_i) * (n // seg_j) + (j // seg_j)
            solver.add_program_line(area(area_id, [(i, j)]))

    solver.add_program_line(fill_num(_range=range(1, n + 1)))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(unique_num(_type="col", color="grid"))
    solver.add_program_line(unique_num(_type="area", color="grid"))

    for (r, c), num in filter(
        lambda x: x[0][0] < n and x[0][0] >= 0 and x[0][1] < n and x[0][1] >= 0, puzzle.text.items()
    ):  # filter center number
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    if puzzle.param["diagonal"]:  # diagonal rule
        for i in range(n):
            solver.add_program_line(f"area({n + 1}, {i}, {i}).")
            solver.add_program_line(f"area({n + 2}, {i}, {8 - i}).")

    if puzzle.param["untouch"]:  # untouch rule
        solver.add_program_line(":- number(R, C, N), number(R1, C1, N), adj_x(R, C, R1, C1).")

    if puzzle.param["antiknight"]:  # antiknight rule
        solver.add_program_line("adj_knight(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| = 2, |C - C1| = 1.")
        solver.add_program_line("adj_knight(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| = 1, |C - C1| = 2.")
        solver.add_program_line(":- number(R, C, N), number(R1, C1, N), adj_knight(R, C, R1, C1).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions
