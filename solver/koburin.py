"""The Koburin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route


class KoburinSolver(Solver):
    """The Koburin solver."""

    name = "Koburin"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VZRb9o8FH3nV1R+vg9x7ISQl4l1sBdGvxWmqooQCjRdo4WFBTJNRvz3HjthYXxJC+rUoWkCXx2f62vuucY3WX3LwywizvVXeGQREEnHNYNz2wyr/IzjdRL5F9TN1w9pBkB01e/TfZisImoF5bJJa6M6vuqSeu8HjDNiNgZnE1If/Y364KshqRFcjDxwg2KRDdir4I3xa3RZkNwCHpaY2LXe7hbTeZzNk2g6AAvmPz9QY2La+dbsoCFbpN8jVuai5/N0MYs1MQvXULR6iJelZ5XfpV/yci02ZIs8WcfzNEkzTWpuS6pbyOjtZMhKhqhkaFjI0KhGhlb3cgnJMq1LvlOf/BaHc430p36glXyqoFfBkb9h0ma+BzwEFu6uIsU5GmfA3lSEKzUh9oj2QQi3TAz+Cj8Zzg/XcHHI2P+LcszO+4xracbaYzwTtb+P5/2yBsK4v4G9NbZvrG3sGDUgJYx9Z6xlrGPswKzpoSi2w8l2URkbf3DXBUZiNpw3ZsmlsdJY14S2dXGPLb+AAlmU/yW5Mukhw45HrC06BZBtkiiGICbEDoFz8YMFJ3CWohD5rJpAoEPUfJy/l520AjbKs/twHuHeDeKv0cUwzRZhglnv7vPebJgvZlG2m6MtblvsBzMjELrN/uuUZ90p9UFZR17Yl1/VI2/cM+kEakS4k+qK2DKfhlNoYngkU6AGu6vf4Cy6QXMkGkRzJHpGvRNtp87RlCR45zTePZFvKo705KmOTq20JxxtyztHR/0RPeU4Sx2nn+Af1tFY3dco+6k/jheJOkcPz6zyRajJXb4b/eboV++7eNmZtB4B",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(fill_line(color="not black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))
        self.add_program_line(grid_color_connected(color="not black", adj_type="line"))
        self.add_program_line(single_route(color="not black"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"hole({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(target=num, src_cell=(r, c), color="black", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            if color == Color.BLACK:
                self.add_program_line(f"black({r}, {c}).")

            if color == Color.GRAY:
                self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
