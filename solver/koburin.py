"""The Koburin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent, avoid_adjacent_color, count_adjacent
from noqx.rule.reachable import grid_color_connected


class KoburinSolver(Solver):
    """The Koburin solver."""

    name = "Koburin"
    category = "loop"
    examples = [
        {
            "data": "m=edit&p=7VZRb9pADH7nV1R+9kMud4SQl4l1ZS+MboOpqqIIBZaqUaFhgUzVIf57fb4wGE2qRpVoNU3hrC+fz8lnH7ay+lXEeYJCmJ/00UFCqNoeLyFcXk55jdP1PAnOsFesb7OcAOJlv4838XyVtMJyV9Ta6G6ge6g/ByEIQHBpCYhQfws2+kugh6hH5AJUxA3sJpfgxR5esd+gc0sKh/CwxASvCc7SfDZPJgPLfA1CPUYw7/nI0QbCIvudQKnD3M+yxTQ1xDReUzKr23RZelbFz+yuKPeKaIu6Z+UOKuTKvVwDrVyDKuSaLF4vd77MqoR2o+2WCv6dpE6C0Kj+sYf+Ho6CDdlhsAHp7XK0pwLKNcSHPeEpQ8gDonMUIhyOoYP9wwhxvEfIY8Z9EtXmJx8ynmMY54DxOerwOb7/1x5KTHB612z7bF22Y8oetWT7ia3Dts12wHsu2F6xPWer2Hq8p2Pq98IKgySpytb5NaJA+XRIXR+hI7sWqA4qyloiSLlDxHn0QstJOjT5wmxCSX1dcbX/XTZqhTAq8pt4llAbDdL75GyY5Yt4TnfDYjFN8t09za9tCx6AVyjNOPw/0k4+0kzxnUaD7e2nQKhHSJ2lLxGWxSSezDL6d1HVQqp32cA1TtvT9ZHU5vWR1PnVThoeVY46kcS3m/FeQ76uOMpXTR3dytSecXQc/z06qo/oOce7zKP5Cb5xHrXVPUXZm76cPgeeOE4+++izAe6LPL2LpwlErUc=",
        },
    ]

    def program(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="gray"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
        self.add_program_line(fill_path(color="white"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
        self.add_program_line(grid_color_connected(color="white", adj_type="loop"))
        self.add_program_line(single_loop(color="white"))

        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            self.add_program_line(f"gray({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(target=num, src_cell=(r, c), color="black", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"black({r}, {c}).")

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="grid_direction", size=3))

        return self.asp_program
