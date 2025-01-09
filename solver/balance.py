"""The Balance Loop solver."""

from typing import List, Tuple

from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import validate_direction
from noqx.rule.loop import loop_segment, loop_sign, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def balance_rule() -> str:
    """Generate a balance rule."""
    rule = ':- black(R, C), segment(R, C, N1, N2, "T"), |R - N1| = |C - N2|.\n'
    rule += ':- black(R, C), segment(R, C, N1, N2, "V"), |R - N1| = |R - N2|.\n'
    rule += ':- black(R, C), segment(R, C, N1, N2, "H"), |C - N1| = |C - N2|.\n'
    rule += ':- white(R, C), segment(R, C, N1, N2, "T"), |R - N1| != |C - N2|.\n'
    rule += ':- white(R, C), segment(R, C, N1, N2, "V"), |R - N1| != |R - N2|.\n'
    rule += ':- white(R, C), segment(R, C, N1, N2, "H"), |C - N1| != |C - N2|.\n'
    return rule.strip()


def count_balance(target: int, src_cell: Tuple[int, int]) -> str:
    """
    Generate a constraint to count the length of "2-way" straight lines.

    A balance loop rule should be defined first.
    """
    r, c = src_cell
    rule = f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| + |{c} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "V"), |{r} - N1| + |{r} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "H"), |{c} - N1| + |{c} - N2| != {target}.\n'
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="black"))
    solver.add_program_line(defined(item="white"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="balance"))
    solver.add_program_line(fill_path(color="balance"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="balance", adj_type="loop"))
    solver.add_program_line(single_loop(color="balance"))
    solver.add_program_line(loop_sign(color="balance"))

    for (r, c, d, _), symbol_name in puzzle.symbol.items():
        validate_direction(r, c, d)
        solver.add_program_line(f"balance({r}, {c}).")
        solver.add_program_line(loop_segment((r, c)))

        if symbol_name == "circle_L__1":
            solver.add_program_line(f"white({r}, {c}).")
            num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
            if isinstance(num, int):
                solver.add_program_line(count_balance(num, (r, c)))

        if symbol_name == "circle_L__2":
            solver.add_program_line(f"black({r}, {c}).")
            num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
            if isinstance(num, int):
                solver.add_program_line(count_balance(num, (r, c)))

    solver.add_program_line(balance_rule())
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
        {"url": "https://puzz.link/p?balance/10/10/q1i8k8k0i1g8h1g9k9h0j1h8k8g0h9g0i1k9k9i0q", "test": False},
        {"url": "https://puzz.link/p?balance/10/10/0g00zg0l0m0k0k0k0k0h0m0k0n0l0h", "test": False},
    ],
}
