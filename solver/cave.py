"""The Cave solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import (
    border_color_connected,
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)


def cave_product_rule(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4):
    """Product rule for cave."""
    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"
    return f":- {count_r}, {count_c}, CR * CC != {target}."


class CaveSolver(Solver):
    """The Cave solver."""

    name = "Cave"
    category = "shade"
    aliases = ["bag", "corral", "correl"]
    examples = [
        {
            "data": "m=edit&p=7VTLauMwFN37K4LWd2FJtvzYpZ1mNmmmM0kpxZjgZFwS6uCME5dBwf8+VzdOVYVuCqWUMtg6nPvSPbYeuz9t0ZTAuXllDD4ggyBUNDgXNPz+ma33VZkOYNjuV3WDBODHaAQPRbUrvazPyr2DTlI9BP09zZhg0I8c9M/0oK9TPQE9xRADjr4xMs5AIL2y9I7ihl0endxHPuk50nuky3WzrMr5+Oi5STM9A2b6XFC1oWxTP5XsWEb2st4s1saxKPb4MbvVettHdu3v+rFlpxYd6OFR7vQkN7BypZUrn+XK1+WKd5FbbevXhCZ51+EP/4VS52lmVN9aGls6TQ+dUXRgUmBpgquM5TibDNCMns3AR1NZ0ySH1oyd5FA5UeUmq8CZKvKd2kg40US5ptsIN6Ejmgs3nYuz/NCVwsPAtZURw/0XDlcOV2ZCcyxOjsh0lNaOzwpi0yG2duJ+Lk9e5uNScFqQe8IRoSCc4XqBloTfCH3CkHBMOVeEd4SXhAGhopzIrPib9sQHyMmkoKvl/Am/rjf3MjZtm4diWeLJnbSbRdkMJnWzKSqGl2Tnsb+MBm2r4P+9+eH3pvn5/mc7KZ9NDp7d3PsH"
        },
        {
            "data": "m=edit&p=7VXfT6swFH7nrzB9Pg+0ZQi8mF2v82XOH5sxhpCFIcZFFiYbxnThf/f0wCQFH7yJmTG56Xr29WvP6ccpPWxeyrhIgdv6Jz3Af2wO96gLz6VuN2223GZpcATDcvuUFwgALkcjeIyzTWqFzarI2ik/UENQ50HIBIOmR6Cug526CNQE1BSnGHDkxog4A4HwrIV3NK/RaU1yG/GkwQjvESbLIsnS+bhmroJQzYDpff6Qt4Zslb+mrHajcZKvFktNLOItPszmabluZjblQ/5csv0WFahhLXe6l+u0cmUrV37IlZ/LFd8iN1vnnwn1o6rChN+g1HkQatW3LfRaOA12lVa0Y9LVrieoAjAAxnMGSIh26BnDATeHXsfb5V3C6RCebUTwzPi+Gd+XHW9ud+Nx3meOu4ywe4wwNuLCN8eyt7PsRXVc08fpxOhlh7vCYPAMOJ3EPdkRWUF2hgcFSpL9S9YmOyA7pjVnZO/InpJ1yLq05lgf9RdfBiYxQY6WjI8k6lfjAOJCWVcYsw1+HxdZIZuWxWOcpHgtJ+VqkRZHk7xYxRnDClhZ7I1RD6UuqP+L4sGLok6+/U+l8ecvZ4h5xRuiLoGty3k8T/KM4RcVNI83tTdxcPl4gyPrHQ=="
        },
        {
            "data": "m=edit&p=7VRNT4NAEL3zK8ye98DsAgVutVovtX60pjGEGFoxNtKgtBizDf/dmYGWkngxMaYmZruv783OLo9ZdtdvZVKkEmz6aV/iPzYHfO7K97jbTZsuN1kansh+uXnOCyRSXg2H8inJ1qkVNVmxtTVBaPrSXISRUEI2PZbmJtyay9CMpZngkJCAsREyEFIhPW/pjMeJDeog2MjHDUd6j3SxLBZZ+jCqI9dhZKZS0HNOeTZRscrfU1FPY73IV/MlBebJBl9m/bx8bUbW5WP+UordIypp+rXdyc6u09rVrV29t6u/tqt+xG72mn9lNIirCgt+i1Yfwohc37XUb+kk3FbkaCu0g1N7uMs4HVdzSKq9dBVKZy893ZE9Sgav1R5qv5VBJ9sHlG4ru8lgB51hAFrcO9CUD+ogEHQTFK0PByvornlwyD1927uAC52XBQ8OLGF9gKt0zzhkVIxTLKI0mvGM0WZ0GUecc844YxwwOowe5/RoG761Ub9gJ9L1ee829+/FYisSk7J4ShYpHpJxuZqnxck4L1ZJJvA+qizxIbhHmq63/yvq168oKr59bN//sdnBExlbnw==",
            "config": {"product": True},
        },
    ]
    parameters = {"product": {"name": "Product", "type": "checkbox", "default": False}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not black"))
        self.add_program_line(border_color_connected(puzzle.row, puzzle.col, color="black"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="not black"))

            if isinstance(num, int):
                if puzzle.param["product"]:
                    self.add_program_line(cave_product_rule(num, (r, c), color="not black"))
                else:
                    self.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
