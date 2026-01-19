"""The Roma solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, count, defined, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, validate_direction
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


def roma_adjacent() -> str:
    """Generate a rule to define the adjacency for roma."""

    # the definition is designed to be compatible with the reachable propagation
    rule = "adj_line_directed(R, C, R, C + 1) :- grid(R, C), arrow_N_W__5(R, C).\n"
    rule += "adj_line_directed(R, C, R, C - 1) :- grid(R, C), arrow_N_W__1(R, C).\n"
    rule += "adj_line_directed(R, C, R + 1, C) :- grid(R, C), arrow_N_W__7(R, C).\n"
    rule += "adj_line_directed(R, C, R - 1, C) :- grid(R, C), arrow_N_W__3(R, C)."
    return rule


class RomaSolver(Solver):
    """The Roma solver."""

    name = "Roma"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VddT9tIFH3nV1Tz2pHWM3b8Je1DoKHbLoTQgrIkQpEJBkwdzDo2dI347z13PCb+SiuxarUPqyjjkzNn7tfY15P133mQhtzFx3S5wQU+piXVVxqe+hr6cxJlcei/4cM8u0lSAM6P9vf5VRCvQ/7x7OZgLxk+vhv+9eBms5l4b+QfjOnt/u3bT6s/P0RmKvbH7uRwchjJ6+Efe7vH9uitPcnXp1n4cLwSu7ens5OryfTak/+MxjOrmB0Zg4+zq98ehqe/78x1DOc7T4XnF0NevPfnTDDOJL6CnfPi2H8qDv3ijBefMcW4AHdQiiTgaAOnap7QXkkKA3isMeAZYJCmyeNivNgtqYk/L044I0e7ajlBtkoeQqYDod/LZHUREXERZKjV+ia61zPr/DL5kmstDLJVHmfRMomTlEjinnkx3J6DucmBYJkDoZ4cKLV6DtOfkAN89OXwjA36hCwW/pwSOt1AdwM/+08Yx2oUajzzn5j0YMXhrcoz0wVtdmhr0EsPDNASWUTpMg4XB5oVYAddsdVvwwYtOrRN6q4Re4uasunSTr8Rx+mn+0vikrpr2+1Xe7KfNvsq5VG1u2JhULm7LoXo2wZs6L7aVqnGE+w6L0w1vlOjocaBGg+UZoQbQNgeFw42EFHhCoxtUxhdyUW4hF2TCw9OCXtWDROP4lYaV2NHbrBNNlENpcFaV691B8DYRqUnXmMba2nDKt7Regd6p9IQX621sRYFVDZdYGyIwsRjz6q1FXYdxKw1HnqtKPPFFbiMUxpGExu6JhSzp+14ZEf79eC3skk5ejo2z8baUoMr9fWXtRtsAZd6XOFX6wU0LxhrRamXBvE1XNkXyMXUuZjIxSr3TtI75QUTr/OyTOCyzrhySQ+gWkt6zUvkbmo9Yant0zuqwhI2ZaXBWql9UT0rLOFLVjbhy6x8IV+zrKfya2q9Cb2p9Sbpy3tA2akwaagfqfgHwNqmBZuWtmmhPpauD/mqMPEDqiEegql6FPbUaKnRVo+IQ23zXzRW6lC15qJeB697Rn8Y5FziXm98cJ/+yt/nO3M2urwO34yTdBXEeHV9vgnuQ4aTA1sn8WKdp1fBMlyEX4Nlxvzy8FKfaXB3+eoixNutRsVJch9Hd30WqqkGGV3fJWnYO0VkiFi3mKKpHlMXSXrZiukxiONmLupY16DKPt+gshQv+tpvdYM0mFWQ3TSI2qGgYSm8axUzC5ohBl+ClrfVphzPO+wrU1+8S9B0/z/m/eePebRZxqt70k/qPj8IZ16M6I1dnjJ4ccTZfb4IFkiN4a8FL6f1wWPb9OtXn3H0xjb/yyukHr0k/U4f3Ey26Z5uCPY7DbE228dv6X212TbfaXQUbLfXge1pd2DbHQ9Ut+mB7PQ9cFtaH1ltdz+Kqt0AyVWnB5Krehucs2UcrNfRkp3vfAM=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_cc(colors=["arrow_N_W__1", "arrow_N_W__3", "arrow_N_W__5", "arrow_N_W__7"]))
        self.add_program_line(roma_adjacent())
        self.add_program_line(avoid_unknown_src(adj_type="line_directed", color="grid"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(("le", 1), color="arrow_N_W__1", _type="area", _id=i))
            self.add_program_line(count(("le", 1), color="arrow_N_W__3", _type="area", _id=i))
            self.add_program_line(count(("le", 1), color="arrow_N_W__5", _type="area", _id=i))
            self.add_program_line(count(("le", 1), color="arrow_N_W__7", _type="area", _id=i))
            fail_false(len(ar) <= 4, "Each room must contain at most four cells.")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_L__2":
                self.add_program_line(f"hole({r}, {c}).")
                self.add_program_line(grid_src_color_connected((r, c), adj_type="line_directed", color="grid"))

            if symbol_name.startswith("arrow_N") and symbol_name.split("__")[1] in ["1", "3", "5", "7"]:
                self.add_program_line(f"{symbol_name.replace('B', 'W')}({r}, {c}).")

        self.add_program_line(display(item="arrow_N_W__1", size=2))
        self.add_program_line(display(item="arrow_N_W__3", size=2))
        self.add_program_line(display(item="arrow_N_W__5", size=2))
        self.add_program_line(display(item="arrow_N_W__7", size=2))

        return self.program
