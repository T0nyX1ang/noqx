"""The Fill-a-pix solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent


class FillpixSolver(Solver):
    """The Fill-a-pix solver."""

    name = "Fill-a-pix"
    category = "shade"
    aliases = ["fillapix", "mosiak"]
    examples = [
        {
            "data": "m=edit&p=7VdPbxo/EL3zKSKffdix9/+lStOkl5T0V1JF0QohQjcKKogUQlUt4rtn/Ex/O+tNpfbQpIcIdjQ8z3jejGdts/m2na5rTYn72lxHmviTRjkeyvk3Pz8/l/OHRV0e6ePtw91qzYrWF2dn+na62NSD6mA1HuyaomyOdfO+rBQprQw/pMa6+a/cNR/KZqibEQ8pnTN27o0Mq6eteoVxp514kCLWhwed1WtWZ/P1bFFPzj3ysayaS61cnLfwdqparr7X6sDD/Z6tljdzB9xMHziZzd38/jCy2X5Zfd0ebGm8182xpzt6gq5t6TrV03XaE3RdFn+ZbjHe77nsn5jwpKwc98+tmrfqqNyxHJY7FUfOlVeG/Nqo2DjACiAOgTQEcgfEAigckLRAgigSoMAlQZSoBVK4vBFASCyFi5gjBTEBZCDmluEA5GG2OXhIC0SRFjYEwnrkSWgBHhLIAqAAD8G0AA8xaYESCoCi0IQiUOsgoCKqSBRGIhPWkQzoidUhg8JlArGYWdrYno3vpVQiqJVInBLURs6T9OZJwvYh3wwdpFcNv/odG+Qlc0/DhqAMNZReGeaRfHwbScT3gESKPoLouUQwT9Eixq9pB8E8HQSVF1U1BC/B2RCyENENwUtENwQ+HRvUWcYymEd6mTAvY8OOMhY2kqHvjQ6CWBKJe5x9t8i8/DYhvfw+0bHp1SdFLJlFBs4yll/3DhJ2uMnC98L4TujM3IvldxBZn7znlcNLRi8QXXr1+sf4PUHwsb5/xPtl/fsu3gtL4PO/F+/7hN3/GvIM0kBe8uGgGwv5DjKCTCDPYXMKeQV5AhlDprDJ3PHymwcQjp6cDwvOwfjT6Bm4VbG/2vzqwxeg19F/e3Q8qNRou76dzmq+Aw23y5t6fTRcrZfTheJL536gfig8lWXz+PUe+kL3ULcE0R/dRl9+b6q4urxDNBda3W8n08lstVD8V0YDpx7+7Ox5AxsPHgE=",
        },
    ]

    def program(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=8, include_self=True))

        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="gray", adj_type=8))

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"gray({r}, {c}).")
            else:
                self.add_program_line(f"not gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.asp_program
