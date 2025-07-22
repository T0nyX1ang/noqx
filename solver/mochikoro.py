"""The Mochikoro solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, invert_c, shade_c
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, grid_color_connected
from noqx.rule.shape import all_rect, avoid_rect, count_rect_size


class MochikoroSolver(Solver):
    """The Mochikoro solver."""

    name = "Mochikoro"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVRi5tAEH73VxzzPA+uu5rcvpT0eulL6rVNSjhEgrEekTNsamIpG/Lfb3aUmhYPehykUIrZj2++Hcdvx3Wz/9ZkdYFCuJ8co4/EUIURDyECHn53LcpDVegrnDSHjamJIN5Np/iQVfvCS7qs1Dvaa20naN/rBAQgBDQEpGg/6aP9oG2Mdk5TgIq0WZsUEL3t6ZLnHbtpReETjztO9J5oXtZ5VaxmrfJRJ3aB4J7zlu92FLbmewGdDxfnZrsunbDODrSY/abcdTP75qt5bLpckZ7QTlq78wG7srfraGvXsQG7bhWvt1vtzJDR6/R0ooZ/JqsrnTjXX3o67ulcHwljfYTQp1vp3bbvBEL5axi5woo8dkLEwpteGI1JUD9D4QuKZR8HruBZrH6vKCJXoX+kGLkK47NYncXkWrD3e8YpY8C4oKWhlYzvGH3GkHHGObeMS8YbRsUYcc7INecP2wcyAK0QJK0vaHt5AW+JpE9w4Ar/XTX1Epg39UOWF7Tj42a7Luqr2NTbrAI6XE4e/AAevMvU//Pm4ueNa77/olPn73/FCfWVviV7h7BrVtkqNxXQnxWyLp/Rn8t/aZ3X1794N+nood2Rb8pHUxtIvSc=",
        },
        {
            "url": "https://puzz.link/p?mochikoro/22/13/4l2k4m3w4p5h1n2x2v4i2h4k2h5p2k4m5j4q2t2u3n4g4l3o4o2n2j2zk2g1n1o",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(invert_c(color="black", invert="green"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="not black", adj_type=8, grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="black"))
        self.add_program_line(all_rect(color="green"))

        all_src = []
        tag = tag_encode("reachable", "bulb", "src", "adj", 4, "not black")
        fail_false(len(puzzle.text) > 0, "No clues found.")
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="not black"))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_rect_size(num, (r, c), color="not black"))

            all_src.append((r, c))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
