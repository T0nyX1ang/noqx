"""The Kurodoko solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
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
            "data": "m=edit&p=7VXBjtowEL3zFWjOc4jjxBDf6HbphbJtoVqtogiFNKtFGxQaSFUZ8e87M0lJUPfQHkqlqgp+em9mHL+MZbP/WqdVjkrxT4/RQ2IYhEaGUr4Mr32Wm0OR2yFO6sNTWRFBvJtO8TEt9vkgbquSwdFF1k3QvbMxKEDwaShI0H20R/feujm6BaUAA4rNmiKf6G1H7yXP7KYJKo/4vOGG6APRbFNlRb6aUZYiH2zslgi8zhuZzRS25bccWh+ss3K73nBgnR7oY/ZPm12b2ddfyue6rVXJCd2ksbv4YZfttHZ1Z5dpY5fZH7Nb7MrXjEbJ6UQN/0RWVzZm1587Ou7owh4J5/YI2qepykPTbAoEY37VkHy2gZAL/E6GJMOzNMFF1vBsfZZj71JycXCWkbmQyuPJPa145W4ppbjedNrn+p4OeLW+5uVGnQ55fk8bru9/qjLR5YojdjDuaX5DT0ecj1pNDVXS1gfBqaAvuKSuo9OCbwU9wVBwJjW3gveCN4KBoJGaEe/bL+4saA3WR9D0/UGzzVfwFmu6HV55wn83mgxiWNTVY5rldBjn9XadV8N5WW3TAujeOw3gO8igM0DX6P+r8OpXITff+60L8e+f4pj6qgN0dwi7epWusrIA+h9Fieuf4ld3T0cdnuuqpF6XkAxeAA==",
        },
        {"url": "https://puzz.link/p?kurodoko/9/9/h3j4g3j4l.j4g3j.ldl.j5g6j.l7j5g6j5h", "test": False},
    ]

    def program(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())
        self.add_program_line(adjacent())
        self.add_program_line(avoid_adjacent_color(color="black"))
        self.add_program_line(grid_color_connected(color="not black"))

        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="not black"))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black"))

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"black({r}, {c}).")
            else:
                self.add_program_line(f"not black({r}, {c}).")

        self.add_program_line(display())

        return self.asp_program
