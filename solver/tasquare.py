"""The Tasquare solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import (
    count_reachable_src,
    grid_color_connected,
    grid_src_color_connected,
)
from noqx.rule.shape import all_rect


class TasquareSolver(Solver):
    """The Tasquare solver."""

    name = "Tasquare"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVdb9owFH3nVyA/+yH+iAl5Y23ZC6PbwlShKEKBpQINFBbINBnx33d9nZKGmK2VVh6mKfHVucd2fHxsx7vvZVpklDHzioB6FBCVvsLCGMfiVc9ktV9nYZcOyv0yLwBQej8c0sd0vcs6cdUq6Rx0P9QDqt+HMWGEEg6FkYTqT+FBfwj1mOoIqgiVwI1sIw7wroYPWG/QjSWZB3hcYYBTgDsUPxtZ5mMY6wklZpx32NtAssl/ZKTSYfJFvpmvDDFP9zCZ3XK1rWp25df8W0mehjhSPbByI4dcUcsVJ7nCLZf/Fbnrbe4S2k+ORzD8M0idhbFR/aWGQQ2j8HA0ig5EBKZrF1TYVSGSnxHKEH6dKkjVKe15kMpT2peQijoNGn2ZxxutGTc5f5arRncmvGbuy8bgzA+a9ers+8H5ZFigGgy4wNCL6ZMXwDeWxhrSYpWbVS4WPWqxaFWbdWqwxrVpfoF2yrButmnfKcR626bdE7dOO2iHEnB7iJ5zjBPYklQLjLcYPYw+xhG2ucP4gPEGo8SosE3PbOoXbnsiYVoSVgomze0ZeL4H3khbLDj+Ss8f/99lk05MorJ4TBcZ/KnG5WaeFd1xXmzSNeTRMt1mBC6HY4f8JFjwHMv/98XV7wtjvveqW+MKJ+YPcmI9pcKn+p6SbTlLZ4scdhW49jte9t+Sj6gMLvA9Ny/EBZ67eSVf+f0L33GMe/XVhV9i0vkF",
        },
        {
            "url": "https://puzz.link/p?tasquare/21/15/g.k..k4k.x.h.i8j2q.u4i2l2jar.2l.h.zhak8i8h9j2.x1m.n2g.h.l.j2h3g1k2g4r.o1i3h.i.j.l1zj2g4i..g.i.h./",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(all_rect(color="black", square=True))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color="black"))
                self.add_program_line(count_reachable_src(num + 1, (r, c), color="black"))
            else:
                self.add_program_line(count_adjacent(("gt", 0), (r, c), color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
