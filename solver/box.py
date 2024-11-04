"""The Box solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.solution import solver


def count_box_col(target: int, c: int, color: str = "black") -> str:
    """Generate a rule to count the number of 'boxes' in each column."""
    return f":- #sum {{ N: box_col(R, N), {color}(R, {c}) }} != {target}."


def count_box_row(target: int, r: int, color: str = "black") -> str:
    """Generate a rule to count the number of 'boxes' in each column."""
    return f":- #sum {{ N: box_row(C, N), {color}({r}, C) }} != {target}."


def solve(puzzle: Puzzle) -> List[Solution]:
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


__metadata__ = {
    "name": "Box",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VXPj9o8EL3nr1j57IMd5/eNbpdeaPoDqtUqilaBZrWooLSBVJ+M+N93PJOQadNLD1/LoQoePZ7fmDcexxy+dVVbS63dxyRSSUAyCCMcWvs4VP+stsddnd3IWXd8bloAUr6bz+VTtTvUXuEy4Sm9k00zO5P2TVYILaTwYWhRSvshO9m3mc2lXcKUkAa4BYl8gHcjvMd5h26J1Apw3mOADwA323azqx8XxLzPCruSwv3OK8x2UOyb77Xofbjvm2a/3jpiXR2hmMPz9ms/c+g+N1+6XqvLs7Qzsrsc7AajXee8t+sg2XXoF3ZdFf+z3bQ8n2HbP4Lhx6xw3j+NMBnhMjtBzLOTMAZTQzBDzREmcIxvGBM6xijGRBNNPGESZPjK6c+aQE0YjUzEGFxZu83smZAYIaOeiHwkglESIwMHbpDElMPcJMjATw+SlFaBpEGiFVKw7qDRauJGa6Rg5YvIxzRWgzYDc9HQhsFGjiKqNGaiENN+EFGtCRNF05Wo2pSJEuozZ6jPnKE+cwb7zOunXePFJthnXlqCfeZ1pNhnbjrFPl8cwmnUeCYfMM4x+hhXcGSlNRhfY1QYQ4wL1NxhvMd4izHAGKEmdof+t16LP2CnCBK6J9kTXxdTeoVYdu1Ttanhssm7/bpub/Km3Vc7Abf72RP/CRyFcX8W/y78v3Thuxaoazvf12YH3rjSewE=",
        },
    ],
}
