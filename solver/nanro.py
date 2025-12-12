"""The Nanro solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, fill_num, grid
from noqx.rule.helper import fail_false, full_bfs
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect


def nanro_fill_constraint(color: str = "black") -> str:
    """Generate a constraint for the number filling in nanro."""
    return f":- number(R0, C0, N), area(A, R0, C0), #count {{ R, C : area(A, R, C), {color}(R, C) }} != N."


def nanro_avoid_adjacent() -> str:
    """Generate a rule to avoid adjacent cells with the same number."""
    area_adj = area_adjacent()
    area_adj = area_adj[area_adj.find(":-") : -1]
    return f"{area_adj}, number(R, C, N), number(R1, C1, N)."


class NanroSolver(Solver):
    """The Nanro solver."""

    name = "Nanro"
    category = "num"
    examples = [
        {
            "url": "https://puzz.link/p?nanro/11/11/9bdcljmcpj6cpj6dpl6mqi46tt8qpltbdmqnljb2nnc4i3g2l23l2n2n2n2n2i3i2n3n3n3n2l43l2g3i",
            "test": False,
        },
        {
            "data": "m=edit&p=7VdNbxs3FLzrVwR75oHk49fq5qZ2L67T1i6CQBAM2VEaozaUylZRrOH/nnnkUHICFEFRpAWKQtJy3iyXO+9xyF3d/7ZbbdfGOf1KMdYAmRBT/Tnn68/yc3HzcLuevzBHu4f3my2AMa9OTsy71e39erZgr+XscRrn05GZvpsvBjeYwdff0kw/zh+n7+fD/e7t5tfdYKZzdBiMw5nT1tUDHh/g63pe0ctGOgt8BiztsjeA1zfb69v15Wnr+MN8MV2YQe/2Tb1a4XC3+X09UI3G15u7qxslrlYPSOn+/c0HnqE23m75ZKajKno67nLLQa4c5CpschV9Lpf5fGW54/LpCcX/CYIv5wvV/vMBns8fcTybPw7Ba3+toMFVes6BdbYU5WOt7OAw7xqGHsYa7s/mT856l/qYNSz2eSi+jlwLqmGoZ/u1EoKGMEkLxzpUPxubjH7f9OxaCH9TkzqpR1+PF8jWTFKP39ajrcdYj6e1zzHS9cEZr5Xw8GbwwEIswFBUcQCOxBEY0ipOwJk4AyO/igvwSDwaHyFWcbTAjhj31VpWjPsmjpMwTiFfwI/kx2xEawCM1ohvPFoj1I/WSCQfwevkKM7gC/mSTbCNR2uCa3xwWOp7HIFbjsEF4JZ7cALcahKgATExtgpqC84CtxyDHYFb7sEW3LfVJFjV0GoVLO5rqW3EOJa1zahPIS7JiG1jokUdGo/WiJAX8JwXtEYS+QQ+k8/gR/Ij8qIeGQV8y0tG1GpseUlGDUfWMIHP1Im5Rsz7gqcHxIGXPke4F+spqHPHHvVHzBwxv5yXijO9l+G9TO9leC/TexneYy5ogbtn9NqOUTdq8wl+Yx18hA9T9yH8GelP+AQxMcakf6rnex/19n5M9Sp1JuhM1JnQP1Fngs5EnerzjhPGL9RTwOsSr97WWnFe9PnjOV8e/N7nwIF9sGYlsg80SyYPzwg9gxbz232o/qSfLfzZvTTCn7bVRMaCue5+0HlvNcE2BNz9GYE5PvyDmHOB+mTWMKO2mXXLqLlugTVfzEXvr+NwXaBFjo1HixzJB/CRfASfyWfw+3yBC/sU6Nlj+LnQz9hDEBNrfehP6EHMcUbgPj7qQP2C+UV88D/nXbC/7bGgD/c9ceCFvAXvWJMC3tIzwL6wPgX1GVmfUetDb2Af8Fx3tbYdY216rk20wPSezkVfy9hzxDN3D17IC/hIPoJPPUfNnXzSvDqva7znrvsJPQBvIybWcVhz7POIeS/w3P9rfYS8Q5+OLfq4rln1cxyL8bkHogXue4juG6yn7lfEaJEva+71XuTxEieRPJ4vn+CeC9YmYmL1W99LoYHPLPHghdpUv3/Ge/b3umY5jtdnU9cDLLyX6F7d1zL6C3NUvj8T9VnMdV33Ivq8PpfrvoSH9uv66H5Zj6EeU32k53os/UXnz1+A9l3quxAEDPPS3ojaG9DfeZ34gr6n2QKPC32z/vwT/7vscrYYznfbd6vrNV5Wj9/+sn5xttnerW4Rne3urtbbQ3xeX2N7jH8QT7Phj6H+FuoB4+T/vxX/6t8KnQr75T8XX30p/ZWlvpjOsd+Y6ZUZPuwuV5fXG3jNLv9ZwVCJ5b+cfQQ="
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not gray"))
        self.add_program_line(avoid_rect(2, 2, color="not gray"))
        self.add_program_line(nanro_fill_constraint(color="not gray"))
        self.add_program_line(nanro_avoid_adjacent())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i, color="gray"))

            unclued = True
            for r, c in ar:
                if Point(r, c, Direction.CENTER, "sudoku_0") in puzzle.text:
                    unclued = False
                    num = puzzle.text[Point(r, c, Direction.CENTER, "sudoku_0")]
                    fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
                    self.add_program_line(count(int(num), color="not gray", _type="area", _id=i))

                if Point(r, c, Direction.CENTER, "normal") in puzzle.text:
                    unclued = False
                    num = puzzle.text[Point(r, c, Direction.CENTER, "normal")]
                    fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
                    self.add_program_line(f"number({r}, {c}, {num}).")

            if unclued:
                self.add_program_line(count(("gt", 0), color="not gray", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"gray({r}, {c}).")

        self.add_program_line(display(item="gray", size=2))
        self.add_program_line(display(item="number", size=3))

        return self.program
