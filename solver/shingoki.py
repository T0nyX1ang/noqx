"""The Shingoki solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_segment, route_sign, route_straight, route_turning, single_route


def count_shingoki(target: int, src_cell: Tuple[int, int]) -> str:
    """Generate a constraint to count the length of "2-way" straight lines."""
    r, c = src_cell
    rule = f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| + |{c} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "V"), |{r} - N1| + |{r} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "H"), |{c} - N1| + |{c} - N2| != {target}.\n'
    return rule


class ShingokiSolver(Solver):
    """The Shingoki solver."""

    name = "Shingoki"
    category = "route"
    aliases = ["trafficlights", "semaphores"]
    examples = [
        {
            "data": "m=edit&p=7VVRb5tADH7Pr6j87AeOAwK8ZW2zlyzdlkxVhaKIZExBIyMjYaqI8t/n89HScDdplaqqkyZyjvlsfP5sfOx/1mmVoXDUT4ZI/3R5IuTlhgEvp73m+aHI4gsc1YdNWZGCeDMe47e02Gc4SFq3xeDYRHEzwuZ9nIALyEvAAptP8bH5EDdTbGZkAhSETUgTgC6p1516y3alXWpQOKRPW53UO1LXebUusuVEIx/jpJkjqH3e8dNKhW35KwP9GN+vy+0qV8AqPRCb/SbftZZ9/bX8XsPjFrCti0O+LouygjbbEzYjTWFioSA7CvKRgrRTcF+CQpH/yO5t2Uf27E/Umc+U/zJOFJUvnRp26iw+nlSaR/AC0A0Uun3guwrwOiAQLeA9AEMFBJ3H0O15hE4vaCQV4HcewulvIxxPIfIJ4j481SFh30f2txLSiBM4Z3sRc8H874i/9Mnm4nmPdFVEH+XSGCjXx4gQqLi+gQ5tKNfPiMBFNHwjYcuB62tE0EU2nHWljchCWFPWXbDAoRXmfphbclNM2LPn7UXW2IGlItTGMTfTZTmn9xsbyfKKpcPSZzlhn2uWtywvWXosA/YZqgl51gw9fZ+emw4EknoUhQiSzmbqrWTNo3LJv0w1kfpAP7/8fw9bDBKY0Gl3MS2rbVrQmTett6us6u5nm3SXAX17TgO4B16JRPf/5+gtf45Ul5xXG6iXme+Eik2Tic0Nwq5epksiBfSaoTK0o/pnI02vYXx1gnQwLAa/AQ=="
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_sign(color="white"))
        self.add_program_line(route_straight(color="white"))
        self.add_program_line(route_turning(color="white"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            self.add_program_line(f"white({r}, {c}).")
            self.add_program_line(route_segment((r, c)))

            if symbol_name == "circle_L__1":
                self.add_program_line(f":- turning({r}, {c}).")
                num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count_shingoki(num, (r, c)))

            if symbol_name == "circle_L__2":
                self.add_program_line(f":- straight({r}, {c}).")
                num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count_shingoki(num, (r, c)))

            if symbol_name == "circle_L__5":
                num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count_shingoki(num, (r, c)))

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
