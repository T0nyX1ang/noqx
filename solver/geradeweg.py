"""The Geradeweg solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_segment, route_sign, single_route


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
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VZdb9MwFH3vr5j8fB/iryTNCypj8FI6YEXTFFVVV4IWkZKRNmhK1f/O9XW61KNuNwETSCjL7bk+tnc/7NMuv9WzKgMemD8ZA37io3hMr4hDeoP2GeerIktOYFCvbsoKAcD5CD7PimUGvbSdNemtm37SDKB5k6RMMKCXswk075N18zZpRtBcIMWA49gQEWcgEJ518JJ4g07tIA8QjywOEV4hnOfVvMimQ7vRuyRtxsDM/3lJqw1ki/J7xuwy8ufl4jo3A9ezFSazvMlvW2ZZfyq/1O1cbpbWxSqfl0VZsTbaDTQDm8JwTwqyS0HepyD/YApF/jW72xd9f3/0G+zMB4x/mqQmlY8djDt4kaw3Jsw1kwGulBDa5jHZR1fcuypCl3du7Lp9x9WB44aBs1WoHTZSDhvHjssDYRIK2M5I6KzngQlNdT4P3R0Ed3nphsOldnmlXV492I9Kses/iFib+ezFTsSUMZPbESw4p7JfkX1NVpAdY1egkWRfkQ3IarJDmnNG9pLsKVlFNqQ5kenrkzr/K+EwJSRL+jEeAaFaYOprQChFC9R2xJTSAMnBkBKRACktQkXihJQCHRPSMURiyyplUYTKZVEM5pQa1Adtd9F4grE/8pF1SqWVQPfR/97YpJeyIQrEyaisFrMCZWJUL66zauujTG967I7Ri9ccVf+/cv+9ym26FDzbLf49opJisdubDc05sNt6OptiYgx/JIAl6bL7SLr/HtJKgoe0KuHfFoXDR5KW+EiSFx9JiuMLiERoP4mCuZ9AufQQKvRtpTwEJu3ZykPgt2AEXHvrzzFqnOKlNUoQfsv56FAg7S0XUkh7m4TUgc214j7CU88IG7uf8NUz0p6yPYV4DPVzAAeCPpDogeIcLevRthxt69FjcfRYHT2WOOHZ1Q9/LUx6PwA=",
        },
        {
            "url": "https://puzz.link/p?geradeweg/17/17/0000i000i0000000i3g0g2i000000g1m3g000000j3g2j0000000g1k1g00000000000i00000000j0k0h2g0g2g1i.g.h4l1g3q2g2g2g0h2h0g2k1g00k00h3g0h000h1h000h0000000k000000000000g2g2g0000000000000i000000000000000g0000000000000000g00000000",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_sign(color="white"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(route_segment((r, c)))
            self.add_program_line(f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| != |{c} - N2|.')

            if isinstance(num, int):
                self.add_program_line(count_geradeweg_constraint(num, (r, c)))
                if num > 0:
                    self.add_program_line(f"white({r}, {c}).")
                else:
                    self.add_program_line(f"hole({r}, {c}).")  # optimize performance if there are too many holes
            else:
                self.add_program_line(f"white({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
