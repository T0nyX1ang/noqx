"""The Oasis solver."""

from typing import Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, invert_c, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected, grid_src_color_connected
from noqx.rule.shape import avoid_rect


def count_reachable_oasis(
    target: int,
    src_cell: Tuple[int, int],
    color: str = "black",
    adj_type: Union[int, str] = 4,
):
    """A rule to compare the number of reachable oasis cells to the source cell with a specified target."""

    src_r, src_c = src_cell
    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)

    return f":- #count {{ R0, C0: {tag}({src_r}, {src_c}, R, C), adj_{adj_type}(R, C, R0, C0), clue(R0, C0) }} != {target}."


class OasisSolver(Solver):
    """The Oasis solver."""

    name = "Oasis"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VRLj5tADL7zKyKffWAeEMIt3W56SbNtk2q1QigilNWigkhJqKqJ8t/rMSgoo1baHrptpWoyX+xvPMYP8OFLl7UFCt/+VIT0T0uLiLeMQt7+sDblsSriCc6741PTkoB4t1jgY1YdCvSSwSz1TmYWmzmaN3ECAhAkbQEpmvfxybyNzQrNmo4AdYpQd9WxzJuqaYE5QXbL/qIk8XYU7/ncSjc9KXySV70ckvhAYl62eVVsl72jd3FiNgj22a/4thWhbr4WMMRm9bypd6UldtmRMjw8lXtARQeH7lPzuRtMRXpGM+8zWD8zAzVmoC4ZqN+ZQbVvfhD7LD2fqS0fKPptnNhEPo5iNIrr+HS2AZ1ASbqqMew7B2p6peqAVDGqkX3OBC5EqB1iKl0idIjIv3IZWZfBRRX+dQBCBI4+I3066lI5/oUSLqMdn4HvWgQ2inDUQ+tVDjpVSnC9HhgXjJJxQ+VEoxhfM/qMAeOSbW4Z7xlvGDVjyDZT25BntgwUBS6pSZSh7vv3ArElqp8W1yv497jUS2DdtY9ZXtDntOrqXdFOVk1bZxXQMDt78A14JwqlNf8/3/7K+WZb5P/SlPvzX3BCpVYCzR3CvttmWyozvwLM+w6vel5rh9c/4YP0xbOlsZB63wE="
        },
        {
            "url": "https://pzplus.tck.mn/p.html?oasis/17/17/.h6o3h.m.g.o.h.h4h.h.h2u4y.i6i.i.m.k4l.l1l.i4j1g1j4i.l1l.l3k.m.i.i2i.y4u3h.h.h3h.h.o.g.m.h5o2h./",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(defined("clue"))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(invert_c(color="black", invert="white"))
        self.add_program_line(invert_c(color="clue", invert="oasis", _from="white"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_color_adjacent(color="black"))
        self.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="not black"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"clue({r}, {c}).")
            self.add_program_line(f"not black({r}, {c}).")

            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color="oasis"))
                self.add_program_line(count_reachable_oasis(num + 1, (r, c), color="oasis"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
