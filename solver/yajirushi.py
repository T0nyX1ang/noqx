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
            "data": "m=edit&p=7VVRb9MwEH7Pr0D3fA+xnaZu3rrR8jI2oJ2qyoqirGRqRauUtIHJVf4750ugWmsQQmOAhFJ//vL5XPu7k53dxzqvChSh+ymN1NMTCc1N6phb2D3T1X5dJC9wWO+XZUUE8WY8xvt8vSswMF1YGhzsILFDtK8SAwIQJDUBKdq3ycG+Tuwc7YSGAKMUYVOv96tFuS4rYE1Q3FU7URIdHemMxx27bEUREr/uONE50byqys/ZdXbRSm8SY6cIbvELnu4obMpPBXSbc++LcnO3csJdvieLu+VqC6hoYFe/Lz/U8HWJBu3wxIL+sQV1tKC+WVB+C/LEwuzpLQzSpqHyvCMTWWKcn9sj1Uc6SQ6gQkgiBNXjToTtq4jito+d3rjNHwgF45ym9SjO9PGkEBB/R6Z/Mb0zua9IVueyP1oPvPJAeZcUofSGi5CcGXGuy9AfL6U/XvmtCpdJjykR+XTK5phzKhmnVBe0ivElY8jYY7zimBHjjPGSMWKMOabvKvuTtfeUVTmzGqF8yEZd1vXjbc9+47aNam+mx0/v39PSwMCkru7zRUEHd7LMtwXQhdkE8ADcKKPShf2/Q//qO9SVKvzl0/RnDrehjCuB9gZhW2d5RtkG+lzjs+jyaXStz/RnzzJdR2nwBQ==",
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
