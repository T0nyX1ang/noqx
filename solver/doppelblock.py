"""The Doppelblock solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import count, display, fill_num, grid, unique_num
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.row == puzzle.col, "This puzzle must be square."
    n = puzzle.row

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=range(1, n - 1), color="black"))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(count(2, _type="row", color="black"))
    solver.add_program_line(unique_num(_type="col", color="grid"))
    solver.add_program_line(count(2, _type="col", color="black"))

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top number
        assert isinstance(num, int), "TOP clue should be integer."
        begin_r = f"Rb = #min {{ R: black(R, {c}) }}"
        end_r = f"Re = #max {{ R: black(R, {c}) }}"
        solver.add_program_line(f":- {begin_r}, {end_r}, #sum {{ N: number(R, {c}, N), R > Rb, R < Re }} != {num}.")

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left number
        assert isinstance(num, int), "LEFT clue should be integer."
        begin_c = f"Cb = #min {{ C: black({r}, C) }}"
        end_c = f"Ce = #max {{ C: black({r}, C) }}"
        solver.add_program_line(f":- {begin_c}, {end_c}, #sum {{ N: number({r}, C, N), C > Cb, C < Ce }} != {num}.")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")

    for (r, c), num in filter(
        lambda x: x[0][0] < n and x[0][0] >= 0 and x[0][1] < n and x[0][1] >= 0, puzzle.text.items()
    ):  # filter center number
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

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
