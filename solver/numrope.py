"""The Number Rope solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Point, Puzzle
from noqx.rule.common import defined, display, fill_num, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_number_adjacent


def numrope_constraint() -> str:
    """Generate a constraint for the number rope."""
    rule = "adj_count(R, C, N) :- grid(R, C), N = #count { R1, C1 : adj_line(R, C, R1, C1) }.\n"
    rule += ":- adj_count(R, C, N), N > 2.\n"
    rule += ":- adj_count(R, C, 1), number(R, C, N), number(R1, C1, N1), adj_line(R, C, R1, C1), |N - N1| != 1.\n"
    rule += (
        ":- adj_count(R, C, 2), number(R, C, N), N * 2 != #sum { N1, R1, C1 : number(R1, C1, N1), adj_line(R, C, R1, C1) }.\n"
    )
    return rule


class NumRopeSolver(Solver):
    """The Number Rope solver."""

    name = "Number Rope"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7ZRLj9MwEMfv/RQrn+fgZ2LnVhbKpZRHi1Yoiqq0ZLURLVnaBkGqfHfGnqSN0GpZBCoX5GTmZ3vs/DN+7L/U+a6AGIuywEFgUVyHN+L+6cuiPGyK5ArG9eGu2iEAvJ5M4Dbf7ItR2kVlo2PjkmYMzcskZYIBk/gKlkHzNjk2r5JmCs0cuxhobJtSkEF8QSgRb0K/p2tqFBx5RuyHfUAsPxcofVMevlPomyRtFsD8l56F8R7ZtvpasE6Jr6+r7ar0Dav8gL+zvyvvu559/bH6VHexImuhGZPg2eOC1UmweliwvIRgl7Utpv4dSl4mqVf//oz2jPPkyKRmiQamYnIuOE01Qy7i5FRwMTkryFHNReha/5c0I8rQmCNa7DB5yiQftLifY0yIEeLc4r+XMntu8J/EaQYhNoSIQYwXMhiEkkRybH3OvZ0EK4NdYA6gUcE+D5YHa4Kd4o8oAxqnM+BJEckhSSJtQTuKO5H0J6gn2ZEDzWkEBy1oxIkiAZEMZIZkiCILEc1shmSIYgeO92SJLAdHMzsJTlHbiWIBVvYUEzkNzlDckCxR3FHrN7tP4E2w18HqYKOQuthvriduv37LmG7V5B+v2hPlpVKH260v5u/XslHK5vXuNl8XeEineOKvZtVum2+wNqu3q2LX1/GebEfsGwtvqnCw/n91/sOr0y8D/60dfIEd+ws5KeYXr6TBKQJ2Xy/z5brCDcezi8vFM5aNfgA=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(fill_num(_range=range(1, 10)))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_same_number_adjacent(adj_type=4))
        self.add_program_line(numrope_constraint())

        for (r, c, d, _), draw in puzzle.line.items():
            fail_false(draw, f"Line must be drawn at ({r}, {c}).")
            self.add_program_line(f'line_io({r}, {c}, "{d}").')

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")

            if Point(r, c) in puzzle.surface:
                self.add_program_line(f":- #sum {{ N, R, C: number(R, C, N), |{r} - R| + |{c} - C| = 1 }} != {num}.")
            else:
                self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
