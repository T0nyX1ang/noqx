"""The Kakuro solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, defined, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, validate_direction


class KakuroSolver(Solver):
    """The Kakuro solver."""

    name = "Kakuro"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VZNb9s8DL7nVxQ66yBK8uct65pdunRbOxSFYQzJliFBGrjIxzA4yH8vSdlO43CHd0DxYtjgmCEfyeJDUl/LyXK3rjQY+rlU4z8+HlJ+bRrza5rnbrF9nOUXerjbzqs1KlrfjEb6++RxMxsUTa9ysK+zvB7q+l1eKFBaWXxBlbr+mO/r93k91vUtNikNiF2HThbVq6N6z+2kXQYQDOpj1F347AHVQD7YH/KivtOKvLzhb0lVq+rHTDUsyP5araYLAqaTLYaymS+empbN7lu13DV9oTzoevhrsu5IltRAlrQ+2SaaVyVry8MBU/4J6X7JC2L++aimR/U236Mc53vlE/oUqwJcF0QB0cxahiOlPfrIbEymbyxnuDFrzDhj721rxq1JsMDgGNQZPTQ2D2WxdMGOuLs72p5Hw2CCnTDBdnS009P2zLHdkAFAWjR+2w4+sGv9Q8p84tbMeLiWrTUcN3Q2MLvOu4XgrWVrseXE9sDeTWvHbHfebRaiadk59PQyGw5CdC0913zf8vEYV5dNrNUD1oqrYXU3qXCSKUfdsKInGIXWxyicPkYh9TFKWh+jQvYxCqePUUh9jIrSw7zg1wt+veA3EuKNhHgjId5I4BcJ/GLKcx8TuMRCDhKBSyJw4cnew1LBRybEC0YgCEbwAkZINa48CRSc4xoUQF4JZ6CQR7BCwkGaiSBNJ1wDEih9Ls0o4P3mDJTyGUmxRxIlaQqBNIcglijFZ5nHpT3iLdqyvMNdW9eO5VuWhmXE8pr7XLG8Z3nJ0rOMuU9C+/5/OhnCSRD2mFeiU7hwxTh9oj8PKweFGu9W09n6YlytV5NHPJtv+Vx+Yc8nTzOFF6LDQP1U/BaO7lf/7kj/wx2J0m9+ez3wuVnf/B2rFCdsV41y8Aw=",
        },
        {
            "url": "https://puzz.link/p?kakuro/15/15/m-dm.ffl-7l9-mQjmIBmbam-anWZs.jSpBjo.7goP4lJ9m..nAjo74lf-.lUUrF9l7-qHNq-clKTrO4l.-clgIoibn.JbmHglfgo.gOo7NpA-.s7Hnb-m-fm-7m-7m-hl-4l.-Dm-Em46BfgJjhSK79acVZD",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        sums: List[Tuple[int, List[Tuple[int, int]]]] = []
        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            if pos == "sudoku_1" and isinstance(num, int):
                area_points: List[Tuple[int, int]] = []
                cur = c + 1
                while cur < puzzle.col and not puzzle.symbol.get(Point(r, cur, Direction.CENTER)):
                    area_points.append((r, cur))
                    cur += 1

                fail_false(len(area_points) > 0, f"Invalid kakuro clue at ({r}, {c}).")
                sums.append((num, area_points))

            if pos == "sudoku_2" and isinstance(num, int):
                area_points: List[Tuple[int, int]] = []
                cur = r + 1
                while cur < puzzle.row and not puzzle.symbol.get(Point(cur, c, Direction.CENTER)):
                    area_points.append((cur, c))
                    cur += 1

                fail_false(len(area_points) > 0, f"Invalid kakuro clue at ({r}, {c}).")
                sums.append((num, area_points))

            if pos == "normal" and isinstance(num, int):
                self.add_program_line(f"number({r}, {c}, {num}).")  # initial conditions

        self.add_program_line(defined(item="area", size=3))
        self.add_program_line(defined(item="number", size=3))
        self.add_program_line(grid(puzzle.row, puzzle.col))

        area_id = 0
        for sum_clue, coord_list in sums:
            self.add_program_line(area(_id=area_id, src_cells=coord_list))
            self.add_program_line(fill_num(_range=range(1, 10), _type="area", _id=area_id))
            self.add_program_line(f":- #sum {{ N, R, C: area({area_id}, R, C), number(R, C, N) }} != {sum_clue}.")
            area_id += 1

        self.add_program_line(unique_num(_type="area", color="grid"))
        self.add_program_line(display(item="number", size=3))

        return self.program
