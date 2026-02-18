"""The Yajikabe solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.rule.variety import yaji_count


class YajiKabeSolver(Solver):
    """The Yajikabe solver."""

    name = "Yajikabe"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZXfb9s2EMff/VcEfNpQDhP1y7KAPThp3LV1HKd2kMWCITCOkiiRrEw/nFZG/vceTxpESnKxPazbgMHW+fQhebwj6S+z3wueBpRp4ms4FH7hYzIHH92x8dHqzzLMo8A9ouMif0hScCg9n0zoHY+ygH64fpieJOOXt+Pfdk6+WrF3WvFeu3qcPL75FH98Hxopm8yc+dn8LNTvx7+eHF/Yp2/seZFd5sHuImbHj5er5d386n6kfzmdrcxyda5ZH1Z3P+/Gl78MvDqH9WBfjtxyTMt3rkcYoUSHh5E1LS/cfXnmljNaLqCJUBPYtOqkg3vauFfYLryTCjIN/Bn4EIyBew3uJkw3UeBPKzJ3vXJJiZjnGEcLl8TJLiB1HuJ9k8Q3oQA3PIelyh7C57olK26Tp6LuCwFJXER5uEmiJBVQsFdajqsSFj0lGE0Jwq1KEF5PCaKyv7mEUX8Jr7A9n6AI3/VEPZeN6zTuwt2Dnbl7YhhipOGL/MVOQlDD7CDTqZDYnBpZWoWMBtmImK9JCMPrcizbqpDUa1j3kpHdGTgcVuGlGR2cUenljDqIaXUwaSTT6mhSSYxh5Wo/hmOVWRnDOZgyh866/fR6caW6mI5jVWbo3ZwNzE/NxayZnLNZ1yszC3PWlLHVTpjNHHAAGB6Da7QTtDraJZwSWhpo36LV0Fpop9jnFO0V2hO0Jlob+wzFOfuTJ5EYsIsmHDI4GHp1LL9Dbp5RKa36sf57bD3wyKJI7/gmAJmYFfFNkB7NkjTmEQGtJlkS+VnV7gef+SYnbnVdyC0K22IMBUVJ8hyF274IfzQpMLzfJmnQ2yRgcHt/KJRo6gl1k6S3rZxeeBSpteBVqqBKfxWUpyCu0jtP0+RFITHPHxQgCbESKdi2FjPnaor8ibdmi5vleB2QzwQfz6C62Mj/L9Z/9cUqtkr7S9frP6+xHqw4KF15Tslz4XMfasK1Fdy0Whz2pLe/dYDbB/hw/d1XAf9cSfoNpWsa27hH74B+Q/Kk1j5+QN2k1jbvSJlItqtmQHsEDWhb0wB1ZQ1gR9mAHRA3EbWtbyKrtsSJqToqJ6aShc4jX/hj+MTLVXH0g3Azvv0JX8H5kawHXwE=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="black"))
        self.add_program_line(avoid_rect(2, 2, color="black"))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            fail_false(isinstance(clue, int) and label.startswith("arrow"), "Please set all NUMBER to arrow sub.")
            self.add_program_line(f"not black({r}, {c}).")
            arrow_direction = label.split("_")[1]
            self.add_program_line(yaji_count(int(clue), (r, c), arrow_direction, color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
