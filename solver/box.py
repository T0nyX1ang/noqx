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
            "data": "m=edit&p=7VVBb5swFL7nV1Q++8CzDRhuWdfskqXbkqqqEIpIRtVoiehImCZH+e97fiY1gx66w9odJvDT4/Nn830P2+y/N0VdcgB7S80DjhlXYUQNQFAL2muxOWzL9IKPm8NDVWPC+fVkwu+L7b4cZUBjIR8dTZKaMTcf0owB40xgA5Zz8zk9mo+pmXEzxy7GJWJTRxKYXvn0lvptdulACDCftTmmd5iuN/V6Wy6nDvmUZmbBmX3POxptU7arfpSs1WGf19VutbHAqjigmf3D5rHt2Tdfq28NO7/ixM3YyZ2f5SovV3q58kmufF6u+Ptyk/x0wrJ/QcHLNLPab3yqfTpPjyer68ikpKEhinEfh0llESE7SGgRGXSQaMCJB4gmpDtz0ueoYIAAIVEHoZkBPBLGrd2oBSJBgPKUmBDhKXHc96kJkZ6SuFmEp0BAkPIcCAZqAAgKOyRBwzoeQJ6RJ44rmOySnNO4QwrFgOS86g4pGs7k3CYdkpa9moFWvRKBDnsVAR31/euBWa371nTS95EEfdEJ/KYQVyPQmryjOKEoKC5wyXIjKb6nGFAMKU6Jc0XxluIlRUUxIk5sF/0LtwVTaEfgqkMPyu2RV9CWKc2hd8X/FpKPMjZv6vtiXeLJM2t2q7K+mFX1rtgyPOpPI/aTUcuk/XP8P/3f6PS3nyD4o3/A2++9DKurEm6uOXtslsVyXW0Zx9oRrgf4q6vHDZqPfgE=",
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
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
