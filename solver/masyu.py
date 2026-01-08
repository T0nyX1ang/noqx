"""The Masyu solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_straight, route_turning, single_route


def masyu_black_clue_rule() -> str:
    """Generate a rule for black_clue masyu."""
    black_clue_rule = ":- grid(R, C), black_clue(R, C), not route_turning(R, C).\n"
    black_clue_rule += (
        ":- grid(R, C), black_clue(R, C), route_turning(R, C), adj_line(R, C, R1, C1), not route_straight(R1, C1).\n"
    )
    return black_clue_rule


def masyu_white_clue_rule() -> str:
    """Generate a rule for white_clue masyu rule."""
    white_clue_rule = ":- grid(R, C), white_clue(R, C), not route_straight(R, C).\n"
    white_clue_rule += (
        ":- grid(R, C), white_clue(R, C), route_straight(R, C), { route_turning(R1, C1): adj_line(R, C, R1, C1) } = 0.\n"
    )
    return white_clue_rule


class MasyuSolver(Solver):
    """The Masyu solver."""

    name = "Masyu"
    category = "route"
    aliases = ["mashu"]
    examples = [
        {
            "data": "m=edit&p=7VVNb9pAEL37V0R7nsOO1xjbN5qGXlzSllQRsizkUFdYNTXFuEoX8d8zO7ZKqkykfgmpUmV2eLxZ8JvHzLr90hW7ElC7l4mA3ukKMOLlRyEvPVw31b4ukwuYdPt1syMAcD2dwseibksvG3bl3sHGiZ2AfZVkylfAC1UO9m1ysK8TuwA7p5QCJC4lhAp8glcneMt5hy57EjXh2YAJLgiuqt2qLpdpz7xJMnsDyt3nBX/bQbVpvpaq/xp/XjWbu8oRd8WeimnX1XbItN2H5lM37MX8CHbSy00FueYk18FerkOCXFfFH8utq8/lvaQ0zo9HcvwdaV0mmZP9/gSjE5wnB4ozjshxkRxUMKafQbrPY20qiCR2hCLri2wssaER2UBixyORDUVWvFukRVasOBIrjsWKY7Fi1GJxqMXqUIsyUIs6EEUzEEU3EEU70Bf9QCMWiUau0jjd/hM6kIsP5OLlrkOp7ahPp9ytPscbamawhuNLjprjiGPKe6443nK85BhwDHnP2I3Dbw/Mr8qhoSEL4oh6FMl+B9A3wDYaZ2f4CI8I0z/qsI6B9hH+yXoy05/cP170g/8al3uZSumsu5g1u01R04k3XxfbUtFT5eipe8UrIwch+P+gOf+DxrmvzzY9f2eYMzL2+9SBvQa17ZbFctVQd5F7fXoYxGfT/Ww+lx7GVU7T5MsJOhueJM7uHZ0dalO03zqVew8=",
        },
        {
            "url": "https://puzz.link/p?masyu/21/15/000a0l2943300030l00200i10j0063c60091000670303010606j3600133013ia16l0110000600306b2063000300020960ai301030",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black_clue"))
        self.add_program_line(defined(item="white_clue"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_straight(color="white"))
        self.add_program_line(route_turning(color="white"))
        self.add_program_line(masyu_black_clue_rule())
        self.add_program_line(masyu_white_clue_rule())

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            self.add_program_line(f"white({r}, {c}).")
            if symbol_name == "circle_L__1":
                self.add_program_line(f"white_clue({r}, {c}).")
            if symbol_name == "circle_L__2":
                self.add_program_line(f"black_clue({r}, {c}).")

        for (r, c, d, _), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
