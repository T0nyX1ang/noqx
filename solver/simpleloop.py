"""The Simple Loop solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import direction, display, fill_path, grid
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("simpleloop(R, C) :- grid(R, C), not black(R, C).")
    solver.add_program_line(fill_path(color="simpleloop"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="simpleloop", adj_type="loop"))
    solver.add_program_line(single_loop(color="simpleloop"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Simple Loop",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VVda9swFH33rwh61oM+/aG3rGv24mUfySjFmOJmLjVz5sxJRlHIf+/VvRp5CWwwKIUGWeceXR1JRzJI21/7Zmy5EuHTORdcQsmKHGtuJVYRy7Lb9a2b8Ol+9ziMQDj/NJvxh6bftkkVVXVy8IXzU+4/uIopxrFKVnP/xR38R+cX3C+gi3EDuRKYZFwBvT7RG+wP7IqSUgCfRw70FuiqG1d9e1dS5rOr/JKzsM47HB0oWw+/W0bDsL0a1vddSNw3O9jM9rHbxJ7t/vvwYx+1sj5yPyW75Rm7+mQ3ULIb2Bm7YRf/bbfvfrZP55wW9fEIJ/4VvN65Ktj+dqL5iS7cgVnDnOHM5hhShaGQGKQQFKWlqKhbqtg2BcU0tjNNMY/5IuYLaitB8ypBOhXnUymto2O/FhlFTeO0jXmbUsz/RNKZOM5oWs9YmtektI5Joy6LuozGm5w2bwravRUxKtLZ6M/ifuHA5u4AKBFvEWeICnEJp8q9RnyPKBAtYomaa8QbxCtEg5iiJgv/5R//3IvZqSzdAH8v9qK76N6erk4qttiPD82qhdu4hFt5Mh/GddMzePeOCXtiWCsNYnN5Cl/+KQynL17btfra7MBFz7bdetO3k34YNqxOngE=",
        }
    ],
}
