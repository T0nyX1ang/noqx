"""The Snake solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import count, display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route
from noqx.rule.shape import avoid_checkerboard, avoid_rect
from noqx.rule.variety import nori_adjacent


class SnakeSolver(Solver):
    """The Snake solver."""

    name = "Snake"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVNj9owEL3zK1Y+++DPfF0qul16oWzbsFqhCKGQZgVqUGggVWWU/97xJCUbaqldqeW0Mh7Nex7Hz2N7OHyr0yqnXNmfDCijHJr2GXble9hZ1+bbY5FHN3RcHzdlBQ6l95MJfUqLQz5KOM7ly9HJhJEZU/M+SggnlAjonCyp+RSdzIfILKiJYYjQALhpGyTAvevdRxy33m1Lcgb+rPPBXYCbbausyFfTlvkYJWZOiV3nLc62LtmV33PS6bA4K3frrSXW6RE2c9hs993Iof5Sfq3JryUaasat3NghV/Zy5VmudMsV/0RusS9dQsNl00DCP4PUVZRY1Q+9G/RuHJ0aq+hEZGinvgEV7akQxYHQPZQAgx4qgKKHHkDVwwCgPEPNhtC7WMq3H+NnyDkbrMU9Nfi6YGyIpfdMDOyH464WsCvt48gwySSULpbzEGVc0qjeQUsnHfguWjDhpIU7WjqXFModrfXvNOx/glkQaOdw3NRItO/QMrQa7RRj7tA+or1Fq9B6GOPbC/OXVwrTHsC5gjDR3q/np/KftCXap9zZXvmuBCckrqunNMuhZszq3TqvbmZltUsLwPEm3ecEynQzIj8Idnyz6rVyX71y2+SzF9XvK7yvP8hJIK/wAs09Jft6la6yEm4VZM3yvnbzMnwJP7M8/nGIrvK7Ai4nXj1NUImWo58=",
        },
        {"url": "https://puzz.link/p?snake/11/11/00000000000000000000000000000000000000000957664857598o9", "test": False},
        {
            "url": "https://puzz.link/p?snake/15/15/13a3b00000a3d3a00000a3a4a00030a3a3a10000d3aca03001a3a3a10039a3d3a00100j3a39zp",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(shade_c(color="dead_end", _from="gray"))
        self.add_program_line(count(2, color="dead_end"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_rect(2, 2, color="gray"))
        self.add_program_line(fill_line(color="gray"))
        self.add_program_line(single_route(color="gray", path=True))
        self.add_program_line(grid_color_connected(color="gray", adj_type="line"))
        self.add_program_line(nori_adjacent(("le", 2), color="gray", adj_type=4))
        self.add_program_line(avoid_checkerboard(color="gray"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
                self.add_program_line(count(num, color="gray", _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
                self.add_program_line(count(num, color="gray", _type="row", _id=r))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_L__1":
                self.add_program_line(f"gray({r}, {c}).")
                self.add_program_line(f"not dead_end({r}, {c}).")
            if symbol_name == "circle_L__2":
                self.add_program_line(f"gray({r}, {c}).")
                self.add_program_line(f"dead_end({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
