"""The Doppelblock solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import count, display, fill_num, grid, unique_num
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.row == puzzle.col, "Doppelblock puzzles must be square."
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
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

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
            "data": "m=edit&p=7VVRb5swEH7nV1T3fA82JgT8lnXNXjK6LZmqykKIUKpGI6IlYZoc5b/3fLA5qlZNe1i2h+niTx+f78J3NpjdU192NaYUKkGBkkIlgkcSuZ8YY7XZN7W+wFm/f2g7IojX8znel82uDozkWpEHB5tqO0P7ThuQgBDSkJCj/agP9r22GdolTQFGpC2GpJDolac3PO/Y5SBKQTwbOdFbotWmq5q6WAzKB23sCsHd5w1XOwrb9msNow93XbXb9cYJ63JPzeweNo/jzK6/a7/0Y67Mj2hnr9tV3q6jg13HfmLXdfGH7ab58UjL/okMF9o47589TTxd6gNhpg+ghCtNyMuwN6Ak/xft1Q8lckooTpTJSyUaqmKvTLhKeSGevhASvrVMvZIqViKvSBGzND2RqIKk0yQVsp/vCrUmucFbxjljyLii/tEqxreMgnHCuOCcK8YbxkvGiDHmnKlbwd9a4zPYMVHIr6uP+LzXeWBg2Xf3ZVXTc5n123XdXWRtty0boIPgGMA34GEUpUf/z4a/dDa4LRD/2tP7CzvGLlEJtNcIj31RFlXbAH1e8BX97O7p9YPyqashD54B",
        }
    ],
}
