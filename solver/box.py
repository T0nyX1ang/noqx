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

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f":- not black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f":- black({r}, {c}).")

    solver.add_program_line(display())
    solver.solve()
    return solver.solutions


__metadata__ = {
    "name": "Box",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVBj5s8EL3zK1Y+zwFjA4Zbut30kma/r0m1WiEUEcpqoxKxJaGqHOW/73gMwS09tIfu9lARj14eb5w3Hts5fOmKtgLOzUco8AERyDCiwXlAw++f9e5YV+kVzLrjY9MiALidz+GhqA+Vl5lMfHLvpJNUz0C/SzPGGbAAB2c56P/Tk36f6iXoFb5iIJBbWFGA8GaEd/TeoGtLch/xsscI7xGWu7asq83CMv+lmV4DM7/zhrINZPvma8V6H+Z72ey3O0NsiyMWc3jcPfVvDt2n5nPXa3l+Bj2zdleDXTnaNc57uwZauwb9xK6p4g/bTfLzGZf9AxrepJnx/nGEaoSr9IRxmZ6YEJQaohnbHCakYQLhMKFhhO8w0UQTTxhFjDtz8qNG+hOGExM5DM3MzWL2TGgZBlFPRAERcpTExOCGGySxzXHcKGLwpwdJYmfBpEHCfaJw3kHD/YkbzonCmS+igNKcGrgYmIvGLhgu5CiylcaOKKS070S2VuWIoulMttrEESnbZ5exfXYZ22eXoT679dtVc4tV1Ge3NEV9dutIqM+u6YT6fHGIu5HTnrynOKcYUFzjlgUtKL6l6FMMKS5Ic0PxjuI1RUkxIk1sNv0vHgsmsZwAdx3WIO0ZeQFvmVT20nSe+O9ici9jq659KMoKb55lt99W7dWyafdFzfCqP3vsG6ORCfPP8e/2f6Xb37TA/63/gNc/exmurkxA3wJ76jbFpmxqBrh2xKsJ/+Lu8YDm3jM=",
        },
    ],
}
