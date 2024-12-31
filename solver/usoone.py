"""The Uso-one solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import defined, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def uso_one_constraints(adj_type: int = 4, color: str = "black") -> str:
    """Generate the constraint for Uso-one."""
    count_adj = f"#count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }}"
    rule = "{ wrong_clue(A, R, C) } :- clue(A, R, C, _).\n"
    rule += ":- clue(A, _, _, _), { wrong_clue(A, R, C) } != 1.\n"
    rule += f":- clue(A, R, C, N), not wrong_clue(A, R, C), {count_adj} != N.\n"
    rule += f":- clue(A, R, C, N), wrong_clue(A, R, C), {count_adj} = N.\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="clue", size=4))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="gray"))
    solver.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(uso_one_constraints(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        for rc in ar:
            if rc in puzzle.text:
                r, c = rc
                data = puzzle.text[rc]
                assert isinstance(data, int), "Clue must be an integer."
                solver.add_program_line(f"not gray({r}, {c}).")
                solver.add_program_line(f"clue({i}, {r}, {c}, {data}).")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert d == Direction.CENTER, "The symbol should be placed in the center."
        if symbol_name == "ox_E__1":
            solver.add_program_line(f":- wrong_clue(_, {r}, {c}).")
        if symbol_name in ("ox_E__4", "ox_E__7"):
            solver.add_program_line(f":- not wrong_clue(_, {r}, {c}).")

    solver.add_program_line("ox_E__1(R, C) :- grid(R, C), clue(_, R, C, _), not wrong_clue(_, R, C).")
    solver.add_program_line("ox_E__7(R, C) :- grid(R, C), clue(_, R, C, _), wrong_clue(_, R, C).")
    solver.add_program_line(display(item="gray"))
    solver.add_program_line(display(item="ox_E__1"))
    solver.add_program_line(display(item="ox_E__7"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Uso-one",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VXfT9tIEH7PX4H2eR+8P/xj/QY09IWGu4YTQlEUBTAlaoJpgk/IUf53vpld1zHK6Rqo6FU6JV5/M56d+WZ2d3b1rZouC6ki+ptM4o2fVRk/Okv4icLvfPY4L/IDeVg93pVLACnPTk7k7XS+KnqjYDXurWuX14ey/piPhBJSaDxKjGX9Z76uP+V1X9ZDfBIyg+7UG2nAfgsv+DuhY69UEfAgYMBLwPJpcuSlP/JRfS4FxTjimQTFovy7EIEDydfl4mpGiqvpIxJZ3c0ewpdVdVN+rYKtGm9kfeipDndQNS1Vgp4qoR1UKYNAtf8qqvPZfVE+7aLpxpsNSv0ZRCf5iDj/1cKshcN8jXGQr4VJMVVjfXk1hE0gmu9iHHVF3RUziLQ7vJioztek6yqNO8YpzW3jpg4ibTMvZsSqneuIRjtXRRTJbsnkrDVXqhtaKfreele6m5bSpkNGWftCJn9b8+2LeJbYb9knlGtjj0IrLvcljyc8ah7PsRqyNjx+4DHiMebxlG36WCStjNQaNdE4OArnzyABxg4Y5AnrVGqLwhA2ETCSYIy5Nsy1SuoY5BhbYCTCGHNp+QjHMTASYozznmLRCSeYS4vIGHGzEDfV1A8CxtwszM0Q14W46Bcm8pzxlkZ5bnhLoz0Ho2Fjg43OgH1c6KSJg73VwCEW8bdNLohLi8QY9WnypVwa+xj6uNEj3yb3hHJvMPJtcuc+1/CHTRZsMuqBjQ3qQJuTsEPNXaihQ1wX4jr4aerg4McFPw5+XPDjXFsfqonyeeEN7P3gDez94A0c6oaebJT3Y7RBPUOtNNU2+NHwo4MfqnPYS3iH+mOjXfB2O+bR8pjwNkypZfxgU8HqsmPae5nvMNvb37eXVLatzzcNHJRG87oT8q/0RzgRdCC7v/j30417IzGslrfT6wIXQP/mS3EwKJeL6RzSoFpcFctWHt5NHwqBu3fTE0+CH+5a9v/r+B2vYyp7tNel/PYb463HeVRfSvT7+kyKh2oynVyX2E+oGenRX3+J/r/GZ1+eu/VDiXtsD/2+/n9WXkNcUPvp/ymvHfbvvvtxIYhqVZb31B6fAQ==",
        },
    ],
}
