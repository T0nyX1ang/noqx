"""The Yajikabe solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.rule.variety import yaji_count


class YajiKabeSolver(Solver):
    """The Yajikabe solver."""

    name = "Yajikabe"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZRLb9swDIDv/hWFzjro5ect65pe0nRbUhSFYRiO66JGHbhz4mFQkP8+ijJmd0qB7bBuAwZHNPOJokiJ5u5zX3QV5cz8ZEThDY/iEQ4RBTjY8KzrfVMlZ3TW7x/bDhRKr+dz+lA0u4p66WCWeQcdJ3pG9WWSEk4oETA4yaj+mBz0VaKXVK9gilAFbGGNBKgXo3qL80Y7t5Az0JeggzMO6h2oZd2VTZUvLPmQpHpNidnnHa42Ktm2XyoyxGH+l+12UxuwKfaQze6xfh5mdv19+9QPttws7Zt9XbZN2xH0x7Mj1TObwupECnJMQX5PQZ5OQfz+FOLTKRzhej5BEnmSmnxuRjUa1VVyOJpYD0RKs1LmJn5zk+BUKgepyCIxIp9ZJEcUIOI5myB0L6a+At+iiVUoXRQ4C8PQup/sGDHHKoodxNngTE7Z4G2SEufKteOBsyvnsWXTPQR37cRwuGzKYpdJ4cYsQzcWNbBpzCp2mY8xsxdr7U2ocQ8oAI5lcIdyjlKgXEOVUC1RvkfJUPooF2hzgfIW5TlKhTJAm9DU2U9WIpFwiwqKDApD2LJ8g9hSaZvhy8f/91jmpWTVdw9FWUGbWPbbTdWdLdtuWzQEevXRI18JjlRSYcz/t++/un2bq2K/1MT//JecwonD96SvKXnu8yKHnPBsDVf+D1xZ7tj7r/DgFR5mb34K0DYy7xs=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="black"))
        self.add_program_line(avoid_rect(2, 2, color="black"))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            fail_false(isinstance(clue, int) and label.startswith("arrow"), "Please set all NUMBER to arrow sub.")
            self.add_program_line(f"not black({r}, {c}).")
            arrow_direction = label.split("_")[1]
            self.add_program_line(yaji_count(int(clue), (r, c), arrow_direction, color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
