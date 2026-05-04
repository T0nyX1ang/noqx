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
            "data": "m=edit&p=7VZLb9NAEL7nV1R73sPOPry2b6E0XEoKJKhCloUSCEqURK7yQMiR/zuzYzuO6fRQpAohkOPJzLeP+WY8+1jP1sddIUGFn4kl/uNjIaZXxxG9qnmmq8NmkV7J4fGwLHaoSHk3Gslvs81+MciaXvngVCZpOZTlmzQTIKTQ+ILIZfk+PZVv03Isywk2CQmI3dadNKo3nXpP7UG7rkFQqI9RN/WwT6iuiXxtv0uzcipF8PKKxgZVbIvvC9GwCPaXYjtfBWA+O2Ao++XqoWnZH78W62PTF/JKlsOnyZqOrDmTNQzZJpoXJavzqsKUf0C6n9MsMP/YqXGnTtJTFVidhPVhKH4VoO+CKCCaaE2wE9Kij0RHwbSNZRQ1Jo0ZJeS9bU2o1dcWKJwjdNZnm6bSprUddTedbWk2aG3vL2dHO+63J4bshgyAJja6bQdbs2v9Q0x8otZM4ku2WlHccLZB9bxrqL2Zs237tgXyrlo7gp53nfgeewO+lw0DdXQtPdOMb/lYDV02q1BMJ0FfQ8tzUWGRCRO6wS+YZjDDYJbBHINFDOYZLGaw5DFmGb+W8WsZv46J1zHxOiZex/BzDL9IMRjDJWJy4BkunuHimbEx4yNh4gXFEATFeAHFpBpXHgcyznENMiBwcwKTR9BMwoGrRODKCdcAB3LDuYoCx2WJqx9wXOyOo8SVEHA1BBFHKXqUeVzaI9qiNckp7tqyNCRfk1QkHclb6nND8p7kNUlLMqI+Puz7zzoZ6pOg3mNeiE5m6itG/3F/H5YPMjE+bueL3dW42G1nGzybJ3QuX9jL2cNC4IWoGogfgt7MhPvV/zvSH7gjhfSr314PdG6Wd//GKsWCzfLBTw==",
        },
        {
            "url": "https://puzz.link/p?kakuro/15/15/m-dm.ffl-7l9-mQjmIBmbam-anWZs.jSpBjo.7goP4lJ9m..nAjo74lf-.lUUrF9l7-qHNq-clKTrO4l.-clgIoibn.JbmHglfgo.gOo7NpA-.s7Hnb-m-fm-7m-7m-hl-4l.-Dm-Em46BfgJjhSK79acVZD",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        sums: List[Tuple[int, List[Tuple[int, int]]]] = []
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            if label == f"corner_{Direction.TOP_RIGHT}" and isinstance(num, int):
                area_points: List[Tuple[int, int]] = []
                cur = c + 1
                while cur < puzzle.col and not puzzle.symbol.get(Point(r, cur, Direction.CENTER)):
                    area_points.append((r, cur))
                    cur += 1

                fail_false(len(area_points) > 0, f"Invalid kakuro clue at ({r}, {c}).")
                sums.append((num, area_points))

            if label == f"corner_{Direction.BOTTOM_LEFT}" and isinstance(num, int):
                area_points: List[Tuple[int, int]] = []
                cur = r + 1
                while cur < puzzle.row and not puzzle.symbol.get(Point(cur, c, Direction.CENTER)):
                    area_points.append((cur, c))
                    cur += 1

                fail_false(len(area_points) > 0, f"Invalid kakuro clue at ({r}, {c}).")
                sums.append((num, area_points))

            if label == "normal" and isinstance(num, int):
                self.add_program_line(f"number({r}, {c}, {num}).")  # initial conditions

        self.add_program_line(defined(item="area", size=3))
        self.add_program_line(defined(item="number", size=3))
        self.add_program_line(grid(puzzle.row, puzzle.col))

        for area_id, (sum_clue, coord_list) in enumerate(sums):
            self.add_program_line(area(_id=area_id, src_cells=coord_list))
            self.add_program_line(fill_num(_range=range(1, 10), _type="area", _id=area_id))
            self.add_program_line(f":- #sum {{ N, R, C: area({area_id}, R, C), number(R, C, N) }} != {sum_clue}.")

        self.add_program_line(unique_num(_type="area", color="grid"))
        self.add_program_line(display(item="number", size=3))

        return self.program
