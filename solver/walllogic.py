"""The Wall Logic solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, bulb_src_color_connected, count_reachable_src


class WallLogicSolver(Solver):
    """The Wall Logic  solver."""

    name = "Wall Logic "
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VZfT9tIEH/Pp6j2tSudd9d2bEunU6BJrz0IoQVxJIoiJxgwdWLOsaFnxHfvzISwu07grkXq3QNyMpr5zez82/V4l39VcZFw0cafCrjDBTx+4NJfSof+6+coLbMkesM7VXmZF8BwftDr8fM4Wyb84+nl3m7euX3X+fMmKIdD8d6pPjgnV72rt5/mf3xIVSF6/WCwP9hP5UXn992dQ7/71h9Uy+MyuTmci52r4+HR+eDkIpR/d/tDtx4eON7H4fkvN53jX1ujhxzGrbs6jOoOr99HIyYZp79gY14fRnf1flT3ef0ZVIyLMWfzKivTWZ7lBVtj9R5wgnEJbFezJ6RHbncFCgf4/gMP7Cmws7SYZclkb4UMolF9xBnG3qHVyLJ5fpNgMFhG8iyfT1MEpnEJ7VtepteMK1Asq7P8S/VgKsb3vO6sKuj+ywrAyboCZFcVILelAizs5RVk1/mW3MPx/T1syyfIfhKNsJBjzQaa/RzdAe1Hd8x1YakLJ412jnkOiEqLqPUeRR+12rhtG7d9EP1HMUCR/QblrYEQAPkohnbkELV6tXCk5VwIlA29CGy9xPXanVAYXqcuXAUyvlIPsiesbITn2fYe+jP8+7je0LcxfUMfYH5G/BD9CyNAiAnrAqRjN1M6bZADLQs7oBQYUPuT1ABdkJSYgCnbDZAS/euEJTXIyEeh3rB3sSGGvYv2hkwNMuL5GD80ZFxv6NuN+EGjfjovhj0dF0NPB0TXr6h/2l452C/tXzl2fOVgv8z1DX/UT90PJRvrlb3Bit4c3S/l2gdSUT+M9b69H8pHe8Nfu+E/sPuvgoY9HbD1eYG3WdA7fUq0R1QSPYJXnteK6DuiDlGP6B7ZdImeEN0l6hL1yaaNQ+O7xsrL08EXGA5MGOBM8rjnQPfUP+Y4crFBzz+4Ba8WrxZPPOPWiHXPLpI3/byYxxl8ePvVfJoUaxmuPWyZZ5NlVZzHs2SSfI1nJYtWNy9TY2EL8mFBWZ5fZ+lim4e1ygLTi0VeJFtVCCaQ8xOuULXF1TQvzho53cZZZtdCt1ILWt1bLKgs4FJiyHFR5LcWMo/LSwswrmCWp2TRaGYZ2ynGX+JGtLlux32LfWX0h8kpX++o/9s7Km6R85M/KS/9wo2g1fhV4vUBZ9fVJJ5AoxkcMv6jmsdP23+gDkH7nen+wJKnk/jpm0uzIi+eGdxa2YS3jG9An5nghnYb/sSwNrRNfGMyY7KbwxnQLfMZ0OaIBmhzSgO4MagBe2JWo9fmuMasmhMbQ20MbQxlzu0RW1RF+iWeJmzc+gY=",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num + 1, (r, c), main_type="bulb", color=None, adj_type="edge"))

        tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
        self.add_program_line(f":- adj_edge(R, C, R1, C1), {tag}(R0, C0, R, C), not {tag}(R0, C0, R1, C1).")
        self.add_program_line(avoid_unknown_src(color=None, main_type="bulb", adj_type="edge"))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
