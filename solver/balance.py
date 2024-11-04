"""The Balance Loop solver."""

from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import direction, display, fill_path, grid, shade_c
from noqx.rule.helper import reverse_op
from noqx.rule.loop import loop_sign, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def balance_rule(color: str = "black") -> str:
    """
    Generate a rule for balance loop.

    A loop_sign rule should be defined first.
    """
    op = "=" if color == "black" else "!="

    # detect the longest straight line
    max_u = '#max { R0: grid(R0 + 1, C), not loop_sign(R0, C, "ud"), R0 < R }'
    min_d = '#min { R0: grid(R0 - 1, C), not loop_sign(R0, C, "ud"), R0 > R }'
    max_l = '#max { C0: grid(R, C0 + 1), not loop_sign(R, C0, "lr"), C0 < C }'
    min_r = '#min { C0: grid(R, C0 - 1), not loop_sign(R, C0, "lr"), C0 > C }'

    rule = f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "lu"), N1 = {max_u}, N2 = {max_l}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "ld"), N1 = {min_d}, N2 = {max_l}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "ru"), N1 = {max_u}, N2 = {min_r}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "rd"), N1 = {min_d}, N2 = {min_r}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "ud"), N1 = {max_u}, N2 = {min_d}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "lr"), N1 = {max_l}, N2 = {min_r}.\n'

    for sign in ["lu", "ld", "ru", "rd"]:
        rule += f':- balance_{color}(R, C, N1, N2), loop_sign(R, C, "{sign}"), |R - N1| {op} |C - N2|.\n'

    # special case for straight line
    rule += f':- balance_{color}(R, C, N1, N2), loop_sign(R, C, "ud"), |R - N1| {op} |R - N2|.\n'
    rule += f':- balance_{color}(R, C, N1, N2), loop_sign(R, C, "lr"), |C - N1| {op} |C - N2|.\n'
    return rule.strip()


def count_balance(target: int, src_cell: Tuple[int, int], color: str = "black", op: str = "eq") -> str:
    """
    Generate a constraint to count the length of "2-way" straight lines.

    A balance loop rule should be defined first.
    """
    rop = reverse_op(op)
    r, c = src_cell
    constraint = ""
    for sign in ["lu", "ld", "ru", "rd"]:
        constraint += (
            f':- balance_{color}({r}, {c}, N1, N2), loop_sign({r}, {c}, "{sign}"), |{r} - N1| + |{c} - N2| {rop} {target}.\n'
        )

    # special case for straight line
    constraint += f':- balance_{color}({r}, {c}, N1, N2), loop_sign({r}, {c}, "ud"), |{r} - N1| + |{r} - N2| {rop} {target}.\n'
    constraint += f':- balance_{color}({r}, {c}, N1, N2), loop_sign({r}, {c}, "lr"), |{c} - N1| + |{c} - N2| {rop} {target}.\n'
    return constraint.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="balance"))
    solver.add_program_line(fill_path(color="balance"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="balance", adj_type="loop"))
    solver.add_program_line(single_loop(color="balance"))
    solver.add_program_line(loop_sign(color="balance"))
    solver.add_program_line(balance_rule(color="black"))
    solver.add_program_line(balance_rule(color="white"))

    for (r, c), symbol_name in puzzle.symbol.items():
        solver.add_program_line(f"balance({r}, {c}).")
        if symbol_name == "circle_L__1__0":
            solver.add_program_line(f"white({r}, {c}).")
            num = puzzle.text.get((r, c))
            if isinstance(num, int):
                solver.add_program_line(count_balance(num, (r, c), color="white"))

        elif symbol_name == "circle_L__2__0":
            solver.add_program_line(f"black({r}, {c}).")
            num = puzzle.text.get((r, c))
            if isinstance(num, int):
                solver.add_program_line(count_balance(num, (r, c), color="black"))

        else:
            raise AssertionError("Invalid symbol found.")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Balance Loop",
    "category": "loop",
    "aliases": ["balanceloop"],
    "examples": [
        {
            "data": "m=edit&p=7VZLa9tAEL77V5g9z2FXL0u6uWnci+s+4hKCEMF2VWIqR6kfJcj4v2dm1o5kzeZQSkugRWiY+Xb30zerT4/Nj91sXYAJIQE/Bg0Gj0jHWGDu+Xzq4zFdbssi7cNwt72r1pgAfBiN4Nus3BS97Dgr7+3rJK2HUL9LM+Up4NOoHOpP6b5+n9ZjqK9wSIFBbIyZUeBhetmk1zxO2YUFjcZ8YvMBpjeYLpbrRVncji3RxzSrp6DoOm94NaVqVf0slF3G9aJazZcEzGdbbGZzt3w4jmx2X6vvu+Nckx+gHr4s12/kUmrlUuaQS138ttxyeV88upQm+eGAO/4Ztd6mGcn+0qRxk16le4yTdK+CCJfGENibooIBMfVVA8QIRM9l5B3HzQnwEQiaMuiMD2h9m3CQ8IJTGeuzMqGyvT4xXaCrwGhqoX0Jo7tdGN2VYTzB41Er50i3G+MTj9+w+NTNGW9w6uAZCQVLGAqEemi20URUhw1HJDqKSElrRkz9tBhi0U1MOlozEmJott4k3V483b45aBjDtrk52cZDS7ZtbN0jUbqOQNlJqKWDkmqJknKBsrUEL/tLoGwzgbLbBC9bTqJOvdZ8gtg60AE7JVsvSm42pAN27oa1puRmh0qYbSph9qrkZsM6YGpewmxeyc0edsBu3exnyc22dsBu3Wxxyc1OF7C1ewdGv4/Y9R7HKb4/ofY5vuWoOYYcxzznkuM1xwuOAceI5wzoDfxL7+j2g/eH5GSB/da/dIT/1mjey9QYv7H9SbVezUr80k52q3mxPtX4V3PoqUfFJ34ODAT/f3T+/o8O7b5+bY/Sa5ODDzfe9XJ2vyjKqnpQee8J"
        },
        {
            "url": "https://puzz.link/p?balance/10/10/q1i8k8k0i1g8h1g9k9h0j1h8k8g0h9g0i1k9k9i0q",
            "test": False,
        },
    ],
}
