"""The Geradeweg solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.loop import loop_segment, loop_sign, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected


def count_geradeweg_constraint(target: int, src_cell: Tuple[int, int]) -> str:
    """Generate a constraint to count the geradeweg clue."""
    r, c = src_cell
    rule = f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "T"), |{c} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "V"), |{r} - N1| + |{r} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "H"), |{c} - N1| + |{c} - N2| != {target}.\n'
    return rule


class GeradewegSolver(Solver):
    """The Geradeweg solver."""

    name = "Geradeweg"
    category = "loop"
    examples = [
        {
            "data": "m=edit&p=7VXbTus4FH3vVyC/Yok414t0NOrtIKHSQ4cyHaiqym1TEkgbTi5QpeLf2dtJyaWB0Yh54GGUxl1ee9te205Wot8JDx1qwKWYVKIMLkVSxa1L+DtcYy/2HfuEtpPYDUIAlP4a0jX3I4de3D50eo/tl3777zPtTlFuhuvTh97o5mE1+YuNJO8slIa+ub286nX80/P07tJtPzt9R7+KgqXrO3zF07vJxc7f/jTv3TXrXrhdc823UvTbHFvPndGPH61prmPW2qeWnbZpem5PiUyouBmZ0XRk79NLO+3T9BpChDLgBoAYoTLAfgEnIo6om5FMAjzMMcBbgEsvXPrOfJAxV/Y0HVOC63TEaIRkEzw7JBsm+stgs/CQWPAYtityvac8EiWr4DHJc2FCskn82FsGfhAiidwrTdtZCYOGEpSiBIRZCYgaSsDKvlyC722dXZN6q1n9K5zMn6B/bk+xlJsCmgW8tvfQDu09UXQYiY+bODyimNBV3rsqdsk1TJwTmlSJaxiX37s6RskfRbouV9INjBfpBkbJeZFuIlHETbWkDfQyofpWtD9FK4t2DEXRVBFtT7SSaDXRDkROH2plikaZCgXLMCO8Z0y1MqzqlGlGji3KsA7EmgEYSkQM7yAzWI5hrJGPNUAg6hYYxlr5WBPqsJQMWxKVpXyspQCGwgADR2WWjQUOsJavCzq1XKdW0oZ6cMsFBg1arkEraUad+kEnaMMjEHog38zzzZJO0MasgzbIt/J8q6wfjtDKNMM/YNQJmzoRW9sVrSpaXWy5gU/Zv3oOv366/yhnKoPy0gV7/F/3Zq0pGcD7ejIMwg334a3tr+5LvWGyWTjhoQ8eSqLAn0dJuOZLZ+7s+DImdubl5UiF24o5KpQfBE9oEw0zHEIV0rvfBqHTGELSAc0fTIWhhqkWQbiqaXrhvl+tRXziKlTmixUqDsH0Sn0ehsFLhdnw2K0QJY+vzORsa5sZ86pE/shrq22K7XhtkR0Rt/Av9f8P3vf94OEpSd/Nbr6bHPGAB+EnblME63SD5wD7ie2Uok38Bw5Titb5IztBsceOAmyDqQBb9xWgjq0FyCN3Ae4Dg8FZ6x6Dquo2g0sdOQ0uVTabKXG5FyVk1noD",
        },
        {
            "url": "https://puzz.link/p?geradeweg/v:/17/17/0000i000i0000000i3g0g2i000000g1m3g000000j3g2j0000000g1k1g00000000000i00000000j0k0h2g0g2g1i.g.h4l1g3q2g2g2g0h2h0g2k1g00k00h3g0h000h1h000h0000000k000000000000g2g2g0000000000000i000000000000000g0000000000000000g00000000",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="clue"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line(shade_c(color="geradeweg"))
        self.add_program_line(fill_path(color="geradeweg"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="geradeweg", adj_type="loop"))
        self.add_program_line(single_loop(color="geradeweg"))
        self.add_program_line(loop_sign(color="geradeweg"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(loop_segment((r, c)))
            self.add_program_line(f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| != |{c} - N2|.')

            if isinstance(num, int):
                self.add_program_line(count_geradeweg_constraint(num, (r, c)))
                if num > 0:
                    self.add_program_line(f"geradeweg({r}, {c}).")
                else:
                    self.add_program_line(f"not geradeweg({r}, {c}).")
            else:
                self.add_program_line(f"geradeweg({r}, {c}).")

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_direction", size=3))

        return self.program
