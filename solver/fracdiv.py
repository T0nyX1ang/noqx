"""The Fractional Division solver."""

from typing import Dict, Optional, Set, Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


class SimpleFraction:
    """A simple class to represent a fraction."""

    def __init__(self, numerator: Optional[int] = None, denominator: Optional[int] = None):
        self.numerator = numerator
        self.denominator = denominator


class FractionalDivisionSolver(Solver):
    """The Fractional Division solver."""

    name = "Fractional Division"
    category = "region"
    aliases = ["fractionaldivision"]
    examples = [
        {
            "data": "m=edit&p=7VRLb9pAEL7zK6I5z2EfNmDfSAq9UNKWVBGyLGTALVaNTA2uokX8986ObYxp1NKHoh6qsUfz+HZ3Xru7L0WUx+gS6T4KlERK9fl3hP1qekj2aezf4KDYr7OcBMT70Qg/Rukuxk5QwcLOwXi+GaB57QegAPmXEKJ55x/MG9/M0EzJBShDhE2R7pNllmY51DYzJkkCKhKHjfjIfivdlUYpSJ5UMokzElfJMi61t35gHhDsube80oqwyb7GUC5hfZltFok1LKI9ZbdbJ1tATY5dsco+F1DvfkQzKKMfXhm9bqLXp+j189GrKvplki/TeD7++xl44fFIjXlPOcz9wKbzoRH7jTj1D0cb1gGUVydfdg/crjWI2kAwSTBHOKciIWk9KLvOmuy2NO8cqURL01ZzS83tipbGPl21YWZjs/4uQvY0vy1BSpIlkChaZD2niQA+o73KubToah9L1R6WWvtorz6rwVye5chzjHwew/uIC4xoYVxZY8TZeReY3hUY7zJTrvEPK0bFHvE4KOYPNCFoNPNXzAVzl/mYMUPmj8zvmDvMu4zp2Rn7pSksh6zs+u+FA8qOj9enmRWUnqB66p+GGKiq70TudVLYCWC4+hTfTLJ8E6V0OSfFZhHnjT5dR9sY6Hk8duAJ+A80qv8v5j/8YtomiRee2D+9QAEV/DTsaO4RtsU8mlPNwT4K1k134jvHi2dB1yzsfAM=",
        },
        {
            "data": "m=edit&p=7VXfb5swEH7nr6j8fA/Y5vfLlHbJXrp0W1JVFUIVSdiCBqIjYaoc8b/vfEBJ0kmwaZsmbbJ8+u78Hf4wd3j3pYrLBDwc0gMTOA5pCZrC9Gma7Vim+ywJLmBS7bdFiQDgZjaDj3G2S8AIW1pkHJQfqAmoN0HIBAOanEWg3gcH9TZQ96AWuMSAR8DyKtun6yIrStbF1DUizkAgnPbwjtY1umqC3EQ8bzHCe4SbdJ003rsgVEtget9LytSQ5cXXhDUp5K+LfJXqwCre49vttukjA4kLu2pTfK5Y9/Qa1KRRPx2pXvbq5bN6+X31olVfPD1c/nr1flTX+FE+oP6HINSvcttDr4eL4FBrSQdmc536CqXQl8Mox6hrms/nAehJ7dmdZ52sudpzW0942pOtJ+nh3OpccZwo7eNEyztea1R1G9onefZJnuscb+j6/Ya1PugDIw0O9AfOSMZpxHsR8c8jlnwRsc4jtnkecbTYrl/wjLvOgb58meMMc1x3BMcb5vhiBEeO4PjDHE5FNEiyxpBGHCPnfAxp8ACwbmbUHoLsEjsGlCT7mqxJ1iZ7TZwp2TuyV2Qtsg5xXN1zP9SVTRc2Bfyb5ITCoRugH/af9SMjZNPNp+RiXpR5nOFvbl7lq6Ts/cU2fkwYXjK1wZ4YzVCC+H/v/KX3jv5A5k/XOf1g1c2/0X1Y0mFkfAM=",  # a little bit slow
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))

        for (r, c, _, _), symbol_name in puzzle.symbol.items():
            symbol, tag = symbol_name.split("__")
            if symbol == "dice":
                dice_cnt = bin(int(tag)).count("1")
                self.add_program_line(f"number({r}, {c}, {dice_cnt}).")

        all_src: Set[Tuple[int, int]] = {(r, c) for (r, c, _, _) in puzzle.text}
        frac_dict: Dict[Tuple[int, int], SimpleFraction] = {}

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)

            if (r, c) not in frac_dict:
                current_excluded = [src for src in all_src if src != (r, c)]
                self.add_program_line(
                    grid_src_color_connected((r, c), exclude_cells=current_excluded, color=None, adj_type="edge")
                )
                frac_dict[(r, c)] = SimpleFraction()

            if label == "normal" and isinstance(num, int):
                frac_dict[(r, c)].numerator = num
                frac_dict[(r, c)].denominator = 1

            if label == f"corner_{Direction.TOP_LEFT}" and isinstance(num, int):
                frac_dict[(r, c)].numerator = num

            if label == f"corner_{Direction.BOTTOM_RIGHT}" and isinstance(num, int):
                frac_dict[(r, c)].denominator = num

        for (r, c), frac in frac_dict.items():
            if frac.numerator is not None and frac.denominator is not None:
                tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
                region_cnt = f"#count {{ (R, C): {tag}({r}, {c}, R, C) }}"
                total_dice = f"#sum {{ N, R, C: {tag}({r}, {c}, R, C), number(R, C, N) }}"
                self.add_program_line(
                    f":- N1 = {total_dice}, N2 = {region_cnt}, N2 * {frac.numerator} != N1 * {frac.denominator}."
                )

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
