"""The Mochikoro solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, invert_c, shade_c
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, count_rect_src, grid_color_connected
from noqx.rule.shape import all_rect, avoid_rect


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

        fail_false(len(puzzle.text) > 0, "No clues found.")
        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(f"clue({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="not black"))
            if isinstance(num, int):
                self.add_program_line(count_rect_src(num, (r, c), color="not black"))

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"black({r}, {c}).")
            else:
                self.add_program_line(f"not black({r}, {c}).")

        tag = tag_encode("reachable", "bulb", "src", "adj", 4, "not black")
        self.add_program_line(f":- clue(R, C), clue(R1, C1), (R, C) != (R1, C1), {tag}(R, C, R, C1), {tag}(R1, C1, R, C1).")
        self.add_program_line(display(item="black"))

        return self.program
