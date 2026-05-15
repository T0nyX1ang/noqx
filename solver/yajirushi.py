"""The Yajirushi solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, shade_cc
from noqx.rule.helper import fail_false, validate_direction


def yajirushi_pair(color: str) -> str:
    """Generate a rule to create Yajirushi pairs and constraints."""
    rule = "{ pair(R, C1, R, C2) } :- arrow_N_W__5(R, C1), arrow_N_W__1(R, C2), C2 > C1 + 1.\n"
    rule += f":- pair(R, C1, R, C2), grid_all(R, C), C1 < C, C < C2, not {color}(R, C).\n"
    rule += "{ pair(R1, C, R2, C) } :- arrow_N_W__7(R1, C), arrow_N_W__3(R2, C), R2 > R1 + 1.\n"
    rule += f":- pair(R1, C, R2, C), grid_all(R, C), R1 < R, R < R2, not {color}(R, C).\n"

    # every arrow symbol should belong to a pair
    rule += ":- arrow_N_W__1(R, C), not pair(_, _, R, C).\n"
    rule += ":- arrow_N_W__3(R, C), not pair(_, _, R, C).\n"
    rule += ":- arrow_N_W__5(R, C), not pair(R, C, _, _).\n"
    rule += ":- arrow_N_W__7(R, C), not pair(R, C, _, _).\n"

    # empty cells must be located between one or two pairs of arrows
    rule += f"between(R, C) :- pair(R, C1, R, C2), C1 < C, C < C2, grid(R, C), {color}(R, C).\n"
    rule += f"between(R, C) :- pair(R1, C, R2, C), R1 < R, R < R2, grid(R, C), {color}(R, C).\n"
    rule += f":- grid(R, C), {color}(R, C), not between(R, C)."

    return rule


class YajirushiSolver(Solver):
    """The Yajirushi solver."""

    name = "Yajirushi"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VZtb6pIFP7ur9jM106yDKhFkvtBrfa221pbNa4SQ9Ci0oLjItguxv/ecwYbeRmbm023d2+ywTkcnnM4c17gwc1fkR04lCn403QKZzjKTBdL1atiKYej74aeY/xG61G45AEolN6123RuexuHXo+WN01ef7mo/7nVw/GYXSrRlTJ8aj+dPfh/XLlawNodvXvbvXXVRf17s3FfbZ1Vu9FmEDrbe581ngbj/rw7XNTUv1udcTke3ymV6/H892198K1kHnKYlHZxzYjrNL40TMIIJSosRiY0vjd28a0Rj2jcAxOh5QklfuSF7ox7PCACY+B3k9yogto6qkNhR62ZgEwBvXPQQR2BagcBf7E6ViOBuoYZ9ynBzRvidlSJz7cO7obJ4fWM+1MXgakdQv82S3dNqAaGTfTIn6ODK5vsaVzPlaB/XAIEeS8B1aQE1CQlYGXpEoafX0Jtst/DeB6gCMswsZ7BUdWPas/YEU0hRpkSrSJOTEkuWbmanKuIg2vH2IFkQo7gtgr4mec0NwhSPQFDFLNSgM81gLUiLPfWa1K4hkGKWzJFlbozBSozWRFXMXWJv4pxJP7YONm+2ElJUawsw6GbbdFTVcg+zIXGmpAXQipCVoS8ET4tIYdCNoUsC1kVPuc42R+cvWSsGharU8Jfrdah63o2bfG4/ktpm1pCe9mj8uthk5JJelEwt2cOvLi9pb12CBAm2XDP2iS45bzas5AYCWenLRlsFflTBwgnBXmcrz13JYvwbsqA7mLFA0dqQtB5XJwKhSZJqCkPHnM5vdiel61FfM8y0MwNZl4WCgMgs9S1eMgyiG+HywyQIr5MJGeVa2ZoZ1O0n+3cbv6xHfsSeSViwbOu4gD//7r9p79uOCrlH/Pcz6FdEzquMRrfUbKOLNuCbhP4I0W/BFc/B9f1Av7lXRYvLw8+YNKjMQ9L+BTQDyg1ZZXhJ9gzZc3jBarEZItsCaiEMAHNcyZARdoEsMCcgJ0gT4ya50/MKk+huFWBRXGrNJGak9Ib",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_cc(colors=["ox_E__8", "arrow_N_W__1", "arrow_N_W__3", "arrow_N_W__5", "arrow_N_W__7"]))
        self.add_program_line(yajirushi_pair(color="ox_E__8"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name.startswith("arrow_N") and symbol_name.split("__")[1] in ["1", "3", "5", "7"]:
                self.add_program_line(f"{symbol_name.replace('B', 'W')}({r}, {c}).")

            if symbol_name == "ox_E__8":
                self.add_program_line(f"ox_E__8({r}, {c}).")

        self.add_program_line(display(item="arrow_N_W__1", size=2))
        self.add_program_line(display(item="arrow_N_W__3", size=2))
        self.add_program_line(display(item="arrow_N_W__5", size=2))
        self.add_program_line(display(item="arrow_N_W__7", size=2))
        self.add_program_line(display(item="ox_E__8", size=2))

        return self.program
