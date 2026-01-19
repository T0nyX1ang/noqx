"""The Koburin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route


class KoburinSolver(Solver):
    """The Koburin solver."""

    name = "Koburin"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VZRb9pADH7nV1R+9kMud4SQl4l1ZS+MboOpqqIIBZaqUaFhgUzVIf57fb4wGE2qRpVoNU3hrC+fz8lnH7ay+lXEeYJCmJ/00UFCqNoeLyFcXk55jdP1PAnOsFesb7OcAOJlv4838XyVtMJyV9Ta6G6ge6g/ByEIQHBpCYhQfws2+kugh6hH5AJUxA3sJpfgxR5esd+gc0sKh/CwxASvCc7SfDZPJgPLfA1CPUYw7/nI0QbCIvudQKnD3M+yxTQ1xDReUzKr23RZelbFz+yuKPeKaIu6Z+UOKuTKvVwDrVyDKuSaLF4vd77MqoR2o+2WCv6dpE6C0Kj+sYf+Ho6CDdlhsAHp7XK0pwLKNcSHPeEpQ8gDonMUIhyOoYP9wwhxvEfIY8Z9EtXmJx8ynmMY54DxOerwOb7/1x5KTHB612z7bF22Y8oetWT7ia3Dts12wHsu2F6xPWer2Hq8p2Pq98IKgySpytb5NaJA+XRIXR+hI7sWqA4qyloiSLlDxHn0QstJOjT5wmxCSX1dcbX/XTZqhTAq8pt4llAbDdL75GyY5Yt4TnfDYjFN8t09za9tCx6AVyjNOPw/0k4+0kzxnUaD7e2nQKhHSJ2lLxGWxSSezDL6d1HVQqp32cA1TtvT9ZHU5vWR1PnVThoeVY46kcS3m/FeQ76uOMpXTR3dytSecXQc/z06qo/oOce7zKP5Cb5xHrXVPUXZm76cPgeeOE4+++izAe6LPL2LpwlErUc=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(fill_line(color="not black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))
        self.add_program_line(grid_color_connected(color="not black", adj_type="line"))
        self.add_program_line(single_route(color="not black"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"hole({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(target=num, src_cell=(r, c), color="black", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"black({r}, {c}).")

        for (r, c, d, _), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
