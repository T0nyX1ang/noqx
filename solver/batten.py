"""The Battenberg Painting solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type


def batten_constraint(color: str = "black") -> str:
    """Avoid checkerboard pattern at places without battenberg pieces."""

    rule = f"checkerboard(R, C) :- {color}(R, C), not {color}(R, C + 1), not {color}(R + 1, C), {color}(R + 1, C + 1).\n"
    rule += f"checkerboard(R, C) :- not {color}(R, C), {color}(R, C + 1), {color}(R + 1, C), not {color}(R + 1, C + 1).\n"
    rule += ":- grid(R, C), not batten(R, C), checkerboard(R, C).\n"
    rule += ":- grid(R, C), batten(R, C), not checkerboard(R, C)."
    return rule


class BattenbergPaintingSolver(Solver):
    """The Battenberg Painting solver."""

    name = "Battenberg Painting"
    category = "shade"
    aliases = ["battenbergpainting"]
    examples = [
        {
            "data": "m=edit&p=7VXfb6JAEH73r2j2tZscv1QkuQdrba89S23VeEqIQYtKC66HYHsY//fODu0JK/Z6yV1zD5eVyfDNMDvfLH6svsdO6NIaLFWnEpVhqbqEl67xn/Syul7ku8YRrcfRnIXgUHpt0qnjr1x6OZi3Gqz+eFr/ttaj4VA+l+ILqX9/dn98G3y98NRQPjP19lX7ylNm9S+Nk5tK87jSjle9yF3fBPLJfW/Ynbb7s5ryo2kOtWR4LZUvh9NP63rvc8mSsTHJLm2SmpHUaXJuWEQmlChwycSmyY2xSa6MZECTDoQI1W1KgtiPvAnzWUgQkyGvlT6ogNvcuX2Mc6+RgrIEvvnigzsAdxXfsYfYjSYp1DaspEsJ3/wEH+cuCdja5bvx5vj9hAVjjwNjJ4LxrebeklAVAmm1l1TZ3tKknlLovJMCFHmlwN2UAvcKKHBmnMLECye+O2r9eQY1e7uF07kFDiPD4nR6O1ffuR1jA9Y0NkSp8UfL0Ep6hESVOKBmAFnMUMQMVczQxIyykKFh0UyGjttWd0ANi/7MgHZlbHrAm1b4BhDIvwyAVw7gejGOZAvw6oE61QN1sPsinI9KxIHEGVJR0HbhSGiioj1FK6Eto21hThNtH20DrYa2gjlVfqjvPHaiQUs6HACMV0nfgexo/1JvlqagpO1W5WPv7ZJFOnE4dSYu/KHMOBi74ZHJwsDx4b4zd5YuAV0jK+aPVmneyH1yJhExUmnNRnLYAmvlIJ+xpe8tiiq8hnKgN1uw0C0McdC9mx0qxUMFpcYsvBN6enR8P88Fvzg5KNWlHBSFIDqZeycM2WMOCZxongMyApWr5C6EYUZOvkXnwRF2C3bj2JbIE8HLUim8TP8/Qv/2R4iflPRbn6IPkKFftGPBwEGokmtKlvHIGcGwYTqaTYsD5QMBmDDiqoCr9ofzxX8RC9+QtF1QhAuEDdA3tC0TLcIPyFgmKuJ7msWb3ZctQAuUC1BRvADa1y8A9yQMsAMqxquKQsa7ErWMb7UnZ3yrrKJZdukZ",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(batten_constraint(color="gray"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(symbol_name, "sudokuetc__1")
            self.add_program_line(f"batten({r - 1}, {c - 1}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
                self.add_program_line(count(num, color="gray", _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
                self.add_program_line(count(num, color="gray", _type="row", _id=r))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
