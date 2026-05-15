"""The Shimaguni solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import area_color_connected


def adjacent_area_different_size(color: str = "black", adj_type: int = 4) -> str:
    """Generate a constraint to enforce that adjacent areas have different sizes."""
    size_count = f"#count {{R, C: area(A, R, C), {color}(R, C) }} = N"
    size1_count = f"#count {{R, C: area(A1, R, C), {color}(R, C) }} = N1"
    return f":- area_adj_{adj_type}(A, A1), A < A1, {size_count}, {size1_count}, N = N1."


class ShimaguniSolver(Solver):
    """The Shimaguni solver."""

    name = "Shimaguni"
    category = "shade"
    aliases = ["islands"]
    examples = [
        {
            "data": "m=edit&p=7ZZdb9MwFIbv+ysmX/si/oydGzRGx80oHx1CU1RVXZexilYd7YJQqv53XjvHNROTBkIMIaEuzpPT0+M3fo+TbT+3s03DRRH+lOM446OFi4d0Nh4Ffc4Xd8umOuLH7d3NegPg/PXpKb+eLbfNoKasyWDX+ao75t3LqmaCcSZxCDbh3dtq172quiHvxviKcYfYWZ8kgcOMH+L3gU76oCjAI2LgBXC+2MyXzfSsj7yp6u6cszDP8/jrgGy1/tIw0hGu5+vV5SIELmd3uJntzeKWvtm2V+tPLUtT7Hl33MsdPyBXZbnqIFc9LFf+ebl+st9j2d9B8LSqg/b3GV3GcbXbB107pgr8VMLr6AxT6v5lGQo/Y4eAkP5egtAhQ9A1aopY+SKOp3GUcTzHxLxTcXwRxyKOJo5nMWcIPVIoLiWKSvSL0GBHjBYMYiOXYEGM9lSyZ4m4prhEXFNcFWBNLMCGWIItMebSNJcGm8QG7ImhwZIGjfqW6hvkW8o3yCkpxyCnpByLuUqay4YtRfES2hxpK2XYZsSo46mOQ9xT3GEuT3NhS6oi5Xiw6tkjLijuHbifC7lgTazA/TqrsOclxYUAG2IJtsQa7IhLrmj98TswxaUBe2Jo0AUxNJAXyOXKJIZm02tGLpg0aGgzZfZI0X0p9IZKPmIdVPLRw7vkS5F7QIvcAzp4TXVQ/9APBmwSB9+ppgm+2+xp0mPK3BvB39QbxufesNBgSYMVuU9smfskPlKppkPcpXjoDX/w9NADHjU9rXnhD/5G74TI3iWvw5rL5AXyae/gnL3DXlAqeQGv1Xde0BrinL3DGiqdcuCRTn6hB2hP4QymntGhB8I97sOjMWzxkzjqONq49cvwRPrJZ1Z8Wrlwo33NUazzm4+cR7XVqn8b3v+Yfy82GdRs3G6uZ/MGL4/h1cfmaLTerGZLXI3a1WWzSdd4d+8H7CuLR63CvwL/X+d/6XUeLCh+6aX+BHviETk1Vhe7pnvN2W07nU3na/QY1i7GxQ/xJ1ePTT0ZfAM=",
        },
        {"url": "https://puzz.link/p?shimaguni/10/10/tbqnmfcip5kb8m1e2o003v00vesf00v3v6sfzh3", "test": False},
        {
            "url": "https://puzz.link/p?shimaguni/15/12/55a19a6l11nhcnqlddnqkr5cmajmaoeahc3gqv3nftavvke414681sk3e7cekml25fok2o43g1s",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(area_color_connected(color="gray"))
        self.add_program_line(area_adjacent())
        self.add_program_line(adjacent_area_different_size(color="gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            flag = True
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    flag = False
                    self.add_program_line(count(num, color="gray", _type="area", _id=i))

            if flag:
                self.add_program_line(count(("gt", 0), color="gray", _type="area", _id=i))

        for (r, c, d, _), draw in puzzle.edge.items():
            if d == Direction.TOP and r > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r - 1}, {c}).")

            if d == Direction.LEFT and c > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r}, {c - 1}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
