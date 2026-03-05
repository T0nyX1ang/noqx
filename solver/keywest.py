"""The Key West solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, fill_line, fill_num, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_number_adjacent
from noqx.rule.reachable import grid_color_connected


def keywest_rule(color: str = "black") -> str:
    """Generate a rule to ensure the keywest constraints are met."""
    rule = f"number(R, C, 0) :- {color}(R, C).\n"
    rule += ":- number(R, C, N), #count { D: line_io(R, C, D) } != N.\n"
    rule += f':- grid(R, C), line_io(R, C, "{Direction.LEFT}"), not line_io(R, C - 1, "{Direction.RIGHT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.TOP}"), not line_io(R - 1, C, "{Direction.BOTTOM}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.RIGHT}"), not line_io(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.BOTTOM}"), not line_io(R + 1, C, "{Direction.TOP}").'
    return rule


class KeyWestSolver(Solver):
    """The Key West solver."""

    name = "Key West"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VZdb9owFH3nV1R+vg92nC/njXVlLxndVqqqiiIELFOjJUsXyDQZ8d93fQMFrkDqtKrbw2RydT9snxzbJ2b5vZu1BUTYdAwSFDYtfXpC6X67NilXVZFcwLBbPTQtOgDXoxF8mVXLAgbZtls+WFuT2CHYd0kmtADh0ZOD/Zis7fvEjsHeYEmAykHUXbUqF03VtGKXsyl6SoCH7tXevaO68y77pJLoj3s/RPce3UXZLqpimvYTfUgyOwHhsN/QaOeKuvlRiH4YxYumnpcuMZ+tkOHyoXwUoLGw7D43X7ttV5VvwA57BukzGeg9A/3EQP8tBibfbHBzPiGHaZI5Ord7N967N8l6415rLTy/pxQCjsfpvIDF4Xbqp0TEOsQsNsexliwmAH2QCFkHBqAZgDbsjXxC8A4S6niEzxB8QpAHCQbhMw4B4xAwgMBjEwaMQ8AAAgYQSjZByBBCj8WaxTFblJAhRIxCxAAiBhBp9kYROygRA4gJwD9IKLbRMYOIGYeYIcQB21fDOBjGwTAAwwCMzxbJsMNujg4KKkSRTu7Jjsh6ZCcoI7Ca7FuykmxANqU+V2TvyF6S9cmG1CdyQvwtqf7J66Bq8YCY2MnV9I4vd46S2xLeCLgg2mkUnGZ6z+lTP5NPhnOogxa8fJQPMpGW34qLcdPWswo/j+OunhftLsbLaTMQPwU9mQbPDfl/X/3D95XbKPlqUngZZWa44KgpsNcgHrvpbIqrLfCfEbgCSut0AcV3ZoSSpwtbUZ4p9jo9X9Qniq++kPhVyAe/AA==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(fill_num(_range=range(1, 5), color="black"))
        self.add_program_line(fill_line(color="not black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_same_number_adjacent(adj_type=4))
        self.add_program_line(grid_color_connected(color="not black", adj_type="line"))
        self.add_program_line(keywest_rule())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if isinstance(num, int) and num > 0:
                self.add_program_line(f"not black({r}, {c}).")
                self.add_program_line(f":- not number({r}, {c}, {num}).")

            if isinstance(num, int) and num == 0:
                self.add_program_line(f"black({r}, {c}).")
                self.add_program_line(f"number({r}, {c}, 0).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="number", size=3))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
