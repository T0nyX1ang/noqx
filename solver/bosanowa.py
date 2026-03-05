"""The Bosanowa solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_num, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent


def bosanowa_constraint(adj_type: int = 4) -> str:
    """Generate bosanowa constraints."""
    return f":- number(R, C, N), N != #sum {{ |N - N1|, R1, C1: number(R1, C1, N1), adj_{adj_type}(R, C, R1, C1) }}."


class BosanowaSolver(Solver):
    """The Bosanowa solver."""

    name = "Bosanowa"
    category = "num"
    aliases = ["bossanowa"]
    examples = [
        {
            "data": "m=edit&p=7VVNb5wwEL3zKyKf54A/sIHbNs32st203a2iCqEVS4myKitSdqkqr/jvHXtISFGj5pKkh8rym/HzjP38gTl874q2ghgMyBhC4FikEiBDBUpzX8OhrHfHukrPYNYdb5oWHYDL+Ryui/pQBdkQlQcnm6R2BvZdmjHOgAmsnOVgP6Yn+z61S7Ar7GKgkFtQkED3YnSvfL/zzonkIfrLwUf3C7rlri3rarMg5kOa2TUwN88bn+1ctm9+VGzQ4dpls9/uHLEtjriYw83udug5dF+bbx27m6IHO3tcrhzlynu58s9yxfPLTfK+x23/hII3aea0fx7deHRX6YkJzVKFh2LIxGQSb2RIRpCRZChEUoiiEKXIRN5EREZERjRDRDNoSteUbijEUJ6hkJiTobyEWgnlJZTHQzFYJ6p3m3tikrv1S9xQumBMCUeoB4R0hB6JyKeIB4SYEDqajKH1ZAyjJykmcYQZiTicjBHHk5Q4mRCJnKyFh/zuMt4z6rcY3AWennp3uxzOPQqPazxvsNLjW4+hx8jjwsdceLzyeO5RedQ+xrgb88Q7RcfxAnIyof0DNZboedt5kLFV114XZYXf3bLbb6v2bNm0+6Jm+ND1AfvJfM0khqv/b98rvX3uCMJ/7bb+RU5mV2AM2Etgt92m2JRNzfD3CY/wL64eP7c8+AU=",
            "config": {"max_number": 10},
        },
        {
            "data": "m=edit&p=7VRNb9swDL3nVxQ66yBKsiP7lnXNLln2kRTFYARFkrlosATZnHgYHPi/jyLpOeh26KVbDoMgPop8kp4lWodv9bIqddBgtAvaaMDmvNUegrY+oW6kzTfHbZlf6VF9fNxX6Gj9bjzWD8vtoRwUwloMTk2WNyPdvMkLBUorix3UQjcf8lPzNm+muplhSmmPsQmTLLo3vXtH+ehdcxAM+lPx0f2E7npTrbfl/YQj7/OimWsV93lFs6OrdvvvpRIdcbze71abGFgtj/gxh8fNV8kc6s/7L7Xqtmh1M3oiF3q5rpfrfsl1f5ZrX15utmhbPPaPKPg+L6L2294NvTvLT8qmKvd4KUOGwJAROMNgGRwDUxxTEqYkwJAw8JopM4eeQUY8L/C8wPMC5zIeZbxfxvuBMYLd2AvyZgBWUPIgeejyqSB/IljhWeFZ4clJgO14QZAVgxOeE54TnhwIyImAF70+fk0b7/2kYgyvxuBlc/GrmMWI6yOpo0h6FvG/cdKn66RZjJxRwjAGQh8AQ1udrQvOd4VNERQJ+amNdRntmKwlO8dK0Y0j+5qsIZuQnRDnhuwd2WuynmxKnGGstWdWI5/WX5BT2JSetr4llzVeDAo1q6uH5brEP3xa71ZldTXdV7vlVuGT2g7UD0W9cEj3/1/Zf/TKxiswl1bdlyYH/7fF4Cc=",
            "config": {"max_number": 25},
            "test": False,
        },
    ]
    parameters = {"max_number": {"name": "Max number", "type": "number", "default": 20}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        lmt_num = int(puzzle.param["max_number"])
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(fill_num(_range=range(1, lmt_num + 1)))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(bosanowa_constraint())

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
