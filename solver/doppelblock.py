"""The Doppelblock solver."""

from typing import List

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import count, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)

    fail_false(puzzle.row == puzzle.col, "This puzzle must be square.")
    n = puzzle.row
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=range(1, n - 1), color="black"))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(count(2, _type="row", color="black"))
    solver.add_program_line(unique_num(_type="col", color="grid"))
    solver.add_program_line(count(2, _type="col", color="black"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")

        if r == -1 and 0 <= c < n and isinstance(num, int):
            begin_r = f"Rb = #min {{ R: black(R, {c}) }}"
            end_r = f"Re = #max {{ R: black(R, {c}) }}"
            solver.add_program_line(f":- {begin_r}, {end_r}, #sum {{ N, R: number(R, {c}, N), R > Rb, R < Re }} != {num}.")

        if c == -1 and 0 <= r < n and isinstance(num, int):
            begin_c = f"Cb = #min {{ C: black({r}, C) }}"
            end_c = f"Ce = #max {{ C: black({r}, C) }}"
            solver.add_program_line(f":- {begin_c}, {end_c}, #sum {{ N, C: number({r}, C, N), C > Cb, C < Ce }} != {num}.")

        if 0 <= c < n and 0 <= r < n:
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            solver.add_program_line(f"number({r}, {c}, {num}).")

    for (r, c, _, _), color in puzzle.surface.items():
        fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
        solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="number", size=3))
    solver.add_program_line(display(item="black", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Doppelblock",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7ZXfb5swEMff+Suqe74HGzsE/JZ1zV4yui2ZqspCEWFUjUZES8I0Ocr/3vOBCup+aHtY+jI5/urLx2dyZ8fO/rHNmxITaipGgZKaigX3WPuP6Ntqe6hKc4Gz9nBfN2QQr+dzvMurfRlYyXNFFhxdYtwM3TtjQQJCSF1Chu6jObr3xqXoljQEqIktuqCQ7NVgb3jcu8sOSkE+7T3ZW7LFtimqcr3oyAdj3QrBf88bnu0t7OpvJfR5+Oei3m22HmzyAxWzv98+9CP79kv9te1jZXZCN/t1umpI19suXe9+kq6v4h+nm2SnEy37J0p4bazP/fNg48EuzZE0NUdQwk+NKZdub0BJfhft1TPRnoRiRCYvie5mRSMSeqIGMOHXjEA0fQFizkUmA0kUEz0QKSJG0xGiGYTGQYq//LkGqlVyxbesc9aQdUULgk6xvmUVrBPWBcdcsd6wXrJq1ohjpn5J/3DRQVNBulv6MyRldcineGjReZ+zwMKybe7yoqSfa9ruNmVzkdbNLq+A7odTAN+Bu1UUrv9fGa90ZfgtEH91cbz+kbJuiUqgu0Z4aNf5uqgroH8d/B3X6gd+9qroWEL+2JSQBU8=",
        }
    ],
}
