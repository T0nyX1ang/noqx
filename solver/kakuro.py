"""The Kakuro solver."""

from typing import List, Tuple

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    sums: List[Tuple[int, List[Tuple[int, int]]]] = []

    for (r, c), data in puzzle.sudoku.items():
        if isinstance(data.get(1), int):
            area_points = []
            cur = c + 1
            while cur < puzzle.col and not puzzle.symbol.get((r, cur, Direction.CENTER)):
                area_points.append((r, cur))
                cur += 1

            assert len(area_points) > 0, "Invalid kakuro clue."
            sums.append((int(data[1]), area_points))

        if isinstance(data.get(2), int):
            area_points = []
            cur = r + 1
            while cur < puzzle.row and not puzzle.symbol.get((cur, c, Direction.CENTER)):
                area_points.append((cur, c))
                cur += 1

            assert len(area_points) > 0, "Invalid kakuro clue."
            sums.append((int(data[2]), area_points))

    area_id = 0

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))

    for sum_clue, coord_list in sums:
        solver.add_program_line(area(_id=area_id, src_cells=coord_list))
        solver.add_program_line(fill_num(_range=range(1, 10), _type="area", _id=area_id))
        solver.add_program_line(f":- #sum {{ N: area({area_id}, R, C), number(R, C, N) }} != {sum_clue}.")
        area_id += 1

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(unique_num(_type="area", color="grid"))
    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Kakuro",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VZNb9s8DL7nVxQ66yBK8uct65pdunRbOxSFYQzJliFBGrjIxzA4yH8vSdlO43CHd0DxYtjgmCEfyeJDUl/LyXK3rjQY+rlU4z8+HlJ+bRrza5rnbrF9nOUXerjbzqs1KlrfjEb6++RxMxsUTa9ysK+zvB7q+l1eKFBaWXxBlbr+mO/r93k91vUtNikNiF2HThbVq6N6z+2kXQYQDOpj1F347AHVQD7YH/KivtOKvLzhb0lVq+rHTDUsyP5araYLAqaTLYaymS+empbN7lu13DV9oTzoevhrsu5IltRAlrQ+2SaaVyVry8MBU/4J6X7JC2L++aimR/U236Mc53vlE/oUqwJcF0QB0cxahiOlPfrIbEymbyxnuDFrzDhj721rxq1JsMDgGNQZPTQ2D2WxdMGOuLs72p5Hw2CCnTDBdnS009P2zLHdkAFAWjR+2w4+sGv9Q8p84tbMeLiWrTUcN3Q2MLvOu4XgrWVrseXE9sDeTWvHbHfebRaiadk59PQyGw5CdC0913zf8vEYV5dNrNUD1oqrYXU3qXCSKUfdsKInGIXWxyicPkYh9TFKWh+jQvYxCqePUUh9jIrSw7zg1wt+veA3EuKNhHgjId5I4BcJ/GLKcx8TuMRCDhKBSyJw4cnew1LBRybEC0YgCEbwAkZINa48CRSc4xoUQF4JZ6CQR7BCwkGaiSBNJ1wDEih9Ls0o4P3mDJTyGUmxRxIlaQqBNIcglijFZ5nHpT3iLdqyvMNdW9eO5VuWhmXE8pr7XLG8Z3nJ0rOMuU9C+/5/OhnCSRD2mFeiU7hwxTh9oj8PKweFGu9W09n6YlytV5NHPJtv+Vx+Yc8nTzOFF6LDQP1U/BaO7lf/7kj/wx2J0m9+ez3wuVnf/B2rFCdsV41y8Aw=",
        },
        {
            "url": "https://puzz.link/p?kakuro/15/15/m-dm.ffl-7l9-mQjmIBmbam-anWZs.jSpBjo.7goP4lJ9m..nAjo74lf-.lUUrF9l7-qHNq-clKTrO4l.-clgIoibn.JbmHglfgo.gOo7NpA-.s7Hnb-m-fm-7m-7m-hl-4l.-Dm-Em46BfgJjhSK79acVZD",
            "test": False,
        },
    ],
}
