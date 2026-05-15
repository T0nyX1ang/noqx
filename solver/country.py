"""The Country Road solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, count, display, fill_line, grid, shade_c
from noqx.rule.helper import full_bfs, validate_type
from noqx.rule.neighbor import adjacent, area_border
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import count_area_pass, single_route


class CountrySolver(Solver):
    """The Country Road solver."""

    name = "Country Road"
    category = "route"
    aliases = ["countryroad"]
    examples = [
        {
            "data": "m=edit&p=7VZdT1w3FHznV0T32Q/XH8cf+1LRFPpCSdtQVdEKISDbBhW6KbBVtGj/e+f4jteoASUoFX2JVusd22d95vrOHPvmr9Xp9cJYZ2w0PpvRWHxCCSaGaEKy9Tvyc3Rxe7mYvTC7q9t3y2sAY17t75vfTi9vFjtzRh3v3K3LbL1r1t/P5oMdzODwtcOxWf80u1v/MFvvmfVrTA3GYuxgCnKAex3+WucVvZwG7Qh8SAz4BvD84vr8cnFyMI38OJuvj8ygeb6t/1Y4XC3/Xgzkof3z5dXZhQ6cnd7iYW7eXbznzM3q7fKP1dBSbMx6d6J78ABd3+n6LV3/MF33X9C9vPhzsfzwENVyvNlgy38G2ZPZXHn/0mHu8PXsbqOc7gYJ+tdvwGN6L4PEfw3EhIEUtn3nNMLf6xf0pfe9R9/e6wv6kX2ktTX5m9ru19bV9gjczNrX9rvajrWV2h7UmD1Q9tCmV97ODD5Y4ETsgDOxBy7Ewfg4EidgP2ER45MlhuSTI0ZMajHIlZhLCrBMOI7AkRgcEjlEcEjkEJE3M29CfGZ8QkxmTEKuwlwZMYUxGY4byafAeSPXLw6Y/y2IsVMMYoGncYyZ4BouJviJc3DJhDDlCj6YIBO3gP0J3B+MAU8cMAbHN4xcmbmSoCpYYowXjmcPXIiLkZF5ywjMdcBfyD+UbMROeysjYmwkDkbcSCzAlhjxjvEW457jeEbhM+J/wFzHeeCJD2KNhEQMDiETIya0GOTlnmA9YK7vI7AjTsCeGHyoQwnIK8yLaimR8dCbUG/ICcx4AZ9IPgI+kXwEfCL5CPgk8oFWhVpFHmCuHxGfGA+9CfUmEfGZ8Xh3kls8+GTyieCTySdiDzP3EFoVahV5gMkN+hTqU3IycWwegc5Fuo+aH9Uj0XZfNN+Bs+c+VF80DybbPZh8912S7jX1S/NXhjczPQ69+UKvFfWR3fql+Qse2noHXoFfSvdF84v6ovkFNQTe6B4J0vXffJHhNe6naj6Qg2p+6xH1bONQkKs0/atHms7D1i/wCjC1Ac7NL/AKPCJd/80vOK7FMt4i3rZ49Re14aA3Rw04vFPnu0eap5z6qOl/7P5Sv/im+dC9ph5pXlOP+OavfM93WDNwzVC6v1TD1EnVamx6A3++X/x2bav2mp6z6xpGzdlqOIeu4Sxdw1n1n7a6nfS80ZNaj5SXtQ21jfWoSXpIPukY/ZJTbUi6/6iFgx21OiuCS/UBfUVaGhRlow8KhOfUx1TkjRZcIGjJqpb8dEh+8unmPtTr3ccf+Tr+HOPHO/PhABe5F4fL66vTS9zm9t7+fq93uLo6W1y3Pi7Sm53hw1C/9fIVvt6t/4e7tW7/+Gyl4TO9/Ak6c+wsK4pZvzLD+9XJ6cn5EiLD5rVJFJmHJxNuXU+b0DL21BlWt0cmp4L32GStgY9Msiw+lQ5K8kcTz/5WUaSPd/4B",
        },
        {"url": "https://puzz.link/p?country/10/12/d4ibeqt5abl75ajb6m94i80400vvvvk5vvufvv9h7sci34h21h21t6j6h", "test": False},
        {
            "url": "https://puzz.link/p?country/17/17/4si5d6t8fa2heg0ch42pfar88vioeikf7s4665a6g69g2bo2rc2qk0g5jrmll2p6kk62qsfhflvrakghu0pq13l87qg5huhgj407o09p0557vg4g4j-19o-362k2q1g",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            self.add_program_line(count_area_pass(1, _id=i))
            if rc:
                num = puzzle.text[Point(*rc, Direction.CENTER, "normal")]
                if isinstance(num, int):
                    self.add_program_line(count(num, color="white", _type="area", _id=i))

        for (r, c, d, _), draw in puzzle.edge.items():
            if d == Direction.TOP and r > 0 and draw:
                self.add_program_line(f":- not white({r}, {c}), not white({r - 1}, {c}).")

            if d == Direction.LEFT and c > 0 and draw:
                self.add_program_line(f":- not white({r}, {c}), not white({r}, {c - 1}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
