"""The Kurodoko solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)


class KurodokoSolver(Solver):
    """The Kurodoko solver."""

    name = "Kurodoko"
    category = "shade"
    aliases = ["kuromasu"]
    examples = [
        {
            "data": "m=edit&p=7VXBjpswEL3zFdGc54BtcIBbut30kmbbJtVqhVBEKKuNSkRKQlU54t87HiiU7B7aQ1OpqsCj92bG+HksD8cvdVrlKIR9VYAuEkLP1zyEkDzc7lnvTkUeTXBWn57KigDi3XyOj2lxzJ24y0qcswkjM0PzJopBAIKkISBB8z46m7eRWaJZUQjQI9+iTZIEbwd4z3GLblqncAkvW6wJPhDMdlVW5JsFRcnzLorNGsGu84pnWwj78msOnQ7Ls3K/3VnHNj3RZo5Pu0MXOdafys91lyuSBs2slbv6IVcOctUgV/Vy1Z+UWxzKl4SGSdNQwT+Q1E0UW9UfBxgMcBWdG6voDErSVOGibg8FvMB+agK9w7cJcqA+Ub+n2htFtZ2tehq4Y2qTvZ6GekSFG4y5kKOlhLD5euAyGHPPveB2uenAfT3m2r3YqtDheMWpVRD8xPWYhzYedpwKKrisD2znbCXbNVUdjWL7mq3L1me74Jxbtvdsb9h6bDXnTO25/eLJglIQSQRF+/faY76CtlhJ7haXj//vehMnhlVdPaZZTpdxWe+3eTVZltU+LYD6XuPAN+BBd4Da6P9WePVWaIvv/lZD/Pu3OKa6Kg/NHcKh3qSbrCyA/qPIfvXMf3X1dNUT5zs=",
        },
        {"url": "https://puzz.link/p?kurodoko/9/9/h3j4g3j4l.j4g3j.ldl.j5g6j.l7j5g6j5h", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_color_adjacent(color="black"))
        self.add_program_line(grid_color_connected(color="not black"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="not black"))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
