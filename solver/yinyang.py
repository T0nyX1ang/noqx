"""The Yin-Yang solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, grid, invert_c, shade_c
from noqx.rule.helper import validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_checkerboard, avoid_rect


def exclude_border_color_changes(rows: int, cols: int) -> str:
    """Exclude border color changes more than twice."""
    rule = ""
    for r in range(rows - 1):
        rev_r = rows - 1 - r
        rule += f"changed({r}, 0) :- circle_M__1({r}, 0), circle_M__2({r + 1}, 0).\n"
        rule += f"changed({r}, 0) :- circle_M__2({r}, 0), circle_M__1({r + 1}, 0).\n"
        rule += f"changed({rev_r}, {cols - 1}) :- circle_M__1({rev_r}, {cols - 1}), circle_M__2({rev_r - 1}, {cols - 1}).\n"
        rule += f"changed({rev_r}, {cols - 1}) :- circle_M__2({rev_r}, {cols - 1}), circle_M__1({rev_r - 1}, {cols - 1}).\n"

    for c in range(cols - 1):
        rev_c = cols - 1 - c
        rule += f"changed(0, {c}) :- circle_M__1(0, {c}), circle_M__2(0, {c + 1}).\n"
        rule += f"changed(0, {c}) :- circle_M__2(0, {c}), circle_M__1(0, {c + 1}).\n"
        rule += f"changed({rows - 1}, {rev_c}) :- circle_M__1({rows - 1}, {rev_c}), circle_M__2({rows - 1}, {rev_c - 1}).\n"
        rule += f"changed({rows - 1}, {rev_c}) :- circle_M__2({rows - 1}, {rev_c}), circle_M__1({rows - 1}, {rev_c - 1}).\n"

    rule += ":- { changed(R, C) } > 2.\n"
    return rule


class YinyangSolver(Solver):
    """The Yin-Yang solver."""

    name = "Yin-Yang"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZVPb9NAEMXv/hRoznPw7Hode28hNFzSQmmqqLKsqg1GjUhkmj9QbeTvzuzEJSqMhIRAVAg5+/TydjL7i722N/e7m3WDRPFjC0yRHWYul0FkZKT9MV1sl41/gcPd9q5ds0F8Mx7jh5vlpkmqvqpO9qH0YYjhta+AAMHwIKgxnPt9OPUwb1e3C8BwwfOAxBOTQ6Vhe3K0M5mPbnQIKWV/1nu2V2zni/V82VxPDslbX4UpQlzspfw6Wli1nxvoYeL3AwAHt8svd3222b1vP+7gsXmHYfgTWnuktd9orU5rntKe/lbasu46PunvmPfaVxH98miLo73w+y4SRSXRK78HO+A2Bp+igTNqmmtpnqmp2jcvtbRI1VRdrVQ7UKouR2mhx3oTIj1WTwaR02MVm0gHNLGafoitDphZtTrTl3Q6oNNJXKn2Huh/fuDU6kLpzRttLNvNiE55N2Kwoq9EU1EnOpGaE9GZ6Eg0E82lZhD38y/v+D+EU1kjD8/vD/fvpnVSwahdfWo3i20D/ODvEngAGZWN75H/74K/8i6IFyB9bvfHc8PhO7ZOvgI=",
        },
        {
            "url": "https://puzz.link/p?yinyang/22/18/00000000000000030190030000900003000000900130020006000l0000090000i0020009400030200060000002empf01900001009901030130900031009a00009000",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="circle_M__1"))
        self.add_program_line(invert_c(color="circle_M__1", invert="circle_M__2"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_rect(2, 2, color="circle_M__1"))
        self.add_program_line(avoid_rect(2, 2, color="circle_M__2"))
        self.add_program_line(grid_color_connected(color="circle_M__1", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(grid_color_connected(color="circle_M__2", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_checkerboard(color="circle_M__1"))
        self.add_program_line(exclude_border_color_changes(puzzle.row, puzzle.col))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__1":
                self.add_program_line(f"circle_M__1({r}, {c}).")
            else:
                self.add_program_line(f"not circle_M__1({r}, {c}).")

        self.add_program_line(display(item="circle_M__1"))
        self.add_program_line(display(item="circle_M__2"))

        return self.program
