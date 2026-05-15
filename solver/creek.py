"""The Creek solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_covering
from noqx.rule.reachable import grid_color_connected


class CreekSolver(Solver):
    """The Creek solver."""

    name = "Creek"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVdb5swFH3nV1R+9oO/wMDLlHXdXjK6LZmqCqGIULpGI6IjYaoc5b/v+oJGa/ehfVimSZPjo5vj4+vDxca7H33Z1ZQL+5MxZZRDU4nCLnWInY1tudk3dXpGZ/3+ru0goPQyo7dls6uDnONUXgQHk6RmRs2HNCecUCKwF9R8Tg/mY2oyahYwRGgM3HwQCQgvpvAKx210PpCcQZwNcQThNYTVpquaejWHUWA+pblZUmLXeYuzbUi27c+ajD7s/6rdrjeWWJd7eJbd3eZ+HNn1N+33ftTy4kjNbLC7eMaunOzK33blH7Rb33yrH55zmhTHI1T8C3hdpbm1/XUK4ylcpIejtXQgkmk79w04o5ABEkqWWEY8Yji3jHzMhK5GSFcjEpdRbPQ5MdzNo4SnUV4e7c4KPT+hdvOEsctEzM0cCTeP9hxqX+Otpb0axrG7VuxpEuYxXuUT6WgUk87qiilXI9zKK+99KeHPCj2NW3klPY30NN57V+ppDWEzctyS14jvEQXiEnYsNRLxHSJDDBHnqLlAvEI8R1SIEWq03fMvPBUkhIILSiJ4hng4Iifwlofj5/JJ0/8eVwQ5WfTdbVnV8HnK+u267s6yttuWDYGr4BiQB4I9l/Zi+X87nP52sNVnr7oj/v7hzKGwkabmkpL7flWuqrYhFMpmeTg6Ln9y93CCi+AX",
        },
        {"url": "https://puzz.link/p?creek/10/10/qbdccdbdbibiceeeddcblbbcdcdddboabbb", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(grid_color_connected(color="not gray"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_covering(num, (r, c), Direction.TOP_LEFT, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
