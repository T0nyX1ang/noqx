"""The Kurodoko solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="black"))
    solver.add_program_line(grid_color_connected(color="not black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(bulb_src_color_connected((r, c), color="not black"))

        if isinstance(num, int):
            solver.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Kurodoko",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VXBjtowEL3zFWjOc4jjxBDf6HbphbJtoVqtogiFNKtFGxQaSFUZ8e87M0lJUPfQHkqlqgp+em9mHL+MZbP/WqdVjkrxT4/RQ2IYhEaGUr4Mr32Wm0OR2yFO6sNTWRFBvJtO8TEt9vkgbquSwdFF1k3QvbMxKEDwaShI0H20R/feujm6BaUAA4rNmiKf6G1H7yXP7KYJKo/4vOGG6APRbFNlRb6aUZYiH2zslgi8zhuZzRS25bccWh+ss3K73nBgnR7oY/ZPm12b2ddfyue6rVXJCd2ksbv4YZfttHZ1Z5dpY5fZH7Nb7MrXjEbJ6UQN/0RWVzZm1587Ou7owh4J5/YI2qepykPTbAoEY37VkHy2gZAL/E6GJMOzNMFF1vBsfZZj71JycXCWkbmQyuPJPa145W4ppbjedNrn+p4OeLW+5uVGnQ55fk8bru9/qjLR5YojdjDuaX5DT0ecj1pNDVXS1gfBqaAvuKSuo9OCbwU9wVBwJjW3gveCN4KBoJGaEe/bL+4saA3WR9D0/UGzzVfwFmu6HV55wn83mgxiWNTVY5rldBjn9XadV8N5WW3TAujeOw3gO8igM0DX6P+r8OpXITff+60L8e+f4pj6qgN0dwi7epWusrIA+h9Fieuf4ld3T0cdnuuqpF6XkAxeAA==",
        }
    ],
}
