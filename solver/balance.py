"""The Balance Loop solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_segment, route_sign, single_route


def balance_rule() -> str:
    """Generate a balance rule."""
    rule = ':- black_clue(R, C), segment(R, C, N1, N2, "T"), |R - N1| = |C - N2|.\n'
    rule += ':- black_clue(R, C), segment(R, C, N1, N2, "V"), |R - N1| = |R - N2|.\n'
    rule += ':- black_clue(R, C), segment(R, C, N1, N2, "H"), |C - N1| = |C - N2|.\n'
    rule += ':- white_clue(R, C), segment(R, C, N1, N2, "T"), |R - N1| != |C - N2|.\n'
    rule += ':- white_clue(R, C), segment(R, C, N1, N2, "V"), |R - N1| != |R - N2|.\n'
    rule += ':- white_clue(R, C), segment(R, C, N1, N2, "H"), |C - N1| != |C - N2|.\n'
    return rule


def count_balance(target: int, src_cell: Tuple[int, int]) -> str:
    """Generate a constraint to count the length of "2-way" straight lines."""
    r, c = src_cell
    rule = f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| + |{c} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "V"), |{r} - N1| + |{r} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "H"), |{c} - N1| + |{c} - N2| != {target}.\n'
    return rule


class BalanceSolver(Solver):
    """The Balance Loop solver."""

    name = "Balance Loop"
    category = "route"
    aliases = ["balanceloop"]
    examples = [
        {
            "data": "m=edit&p=7VZNb9swDL3nVwQ666Avy7JvWdfskqXb2qIoDCNIMg8NlsxdPobCQf77aMqpa0kB1qHIZYNhgnyU6Cf6Sfbm5266LiiPaEKloYxyuDQzEIAvJN6suW4W22WR9ulgt30o1+BQejUc0m/T5aboZc2ovLevkrQa0OpDmhFBKN6c5LT6nO6rj2k1otU1pAjlgI3A44QKcC9b9w7ztXdhQc7AH1s/Bvce3PliPV8Wk5Et9CnNqhtK6ue8w9m1S1blr4LYaRjPy9VsUQOz6RYWs3lYPDaZze5r+X3XjOX5gVaD03RlS1c+05VhuuIt6C4XP4qnENMkPxyg41+A6yTNatq3rWta9zrdH2pKe6I0TDVU2ZdCVFxX6pMWMADo51CLJs+PgARAtaFy8rFxCsYJTjiGhnXChDnzE+4CLgPOtPMIztxVcObS4MKrI6SHuKvhsq4j2yoycesq5iKRVyWKPER32sh1HUdtDe2tSJvuCCO6FYy3GqO6IxLTaT1P3LUI9vLlgGA4yub+KBtBuzK26vFRE0JRSdxDZRBVITQO1kV9eSjKzENRbV5dlJyPBvla8XmFrQIDcJCy1aJfWwSbYVXpwzJcWwb7YWXqw1G4Ngo2AOsgrMM90eGe6DBvE+6JCffEhHkn4dpJsCdW7g4Meh+i6gXaGzg/aSXRvkfL0EZoRzjmEu0d2gu0Cq3GMXF9Ar/qjH658V5Lh0QSXl1i6h3ArKMYVaBwiV4EnZB/yDlT9ofg1BX9W9m8l5ERfIj743K9mi7hczzerWbF+hjDr8+hR54I3vDN4FT9/xs6/99Q3X12tv32Nts/g8Y2+5RWV5Q87ibTybwEjUHvjknYuqeSIDXxN0k4I8IJOEW8xNl7BidQ3vsN"
        },
        {"url": "https://puzz.link/p?balance/10/10/q1i8k8k0i1g8h1g9k9h0j1h8k8g0h9g0i1k9k9i0q", "test": False},
        {"url": "https://puzz.link/p?balance/10/10/0g00zg0l0m0k0k0k0k0h0m0k0n0l0h", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black_clue"))
        self.add_program_line(defined(item="white_clue"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_sign(color="white"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            self.add_program_line(f"white({r}, {c}).")
            self.add_program_line(route_segment((r, c)))

            if symbol_name == "circle_L__1":
                self.add_program_line(f"white_clue({r}, {c}).")
                num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count_balance(num, (r, c)))

            if symbol_name == "circle_L__2":
                self.add_program_line(f"black_clue({r}, {c}).")
                num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count_balance(num, (r, c)))

        self.add_program_line(balance_rule())

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
