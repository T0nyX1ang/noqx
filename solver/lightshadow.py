"""The Light and Shadow solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Point, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected


class LightShadowSolver(Solver):
    """The Light and Shadow solver."""

    name = "Light and Shadow"
    category = "shade"
    aliases = ["lightandshadow"]
    examples = [
        {
            "data": "m=edit&p=7Vbfb5swEH7PX1H52Q/+BQZepqxr9pKl25KqqiwUJRlVoxGRkTJNRPzvO5/dkXqJ1kpTnirE3fH54/zdYQO7H82iLijnlCsqE8ooRFRFMY00o3Gs8WT+mK0fyyK7oMPm8aGqIaD0ejSi94tyVwyMZ+WDfZtm7ZC2HzNDOKFEwMlJTtsv2b79lLUT2k5hiFAF2NiRBIRXfXiL4za6dCBnEE9cbG+7g3C1rldlMR/DKCCfM9POKLHzvMe7bUg21c+CeB32elVtlmsLLBePUMzuYb31I7vmW/W98Vyed7QdOrnTI3JlL1f+kSuPyxX/RW65rY4JTfOug4Z/BanzzFjVN32Y9OE02xOZkExREkfoNHcuRZe4K86F80I6rzyunq6185p5r5xPPS916QRzkwhp83W2FzC/tqJTqN+tBxTknqgHYmUB2TOsVmCwnmInNiTpKbYOQ6IDRhIksSUa8q5nJMwDT4wkzME5InFPwc4Yog44AhFxwLFdM0QfcBQL8ygeqOFKBHKw23hXz4m9wp6jQ81xGhTONQvn0jKcS6twrjRsDz7d57WniUd6TthlwVSQB1fFszxC8qAuXDHYVceBtcOzfWe3kLUjtALtDJY2bSXaD2gZ2gjtGDlXaG/RXqJVaGPkaLs5Xrx93NZQULlwK/oM2owU+EoOj+gNPY3mA0OmTX2/WBXwzpw0m2VRX0yqerMoCXyeugH5RfA0Eujq7Yt19i+WbT574cY72177hxwDfZWatteUbJv5Yr6qSgK/O/Q0fvdKHPKIE7h8Ha6Sv/CzdxNeXvngNw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(avoid_unknown_src(color="black"))
        self.add_program_line(avoid_unknown_src(color="not black"))

        all_src: List[Tuple[int, int]] = []
        for (r, c, d, label), _ in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            all_src.append((r, c))

        for (r, c, _, _), num in puzzle.text.items():
            current_excluded = [src for src in all_src if src != (r, c)]
            color = "black" if puzzle.surface.get(Point(r, c)) == Color.BLACK else "not black"
            self.add_program_line(f"{color}({r}, {c}).")
            self.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color=color))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num, (r, c), color=color))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
