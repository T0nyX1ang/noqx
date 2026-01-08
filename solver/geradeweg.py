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
    rule = f':- route_segment({r}, {c}, N1, N2, "T"), |{r} - N1| != {target}.\n'
    rule += f':- route_segment({r}, {c}, N1, N2, "T"), |{c} - N2| != {target}.\n'
    rule += f':- route_segment({r}, {c}, N1, N2, "V"), |{r} - N1| + |{r} - N2| != {target}.\n'
    rule += f':- route_segment({r}, {c}, N1, N2, "H"), |{c} - N1| + |{c} - N2| != {target}.\n'
    return rule


class GeradewegSolver(Solver):
    """The Geradeweg solver."""

    name = "Geradeweg"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VZtb9pIEP7Or6j2a1eq12sbY6k6kZdWighNrsnlEhShDSwvicGpgSRylP/emTGJvcYLre6uupNOxsvM86zH82LNzuLbSqWaCwd/MuTwD5cnQrrdMKDbWV9n02Wso3e8vVpOkhQEzr90+UjFC82PLm/3Du7aj4ftPz/4V1Ked0fvbw9Oz2+HF3+IU2f6IXW6cTg/PjnYi99/zq6OJ+0HfaiDk0UymMRaDVV2dXH0FM8/hePJSOwfTfbDkZo7i2/hWeth7/Tjx0Zv7cd14zlrRVmbZ5+jHnMZp1uwa56dRs/ZcZR1efYVKMYFYB2QBOMuiIeFeEE8Svs5KByQu7kcgHgJ4mCaDmLd7+SGTqJedsYZvmePnkaRzZIHzfLHSB8ks5spAjdqCelaTKb3a2axGiZ3q/VeMMhmq3g5HSRxkiKI2AvP2nkInZoQZBECinkIKP1TIcTTuX6q875V7/0LVOZ38L8f9TCU80IMC/Fr9AxrN3pm0oEnJQ/y4jHZAtV9U70mqKJQQ1PFzYXqo6lCDVAtTAW+wTY9gw3RcqEKx8WAHMjhGxIYzwsHXfMKXSBfsuAKk6dAS7xEf0q8h3qJ9yr2KBVlveKxj/vZbyWPKWImXxFIuKC0X9L6iVaX1jOoCs8krQe0OrT6tHZozyGtF7Tu0+rRGtCeJtb1pyr/V9xhnitZ1ArhE3ChjiRgflEIJJSOBO8VwVSiIAVHUoLkcgkWUIKeB5UCyfO4DzkFyQ95c73P4R68AKUm9MZcCjl+pSi1uJ9b8eELhvrIH8xTD+xikzUv/7+HXTd6rAMN4l03SWcqhjbRXc1udPqqQ5tmiyTuL1bpSA10Xz+pwZJF+XFRZgxsTjYMKE6Se+xENRZeKQOcjudJqmspBPVwbDOFVI2pmyQdVnx6VHFsxkInqQHlrdeAlin01ZKu0jR5NJCZWk4MoHSMGJb0vJLMpTJdVHeq8rZZkY6XBntidEMDhhP//zP133umYpWcX9Zf/55234Nkr3suz75wdr/qqz4ExmB84zlJbdhGUme2kHmztpB5/7abhZZuI6nL20hq/DaSzgKbQ3Q81JNwlNUTcJBZCC+wmfIsBARtMWUhYD5pcuFb8y/Aa9hipX04HGD+sNGBC7Q1XUABbS0SUFuM+56wEZZ8NqGw9YQtn03fkrafIX6E2nRgi9NbAt2SnJ1p3VmWnWXd+Vns/Kx2fpaw4Zd3PzpPk3TLcFOQVbhmxAF0y5RTYutwy0BTYqv4xvSCzm4OMIDWzDCAVscYgDYnGQA3hhnALPMMWq2ONOhVdarBV20MNviq8mzTY2OdqqF+1GN23fgO",
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
        self.add_program_line(shade_c(color="green"))
        self.add_program_line(fill_line(color="green"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="green", adj_type="line"))
        self.add_program_line(single_route(color="green"))
        self.add_program_line(route_sign(color="green"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(route_segment((r, c)))
            self.add_program_line(f':- route_segment({r}, {c}, N1, N2, "T"), |{r} - N1| != |{c} - N2|.')

            if isinstance(num, int):
                self.add_program_line(count_geradeweg_constraint(num, (r, c)))
                if num > 0:
                    self.add_program_line(f"green({r}, {c}).")
                else:
                    self.add_program_line(f"hole({r}, {c}).")  # optimize performance if there are too many holes
            else:
                self.add_program_line(f"green({r}, {c}).")

        for (r, c, d, _), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
