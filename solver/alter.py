"""The Alternation solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, count, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent


def alternation_constraint() -> str:
    """Generates a rule to ensure that the colors alternate."""

    # three shapes do not appear in the same row or column
    rule = ":- grid(R, C0), grid(R, C1), grid(R, C2), ox_E__1(R, C0), ox_E__2(R, C1), ox_E__3(R, C2).\n"
    rule += ":- grid(R0, C), grid(R1, C), grid(R2, C), ox_E__1(R0, C), ox_E__2(R1, C), ox_E__3(R2, C).\n"

    # the same row and column does not only contain one of the three shapes
    rule += ":- grid(R, C), ox_E__1(R, C), not ox_E__2(R, _), not ox_E__3(R, _).\n"
    rule += ":- grid(R, C), ox_E__2(R, C), not ox_E__1(R, _), not ox_E__3(R, _).\n"
    rule += ":- grid(R, C), ox_E__3(R, C), not ox_E__1(R, _), not ox_E__2(R, _).\n"

    # color alternation rules
    rule += ":- grid(R, C), ox_E__1(R, C), grid(R, C1), ox_E__1(R, C1), C1 > C, #count { C0: grid(R, C0), ox_E__2(R, C0), C0 > C, C0 < C1; C0: grid(R, C0), ox_E__3(R, C0), C0 > C, C0 < C1 } = 0.\n"
    rule += ":- grid(R, C), ox_E__2(R, C), grid(R, C1), ox_E__2(R, C1), C1 > C, #count { C0: grid(R, C0), ox_E__1(R, C0), C0 > C, C0 < C1; C0: grid(R, C0), ox_E__3(R, C0), C0 > C, C0 < C1 } = 0.\n"
    rule += ":- grid(R, C), ox_E__3(R, C), grid(R, C1), ox_E__3(R, C1), C1 > C, grid(R, C1), #count { C0: grid(R, C0), ox_E__1(R, C0), C0 > C, C0 < C1; C0: grid(R, C0), ox_E__2(R, C0), C0 > C, C0 < C1 } = 0.\n"
    rule += ":- grid(R, C), ox_E__1(R, C), grid(R1, C), ox_E__1(R1, C), R1 > R, grid(R1, C), #count { R0: grid(R0, C), ox_E__2(R0, C), R0 > R, R0 < R1; R0: grid(R0, C), ox_E__3(R0, C), R0 > R, R0 < R1 } = 0.\n"
    rule += ":- grid(R, C), ox_E__2(R, C), grid(R1, C), ox_E__2(R1, C), R1 > R, grid(R1, C), #count { R0: grid(R0, C), ox_E__1(R0, C), R0 > R, R0 < R1; R0: grid(R0, C), ox_E__3(R0, C), R0 > R, R0 < R1 } = 0.\n"
    rule += ":- grid(R, C), ox_E__3(R, C), grid(R1, C), ox_E__3(R1, C), R1 > R, grid(R1, C), #count { R0: grid(R0, C), ox_E__1(R0, C), R0 > R, R0 < R1; R0: grid(R0, C), ox_E__2(R0, C), R0 > R, R0 < R1 } = 0.\n"

    return rule.strip()


class AlterSolver(Solver):
    """The Alternation solver."""

    name = "Alternation"
    category = "var"
    aliases = ["alternation"]
    examples = [
        {
            "data": "m=edit&p=7VNNb9swDL37VxQ886APp5F0Sztnl65fSVEEhhG4rbcEc+A0iYtCgf97KdmNii5Ah2Abehhk0U9PEvVEkevHOl8VGFOTChly1zTzXXP3sa6N55uyMEc4qDezakUA8WI4xO95uS4wSrtlWbS12tgB2q8mBQ4IgjqHDO2V2dpvxiZoRzQFyDOERV1u5vdVWa3glbNn7UZBMAnw1s87dNqSnBE+7zDBCcHqeXrSji5NascI7twTv9NBWFRPBXS63Pi+WtzNHXGXb+h269l8CShpYl0/VD9rePXeoB206ie/qV4G9XKnXu5XL4L65M+r11nT0KNck/6pSd1VbgJUAY7MtnGSnOXeTswWBCc3HENkQfSJkW8ZGb9fI4/fM7EgRgSG3A/9IcLbMWlAK7394i3ztuftmV+TkBzFUZEncqQEauaRy1TVIoVat0hThLtpsYMqRt3tlqhij/o9VDLsocuJxr2XO/HU29jbY6+k72J1eDQ5qUsVhpcGwXbRTA6Py4eKU67a0sbe/n8WpZA8/CiOzqvVIi8pw0azfFkA1XMTwTP4TkLF/xL/pCXuHogdnJp/Ke8+kJNSsIVGe4GwrKf5lAINlGD4KXm2n+e/rv/nUaYCz6IX",
        },
        {
            "data": "m=edit&p=7ZZdb9sgFIbv8ysqrrkADmDsu7ZLd9N1H+00VVFUpWu2RkvkLh9T5Sj/fS/4OMTVpE3VLjppcgwPx3DOywETr75vJsup1Cr+KEjUuKwO6TbBp1vxdTVbz6fVkTzerO/rJUDKt2dn8stkvprKwYi7jQfbpqyaY9m8rkZCCykMbi3GsnlfbZs3VTOUzSUeCanHUiw28/Xscz2vl6KzNeftQAMcZvyUnkc6bY1agS+YgdfA+vHmpG29q0bNlRQx7kkaGVEs6h9Twbpi+3O9uJ1Fw+1kjdmt7mcPQhIerDZ39beN6LzvZHPcqr/+Q/WU1dNePf1avcnqh39ffTne7bAoH6D/phrFqXzMGDJeVttdlBRLncrraiushxsjc2aFM08tpX5q0aRg0n1T9ETZhABnKYxJ5RVUyIZS+SqVKpUuleepzxCCDJXSWLhHQNRg3bIpMmuSaGe7CczY1tbwWAMmZvR33N+hv+P+1vbZupZJHzA0UKcB2oi1aYe4JY8Fx0ym/iZzfM2I9Tiw4/4Ofjz78fDv2b8tMhM0W9asY1zKfWynOc63zLlylv3HebF+B22e+3j4CewnmD6XrLn0knSrjVSZ2ZAkY5ktuPVPWvdZ83zLcMDQXLLmgHmVBftxkqjVhlqSo8y2i+v7bLqxBextrlCDDbOBH896wJp9Ys+QZv066g/sJ+zHmmAPdIID5zC4eFQyQ4Pq8qP6PnWXB8xLswZl9mwCYqkuFnISwt4n2i0XWMfQrSPshcq838NY94L9FCZri3up4LGF3ftHfOSZNWM/k2XN2PPE+xw18tathc72yLyHUYO7fIZsV3HuHEshz4o1BKyjoj2bkudS+ANGbgufNRecc2+yPbKPfnbxqI1HxWkqbSp9OkKKeMw9+yB83mn1Wzkjav90+5f792zjwUgM775Ojy7q5WIyxz/U5f3kYSrwPbAbiEeRbhz/5v8nwgv9RIgLpF7a+/HS5OCNHQ9+Ag==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(colors=["ox_E__1", "ox_E__2", "ox_E__3", "white"]))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(alternation_constraint())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(1, color="ox_E__1", _type="area", _id=i))
            self.add_program_line(count(1, color="ox_E__2", _type="area", _id=i))
            self.add_program_line(count(1, color="ox_E__3", _type="area", _id=i))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            symbol, style = symbol_name.split("__")
            validate_type(symbol, ("ox_B", "ox_E"))
            fail_false(style in ["1", "2", "3", "4", "7", "8"], f"Invalid symbol at ({r}, {c}).")
            if style in ["1", "2", "3"]:
                self.add_program_line(f"ox_E__{style}({r}, {c}).")
            else:
                self.add_program_line(f"white({r}, {c}).")

        self.add_program_line(display(item="ox_E__1"))
        self.add_program_line(display(item="ox_E__2"))
        self.add_program_line(display(item="ox_E__3"))

        return self.program
