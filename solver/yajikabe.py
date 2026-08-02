"""The Yajikabe solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction
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
            "data": "m=edit&p=7VTNbtswDL7nKQqddbB+7Di+DFnX7JKlW5OhKIzAcDIXDebAnRMPg4K8e0lKgKUlBbbDug0oHDH0J4rkJ9LcfevKtuIiwp9KOfzDo0VKS6YJrcg9i82+rrILPu72D00LCufXkwm/L+tdxQe5M1sODmaUmTE377OcCcaZhCXYkptP2cF8yMyMmzlsMa4Bm1ojCepVr97SPmqXFhQR6DPQwZng7Abd3cHretOu66qYAgrIxyw3C85w8y15QJVtm+8Vc7ng+7rZrjYIrMo9MNo9bB7dzq770nztnC04ZNuu3m/WTd20CCJ25GZsaczP0FA9DVQtDdTO0EB2f5jC6DyFI5ToBkgUWY58Pvdq2qvz7ABylh2YjPFkgeljMcGnUoioANKn0AihNz6kU2tlq0hQHFlI9VBCkCgiD6KI0veVUFrStxo6Kx9KTg4Oh9a9FzGliIFVStkHkIicM++kiJw3j5IQdBmhnaCzQVQhKIYIYkhxaifdfXu8hKSzIabkac6K8gtz0Q7zc9aOr4/FlHMUnLWV0H0M6BJBvXJHckJSklxAK3GjSL4jGZGMSU7J5orkLclLkppkQjZDbMZfbFemoIoamgwaQ9refYHccmWnZvjE/x+2HORs3rX35bqCWTLrtquqvZg17basGQz144D9YLRyxSWav875f37OY7mi35r2f/9rzuHG4Zsy15w9dkVZACe6W8R1/BMONTlrHz+DJ8/gw+WL3wKMjuXgCQ==",
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
            self.add_program_line(f"not black({r}, {c}).")

            if isinstance(clue, int) and label.startswith("arrow"):
                arrow_direction = label.split("_")[1]
                self.add_program_line(yaji_count(clue, (r, c), arrow_direction, color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
