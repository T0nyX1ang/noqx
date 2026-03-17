"""The Simplegako solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, fill_num, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type


def simplegako_fill_constraint() -> str:
    """Generate a constraint for the number filling in simplegako."""
    return (
        ":- number(R, C, N), RC = #count { R1 : number(R1, C, N) }, CC = #count { C1 : number(R, C1, N) }, N != RC + CC - 1."
    )


class SimplegakoSolver(Solver):
    """The Simplegako solver."""

    name = "Simplegako"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VNNT4NAEL3zK5o57wF2gbZ7q7X1UvGjNU1DSEMrpkQICsWYJfx3Zwcq0ehBE7UHM5mXx9vZzBtgiscyzCPmYogBM5mFwV2X0rJtSrONRbxPItljo3K/y3IkjF1Mp+wuTIrI8NuqwKjUUKoRU2fSBwsYcEwLAqauZKXOpfKYmuMRMAu1WVPEkU46uqRzzcaNaJnIvZYjXSHdxvk2idazRrmUvlow0H1O6LamkGZPEbQ+9PM2SzexFjbhHocpdvFDe1KUt9l9CYcWNVOjz+2Kzq54tSs+tst/3u4wqGt87ddoeC197f2mo4OOzmVVa18VcFdf7aOX5tuA4IfRW8EW7wTH1oLoBNfRgt0JffeNgK0sarginBJywgX6YUoQnhKahA7hjGomhEvCMaFN6FJNX0/0pZl/wY7POS1QE873eWD44JXpJsp7XpanYQK4VrUBz0DpCyyy/zftjzZNfwLz2P69Y7OD2xAYLw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_num(_range=range(1, puzzle.row + puzzle.col)))
        self.add_program_line(simplegako_fill_constraint())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
