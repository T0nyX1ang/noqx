"""The Inaba's Island solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, invert_c, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import count_reachable_src, grid_color_connected, grid_src_color_connected


class InabasIslandSolver(Solver):
    """The Inaba's Island solver."""

    name = "Inaba's Island"
    category = "shade"
    aliases = ["inabasisland"]
    examples = [
        {
            "data": "m=edit&p=7VZLb9pAEL7zK6I9z2Fffl4qmoZeKGkLUYQsCxnqKFaNTA2uqkX8986OTYwRlpJD0hyqxaOZ+Wb3m9mxR2x/VUmZQoBL+cBB4FI+p8fX9sebNct2eRpewbDaPRYlKgC3oxE8JPk2hUHUhMWDvQlCMwTzOYyYYMAkPoLFYL6Fe/MlNBMwU4QY6BjYusp32arIi5KRT2DcuN4oUb1p1XvCrXZdOwVHfVLrLqpzVFdZucrTxbg+6GsYmRkwy/2RdluVrYvfKWtys/aqWC8z61gmO6xw+5htGCgEttWP4mfVhIr4AGZYVzB9ZgWqrUA9VaBes4J8U1zIPYgPB2zLd8x+EUa2kLtW9Vt1Gu4PNqE90xK3SnDrzjGt0RSt6XZNv2O61lRPpsc7qNc92dOd4EB30KBLFHRPFtwe7bW2sDb7wFqPtB73xLbsgp84dPcI6Z5Q4GUIupI5yRFJSXKGNwZGkfxEkpN0SI4p5obkPclrkpqkSzGevfNndgXz8lioMSmNBcm6SW+QXSR9Gginy3lfnngQsWlVPiSrFL+GSbVepuXVpCjXSc5wFh0G7A+jB7sqbfj/8fQux5NtEX/RkPr3X2eEV41DB8wtsE21SBZ4z/QOXAaUBeZ9wOQCwPt2iIZD95FL7xIHAo46A3TfUU7fDvfI4ZwBXgPgH4ku4B+B4AwIjhzyvEDeRyJEH4uQfTRC9fL0li+c+M1fN5y48eAv",
        },
        {"url": "https://pzplus.tck.mn/p.html?island/4/5/k0i6i0j6g", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(defined("clue"))
        self.add_program_line(invert_c(color="clue", invert="clueless"))
        self.add_program_line(shade_c(color="black", _from="clueless"))
        self.add_program_line(invert_c(color="black", invert="white", _from="clueless"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not white", grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"clue({r}, {c}).")

            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color="black"))
                self.add_program_line(count_reachable_src(num + 1, (r, c), color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
