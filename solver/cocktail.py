"""The Cocktail Lamp solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import area_color_connected, grid_color_connected
from noqx.rule.shape import avoid_rect


class CocktailSolver(Solver):
    """The Cocktail Lamp solver."""

    name = "Cocktail Lamp"
    category = "shade"
    aliases = ["cocktaillamp"]
    examples = [
        {
            "data": "m=edit&p=7VZNbxs3FLzrVxg8E8iSj5+6FG5q9+I6be2iCATBkBUlMWJDqWwVxRr67xlyZ01skSINgqaXQFjukDt6b/ZxSO79H/vVbqONaGO0JN1pg58Xq50P2thYr46/y5uH2838SB/vH95udwBavzg91a9Xt/eb2YKs5eyxz/P+WPc/zhfKKK0sLqOWuv9l/tj/NO9PdH+BR0onjJ0NJAt40uDv9XlBz4dB0wGfEwO+BFzf7Na3m6uzYeTn+aK/1Krk+b7+u0B1t/1zo6ij9Nfbu+ubMnC9esDL3L+9ec8n9/tX23d7NaY46P54kHvxEbnS5MqTXPm4XPvfy83LwwFl/xWCr+aLov23BlODF/PHQ9H1qCTgr2W268woSejap67z6JrWTZOuzxNylMnTFCfdPO0aY6Z9O01lJE/7rvSl9cM0m4klvvpOtZE8zWA7M5Fru+mrW+MnEVAgU8v0srantbW1vUQVdS+1/aG2XW19bc8q5wTFtdFpW2RYhI8e2BJHYDfgZIEzsdPSkZ88MPkZi7JLxEGLEeIE7IkzcKgYMYAHvphOi43EFjgTixbpiJFLhlxiEd8JcQR2xIjvGF+g0xti8D35DjEDYzpoC4M28dAQqMFDW6A2D34kP0BbpLaA+InxA7QlagvQk6gnIm9m3ohcmbkidGbqTMiVmSsF7Trys2hnmDd74CG+6zrgSIy9z2Ri8O3Ad8ZpJ4YYMUWII7AjzsCDBmeTdm7Q5gTxHeOLAU7EiO8ZH7uv8+Q75ArM5aAzUKdDrsBcHjoDdXrwI/ke/Dj6p3hs9Iw078FLNkfi4knWCu8uY626+OS96iXDeSkHBesG3wGPHovNexbzaDkvFvNoR/8gjoz+Mc17xVdCvhRPko86CGuIe/Nh8ZijZxzmnTUUj3HPcZ+bJ4vHAt8rFK/SS6F4dfRebp4sHot8L6xZ+IxeQpzEOEmaJ+ExSeSn4lXyy5plnXF/8mT1G9c77sCcX1N8OHrMNH8W73G94w48egx8S74F39rmPa533OHJ0WPFw6MnffNq8Z6Qj7XsuPbhU+BxPDevFu9x7eMOXPiHcg6WLfB5bV1tQ90aYzl+/uUBpSiqxEzDafXlW/IntS2wnZl/+PlvT5azhbrY716v1ht8f5y8erM5Ot/u7la36J3v7643uyPzzCl8+x1m6i9Vr3pqu2+fg//T52CZgu6zPgq/wjL7hJwFqouF2L/Q6v3+anW13sJgqF0dj583jjPx7+Nf/W2xryxnHwA=",
        },
        {"url": "https://puzz.link/p?cocktail/10/10/107668sgg1l3q54f0qfee0e0fevvf70c0cf7dh853h1g2h1", "test": False},
        {
            "url": "https://puzz.link/p?cocktail/17/35/0gf1sfdrdfrvnar28dkkmpab4k3i4jt99ugkvdo7nd5n6irjmdpn6sr36c1jj09tqgctc0ve8tb9b9qapr5as8be6dr575jbcphpc5cidpitt9h41fhj2poh2g2l29f0e70e8041h0t3hpk01u01n1o0hh76003hvc08000gs080e7s0oue607v0o7ha2dd1dte8371ji01o610ao6180ca790dt5fkg42rck531h314h56g28j2g6h4g2k1632g4i0h25h34111",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="gray", adj_type=8, grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(area_color_connected(color="gray", adj_type=4))
        self.add_program_line(avoid_rect(2, 2, color="gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count(num, color="gray", _type="area", _id=i))

        for (r, c, d, _), draw in puzzle.edge.items():
            if d == Direction.TOP and r > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r - 1}, {c}).")

            if d == Direction.LEFT and c > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r}, {c - 1}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
