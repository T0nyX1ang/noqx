"""The Box solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type


def count_box_col(target: int, c: int, color: str = "black") -> str:
    """Generate a rule to count the number of 'boxes' in each column."""
    return f":- #sum {{ N, R: box_col(R, N), {color}(R, {c}) }} != {target}."


def count_box_row(target: int, r: int, color: str = "black") -> str:
    """Generate a rule to count the number of 'boxes' in each column."""
    return f":- #sum {{ N, C: box_row(C, N), {color}({r}, C) }} != {target}."


class BoxSolver(Solver):
    """The Box solver."""

    name = "Box"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVBj5s8EL3zK1Y+zwFjA4Zbut30kma/r0m1WiEUEcpqoxKxJaGqHOW/73gMwS09tIfu9lARj14eb5w3Hts5fOmKtgLOzUco8AERyDCiwXlAw++f9e5YV+kVzLrjY9MiALidz+GhqA+Vl5lMfHLvpJNUz0C/SzPGGbAAB2c56P/Tk36f6iXoFb5iIJBbWFGA8GaEd/TeoGtLch/xsscI7xGWu7asq83CMv+lmV4DM7/zhrINZPvma8V6H+Z72ey3O0NsiyMWc3jcPfVvDt2n5nPXa3l+Bj2zdleDXTnaNc57uwZauwb9xK6p4g/bTfLzGZf9AxrepJnx/nGEaoSr9IRxmZ6YEJQaohnbHCakYQLhMKFhhO8w0UQTTxhFjDtz8qNG+hOGExM5DM3MzWL2TGgZBlFPRAERcpTExOCGGySxzXHcKGLwpwdJYmfBpEHCfaJw3kHD/YkbzonCmS+igNKcGrgYmIvGLhgu5CiylcaOKKS070S2VuWIoulMttrEESnbZ5exfXYZ22eXoT679dtVc4tV1Ge3NEV9dutIqM+u6YT6fHGIu5HTnrynOKcYUFzjlgUtKL6l6FMMKS5Ic0PxjuI1RUkxIk1sNv0vHgsmsZwAdx3WIO0ZeQFvmVT20nSe+O9ici9jq659KMoKb55lt99W7dWyafdFzfCqP3vsG6ORCfPP8e/2f6Xb37TA/63/gNc/exmurkxA3wJ76jbFpmxqBrh2xKsJ/+Lu8YDm3jM=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            num = int(num)

            if r == -1 and 0 <= c < puzzle.col:
                self.add_program_line(count_box_col(num, c, color="black"))

            if r == puzzle.row and 0 <= c < puzzle.col:
                self.add_program_line(f"box_row({c}, {num}).")

            if c == -1 and 0 <= r < puzzle.row:
                self.add_program_line(count_box_row(num, r, color="black"))

            if c == puzzle.col and 0 <= r < puzzle.row:
                self.add_program_line(f"box_col({r}, {num}).")

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"black({r}, {c}).")
            else:
                self.add_program_line(f"not black({r}, {c}).")

        self.add_program_line(display())

        return self.program
