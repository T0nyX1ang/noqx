"""The Kakuru solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_num, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_number_adjacent


def count_adjacent_sum(target: int, src_cell: Tuple[int, int], adj_type: int = 8) -> str:
    """Generate a constraint to count the sum of numbers in adjacent cells."""
    r, c = src_cell
    return f":- #sum {{ N, R1, C1: number(R1, C1, N), adj_{adj_type}(R1, C1, {r}, {c}) }} != {target}."


def avoid_repeating_digit(src_cell: Tuple[int, int], adj_type: int = 8) -> str:
    """Generate a constraint to avoid repeating digits in adjacent cells."""
    r, c = src_cell
    return f":- number(_, _, N), {{ grid(R, C): number(R, C, N), adj_{adj_type}(R, C, {r}, {c}) }} > 1."


class KakuruSolver(Solver):
    """The Kakuru solver."""

    name = "Kakuru"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VTJTsMwEL3nKyqffYiXbL6gspRLKUuLELIilJZUrWgVSBuEHOXfGY8DqSoOXIAekOuZ1+ex/TzjePNSZWVOA2gipj5l0DiPsUvf/j7aZLld5apH+9V2UZQAKL0cDOg8W21yT7dRqVebRJk+NedKE0Yo4dAZSam5VrW5UGZEzRiGCJXADV0QB3jWwTsct+jEkcwHPHI4BHgPcLYsZ6v8YQijwFwpbSaU2H2OcbaFZF285qTVYf/PivV0aYlptoXDbBbL53ZkUz0WT1Uby9KGmv6eXNbJFZ1c8SlXfC2X/7zcJG0aSPsNCH5Q2mq/7WDcwbGqCfeJklAU5hx3TjgnnUvQCUeKGJ10kTJCF7jpQehcS7rIwE0P7UaNTUONu2kioHbuKuC+moQ7hLDE0Q6R7BECI5IdIsbj846RuCqLd5gIGdYxAdtbN4j2CVwXctExqIVFHwyciqm6sXW1doCWo51ApqkRaE/R+mgDtEOMOUN7h/YErUQbYkxka/XNarr0/oIczd3DYFvwPZR6moyrcp7Ncrizo2o9zcveqCjX2YrAI9F45I1g1wLC5f+78Ufvhi2Bf2j37dDkwBeQeu8="
        },
        {
            "data": "m=edit&p=7VRNj9MwEL3nV6x89iH+iltfUHfZcinlo0UrZEWrtGS1Fa0CaYOQq/x3xjPRunQ5rJCAPSDLz69vxvWzx/H+a1e1NS+gqRHPuYAmiwK70Bp7PrTl5rCt3QWfdIf7pgXC+ZvplN9V232d+SGrzI5h7MKEh1fOM8E4k9AFK3l4547htQtzHhYQYlyDNqMkCfQ60RuMR3ZFosiBz4kXQD8CXW/a9ba+nUEUlLfOhyVncZ1LnB0p2zXfajb4iL/XzW61icKqOsBm9vebL0Nk331qPndDrih7HiZndkWyq5Jd9WBX/dqu/PN2x2Xfw7G/B8O3zkfvHxIdJbpwRyYlcxqKomkwNFgclMJBU4qmmKaYIdHQPENiUeBgKWYpZmmejSl9PAZaFJxqKB7dBVz/TDFRkeJEsVF5kYTozzOVJ0XL80naPMrBvxE2KUae5xi0o08VnDVOQtyrj54eFEu7Gp0oj3Zl0Y5QJ4r9WYEjEu7Yx0sScYooEZdQNh4U4kvEHNEgzjDnGvEG8QpRIxaYY2Phn3g1qFZ/wY6XEt8Zaub3eZl5tujau2pdw2cx73arur2YN+2u2jJ4h/qMfWfYvYJ0/f9p+kdPUyxB/txu4XOzA99Fmf0A"
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(fill_num(_range=range(1, 10)))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(avoid_same_number_adjacent(adj_type=8))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(avoid_repeating_digit(src_cell=(r, c), adj_type=8))
            if isinstance(num, int):
                self.add_program_line(count_adjacent_sum(target=num, src_cell=(r, c), adj_type=8))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
