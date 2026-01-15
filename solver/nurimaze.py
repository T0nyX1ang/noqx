"""The Nurimaze solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, display, fill_line, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_same_color
from noqx.rule.reachable import border_color_connected, grid_color_connected
from noqx.rule.route import directed_route
from noqx.rule.shape import avoid_rect


class NurimazeSolver(Solver):
    """The Nurimaze solver."""

    name = "Nurimaze"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZffT9tIEMff+Ssqv3al83r9Yx3pHlIKvfYg0ALimihChhpIm2DOiWnPiP+931nPkDgx7V0fqjvplMSZjGd2v2PPZ72Z/1llZa60T29jFb7xCrV1n8DG7uPz63iymOa9Z6pfLa6LEoZSB7u76jKbznP15v313nbR//yy/8edXQyH+pVfvfZPP+5+fP5u9vvriSn17sAe7h/uT4Kr/m/bL97GO8/jw2p+ssjv3s70i48nw+PLw9OrNPhrZzAM6+GBH70ZXv5y1z/5dWvEGsZb93Xaq/uqftUbedpTXoCP9saqftu7r/d79Y6qj3DKU3asvFk1XUwuimlRes6nEbfXJAYwd5bmqTtP1nbj1D7sAdsw38O8mJQX0/xsr/Ec9kb1sfJo7hcum0xvVtzlNBlpo98Xxex8Qo7zbIHLN7+e3HrK4MS8+lB8qjhUjx9U3W8qOJIKoOZbFWAQqYDMpgKyOiqgwlYq2P+hCqaTm/xLh/h0/PCA+/IO8s96I6rkZGnapXnUu8dx0Lv3rKXUI6hobp6n/YQ8r8SDOO2i3yPaxDgH/6KcVLes3YtoCDhbFXkJe1uh2oRd3pC97RF01DWbjqMNL9TtOo2BOx6jSFUbd3zpjr47Ru6452J2UE2gAxUEmCRA82oDG6U7O4QN/c6OYKdsg0Ljs53A1myDUBOwncI2jR0gPuT4APEhxweIDzk+QHzI8caHjWvhbA0bpTobOkPWaaAzZJ0GOkPWGSI34twQuRHnhoiPOD5EPN0tZ6OuiOsKoTNmnSF0xqwzQkzMMRFiEo6JEJNIDGpJuJYItSRcSww9CeuJoSdhPTFqSbiWmFY2zk0Qbzk+Qbzl+ATxluMT1GK5lgTaLGuziEk5xiIm5RiLelOu1yI+lfhYGZ9rsQlsrsVa2KzHprC5lhRLss/aUuRqzk2Rqzk3Ra7m3BS5usnFPLCbXMwDu6kL88BuNGMe2I1mzAO70Yx5lAk4F71quFcxNmyOR68a7lWMpwz3J8aD3WjDGLA5JohgN9cBYyjDPYkxYDf6DXrScE9iPNisAT1puCcNetJwT2JsZSLONciNOBc9abgnMQ9szg2RS3A7G7Vwf2Ie2KwT/Wm4PzGPMtKf0P/ILPElzBJfwizxJcwSU8IpMSWcElPCKTFFK5MwZYQ7YlO4IDZ5HOJL+EUtj/wSa8Iv8SXMEl/CbEjsC1PEJsdHxCbPS9zx9XHcCb/EmjBLfAmnxFfMeoivWBgklvmaEGvCMrEm/BJrwi/xJcwm0CPMEmvCrCU2hRFik+ci7oRf4k74Je6EX7eLETahjR4+zN2SZVzzVPiCzlT4QrywTHwxv44v5tfxxfw6pphZx5Qv3BGbwgixybma2ORcYk34JdaEX2JN+MVz4ZFf4k74Je4e+aU1QVgjTjmXGBSW0cOPLBOD3LeOQWGZuOO+ddxx3xpDjPNcxB33quNOuCbuhGviTrgm1oRl4sv1Jx6Mp+7xuO2OoTvG7rGZ0M7hb+4tPIaA+so2G43VbcSPPa6/q20E1GnT3H5F/z3feAs7sqq8zC5ybPz2sNd7NijKWTbFr50PVyu/BtXsPC+Xv4+us9vcw9bcmxfTs3kzxln+JbtYeL3m38HqmZbvxo3Vck2L4pa2mh0jyKmWc3J1U5R55yly5tD+xFB0qmOo86L8sKbpczadtmtx/5xarmYf2XJht9j6nZVl8bnlmWWL65Zj5W9Ca6T8Zu1iLrK2xOxTtjbbbHk5Hra8L577jLBi0s3+/3/Uv/N/FN0j/x/9m/oJi9x35IxwrbFLqA+Ud1udZWe4zu5SkR8rftuPsjv9YePfGCdq/NiRt/3xE+O4efdUjEdc+wRuIyXgkdUpaMPvBHUP9NOvv+O5KL+xuC5Prrs7llh4v7HKrpzt8j+xoK6cXfdvrJ4kdnMBhbdjDYV3fRmFa3MlhXNjMYXvifWURl1fUknV+qpKU20srDTV6to68m6qcjLL6iE9Br8C"
        },
        {
            "url": "https://puzz.link/p?nurimaze/10/10/vvvvvtv6rtlrvrvvvuvtvrvvvvvvrnvv7fvve3m3845394c3c2k4946371a46",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line("{ white(R, C) } :- grid(R, C), not gray(R, C).")  # select from non-gray cells
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(adjacent(_type="line_directed"))
        self.add_program_line(area_same_color(color="gray"))
        self.add_program_line(border_color_connected(puzzle.row, puzzle.col, color="gray", adj_type=8))
        self.add_program_line(avoid_rect(2, 2, color="gray"))
        self.add_program_line(avoid_rect(2, 2, color="not gray"))
        self.add_program_line(grid_color_connected(color="not gray", adj_type=4))
        self.add_program_line(fill_line(color="white", directed=True))
        self.add_program_line(directed_route(color="white", path=True))
        self.add_program_line(grid_color_connected(color="white", adj_type="line_directed"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, (ar, _) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if clue == "S":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"path_start({r}, {c}).")

            if clue == "G":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"path_end({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__1":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"white({r}, {c}).")

            if symbol_name == "triup_M__1":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"not white({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))
        self.add_program_line(display(item="line_in", size=3))
        self.add_program_line(display(item="line_out", size=3))

        return self.program
