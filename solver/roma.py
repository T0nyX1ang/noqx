"""The Roma solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, count, defined, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, validate_direction
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


def roma_adjacent() -> str:
    """Generate a rule to define the adjacency for roma."""

    # the definition is designed to be compatible with the reachable propagation (grid_all = grid + hole)
    rule = "adj_line_directed(R, C, R, C + 1) :- grid_all(R, C), grid_all(R, C + 1), arrow_N_W__5(R, C).\n"
    rule += "adj_line_directed(R, C, R, C - 1) :- grid_all(R, C), grid_all(R, C - 1), arrow_N_W__1(R, C).\n"
    rule += "adj_line_directed(R, C, R + 1, C) :- grid_all(R, C), grid_all(R + 1, C), arrow_N_W__7(R, C).\n"
    rule += "adj_line_directed(R, C, R - 1, C) :- grid_all(R, C), grid_all(R - 1, C), arrow_N_W__3(R, C)."
    return rule


class RomaSolver(Solver):
    """The Roma solver."""

    name = "Roma"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VZdT9swFH3vr0B+9kP8kdjOG7CyFwbbYEJVVVUBulGtVVg/tilV//uOnZuaDyMkJtAepiju6fG51/fYiZ3lj3W1mHCLS1mecYFLaRlumblwZ3SdT1ezSbnH99erm3oBwPnp0RH/Ws2WE94bkmzU2zSubPZ5874cMsE4k7gFG/HmU7lpPpTNgDdn6GJcgDtuRRKwH+FF6PfosCVFBnxCGHAAWC0W9a/xyfigpT6Ww+acMz/QQQj3kM3rnxNGhfj/V/X8cuqJy2oFO8ub6S31LNfX9fc1243B5uvZanpVz+oFo3K3vNl/2oOKHtTOg0p7kA88XLyCB5n2sMUCfYaLcTn0hr5EaCM8KzdbX6xvRWgH5YZJhyyGP5h5pixo9YjWeZLOM9ASLqaLq9lkfEysAJs/Fut0jgK0eEQXOpmkeELtkrRJJzEmTaenxJpkbptWO5mmVWqmnE2KRZYnhxQitQxY0KOwrDK051h13qjQvgttFto8tMdB08cDIArHhcECoir8AgvC2DisarFVXLi8xU7fwZ7XUWMJGxlx4XNK0iDWUqzNgQvS64gLxBodeUN6A73pNDpiUyDWUk4L7Ah73sTYDluDmknjsB2K1i9+gds6ZZbdx5mINTvK43weGtfZmNN7dFSbKxBrKY/1W+8uNmINXJAGekF6Ye5gxApHGnMfd/kFvCjyouBFt2sn/ba/w54nX1oBa8KoIacalIy8hHclI5aU3x8jHZbIKTsNYqWK89lhibFklxNjqW4s+FUmjqtIr6BXpFden8c8HfYaTVjnwJRTI6emnBrzo20cq8Oez/0cbv2m7l+Fw9Dq0BbhFTF+2/yLjbW4v7lcvPwdfbbIoSzCMR+v/G3/j3pD1r/+Ntk7qRfzaoaj6+ymup0wfDlse+w3Czd2LOml/z8m/vGPCb9Y2Yuf/Fd6xp8pZ9j0+e4s480pZ7frcTWGNYYPWN520/H2VPfLowccb+BD/s1nCBvBqPcH",
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
