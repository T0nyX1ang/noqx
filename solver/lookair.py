"""The Look Air solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.shape import all_rect


def square_size(color: str = "black") -> str:
    """Generate a rule to determine the size of the square."""
    rule = f'square_size(R, C, N) :- rect(R, C, "{Direction.TOP_LEFT}"), MC = #min {{ C0: grid(R, C0 - 1), not {color}(R, C0), C0 > C }}, N = MC - C.\n'
    rule += f"square_size(R, C, N) :- grid(R, C), {color}(R, C), square_size(R, C - 1, N).\n"
    rule += f"square_size(R, C, N) :- grid(R, C), {color}(R, C), square_size(R - 1, C, N).\n"
    return rule


def avoid_same_size_square_see(color: str = "black") -> str:
    """Generate a constraint to avoid the same size square seeing each other."""
    rule = f"left_square(R, C, C - 1) :- grid(R, C), {color}(R, C - 1), not {color}(R, C).\n"
    rule += "left_square(R, C, C0) :- grid(R, C), not left_square(R, C, C - 1), left_square(R, C - 1, C0).\n"
    rule += f':- rect(R, C, "{Direction.TOP_LEFT}"), left_square(R, C, MC), square_size(R, C, N), square_size(R, MC, N).\n'
    rule += f':- rect(R, C, "{Direction.LEFT}"), left_square(R, C, MC), square_size(R, C, N), square_size(R, MC, N).\n'

    rule += f"top_square(R, C, R - 1) :- grid(R, C), {color}(R - 1, C), not {color}(R, C).\n"
    rule += "top_square(R, C, R0) :- grid(R, C), not top_square(R, C, R - 1), top_square(R - 1, C, R0).\n"
    rule += f':- rect(R, C, "{Direction.TOP_LEFT}"), top_square(R, C, MR), square_size(R, C, N), square_size(MR, C, N).\n'
    rule += f':- rect(R, C, "{Direction.TOP}"), top_square(R, C, MR), square_size(R, C, N), square_size(MR, C, N).\n'
    return rule


class LookAirSolver(Solver):
    """The Look Air solver."""

    name = "Look Air"
    category = "shade"
    aliases = ["rukkuea"]
    examples = [
        {
            "data": "m=edit&p=7VRNT4NAEL3zK8yc5wC7QOteTK2tl1o/WtM0hDQUaWykQWkxZhv+u7MDFa0e1ES9mM28PN7Osm9nGdYPRZQn6NOQbbTRoSF8n8NxXQ67HuPlJk3UAXaKzW2WE0E87/dxEaXrxArqrNDa6kOlO6hPVQACkMOBEPWl2uozpYeoRzQF2CZtQMwBFER7DZ3wvGHdSnRs4sOaE50SjZd5nCazQaVcqECPEcw+x7zaUFhljwlUy/g5zlbzpRHm0YYOs75d3tcz6+Imuytgt0WJulPZHe3sisaubOzKF7vyY7vi5+0ehmVJZb8iwzMVGO/XDW03dKS2pfG1BSHMUkleqrsB0TLCUSPI/Qzp7Qlua1etWvAkVFe+E3wW7FeCt5fRkm/eQe4c9jhl7DMKxjEdAbVkPGG0GT3GAef0GCeMXUaX0eeclinCJ8sEgoy1qSwuKFHV7Be8BUJwA1bD+z4PrQBGRb6I4oS+l2Gxmif5wTDLV1EK1KClBU/AEUhKd/979o961lyB/aXO/fsOCai6QqI+R7gvZtEszlKg3z5+S3ff6b9+Wmq70HoG"
        },
        {"url": "https://puzz.link/p?lookair/9/9/g2a2b4d2i2y1i3d4b1a1g", "test": False},
        {"url": "https://pzplus.tck.mn/p?lookair/20/10/1b2f12b1c3d2l2zzg2a1b4a3zzg2l4d2c1b32f3b2", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(all_rect(color="gray", square=True))
        self.add_program_line(square_size(color="gray"))
        self.add_program_line(avoid_same_size_square_see(color="gray"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="gray", adj_type=4, include_self=True))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
