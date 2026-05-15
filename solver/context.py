"""The Context solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected


class ContextSolver(Solver):
    """The Context solver."""

    name = "Context"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVNj5swEL3zK1Y+zwHbEAy3dLvpJc22JdUKIRQRymqjEpGSUFWO+O8dD3SzTlOpSFWqSpXjybznr8eMGfZf2rwpgbvmJxXgPzaPK+pCTai7Q1tuDlUZ3cC0PTzVDToA97MZPObVvnTSYVbmHHUY6SnoN1HKOAMmsHOWgX4fHfXbSC9AxzjEQCE37ycJdO9O7gONG++2J7mL/mLw0U3QLTZNUZWrec+8i1K9BGbOeUWrjcu29deSDToMLurtemOIdX7Ah9k/bXbDyL79VH9u2Y8jOtDTXm58Qa48yZXPcuVlueKPyK129SWhYdZ1GPAPKHUVpUb1x5OrTm4cHTuj6Mikh0tNliknTE4Qimfo+Ta0R31hwUDa0N45CBDKE1QWVNyarAJrK6UsGHJrbSgsyN3Q2otzWwgXysbSPcPS3o9C9BLbUeBecIZttdw/298/O99/qRfTwik5CdkZWUF2ibkDLcm+JuuS9cnOac4d2Qeyt2Q9shOaE5js/+b9YCYsCnOOTy/6y3IFbansa47d/H+Py5yUxW3zmBclvqiLdrsum5tF3WzzimFN7Bz2jVGnm+X9L5NXL5Mm+O6oYvn3380U4zoRoO+B7dpVvirqiuE3Fn7NJyP5GIJgDJ+M5GPw1Bg+GcnHgBXk8v7eT/zVs4sFLnO+Aw==",
        },
        {
            "url": "https://puzz.link/p?context/16/12/g1k12g2010k3q2h323i2p3i222i3h21l2i333l2m3j3m0l333i1l11h3i121i3p1i323h0q3k2121g20k1g",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(avoid_same_color_adjacent(color="gray", adj_type=4))
        self.add_program_line(grid_color_connected(color="not gray", adj_type=4, grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f":- not gray({r}, {c}), #count {{ R, C: adj_4({r}, {c}, R, C), gray(R, C) }} != {num}.")
            self.add_program_line(f":- gray({r}, {c}), #count {{ R, C: adj_x({r}, {c}, R, C), gray(R, C) }} != {num}.")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
