"""The Kakuru solver."""

from typing import List

from .core.common import display, grid
from .core.penpa import Puzzle, Solution
from .core.neighbor import adjacent
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line("{ number(R, C, (1..9)) } = 1 :- grid(R, C), not black(R, C).")
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(":- adj_8(R, C, R1, C1), number(R, C, N), number(R1, C1, N).")

    for (r, c), clue in puzzle.text.items():
        solver.add_program_line(f":- number(_, _, N), {{ grid(R, C): number(R, C, N), adj_8(R, C, {r}, {c}) }} > 1.")
        if clue != "?":
            assert isinstance(clue, int), "Clue should be integer or '?'."
            solver.add_program_line(f":- #sum {{ N: number(R, C, N), adj_8(R, C, {r}, {c}) }} != {clue}.")

    for (r, c), color_code in puzzle.surface.items():
        if color_code == 4:  # shaded color (BK)
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions
