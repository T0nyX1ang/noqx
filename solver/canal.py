"""The Canal View solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from noqx.rule.shape import avoid_rect


class CanalSolver(Solver):
    """The Canal View solver."""

    name = "Canal View"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VTLTsMwELznK9CefYgfaV1fUHmUSymPFiEURSgtQVSkCqQNQo7y76w3oSGoBw4I9YBcj2Z23Xi8m3j9WsR5wgY4pGY+4zik9mlq5X5+M2bLTZqYAzYsNk9ZjoSxi9GIPcbpOvHCZlXklXZg7JDZMxMCBwYCJ4eI2StT2nNjJ8xOMQVMYWxcLxJIT1t6S3nHjusg95FPGo70DulimS/S5H5cRy5NaGcM3D5H9G9HYZW9JdD4cHqRreZLF5jHGzzM+mn50mTWxUP2XMDnFhWzw9rudIdd2dqVW7tyt13xK3bTl2yX0UFUVVjwa7R6b0Ln+qaluqVTU0KgwCgGQQBGVM5eCULjcwJsODUIpEDZa2UPpdxKJbqy35F9lxVbqf3Oo7Ryhg+hDehOftDdigv+Tbu8arXseuFktT0IV/4XjYflpqxcGxyOCAXhDMvDrCQ8IfQJA8IxrTklvCU8JlSEPVrTdwX+YQvqqv+BnVBo+o6/jmC/IpEXwrTIH+NFgi/2pFjNk/xgkuWrOAW8QyoP3oEmtVn9Xyt/fq244vv79mbvmx381iLvAw==",
        },
        {
            "url": "https://puzz.link/p?canal/17/17/r11q33h33m31h13m31h16q42q16u81z14u21q21u43z16u31q31q62h41m54h31m12h15q21r",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="black"))
        self.add_program_line(avoid_rect(2, 2, color="black"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(bulb_src_color_connected((r, c), color="black"))
                self.add_program_line(count_reachable_src(num + 1, (r, c), main_type="bulb", color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
