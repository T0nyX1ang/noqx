"""The Kurotto solver."""

from typing import List

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import count_reachable_src, grid_src_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        solver.add_program_line(f"not black({r}, {c}).")
        if isinstance(num, int):
            solver.add_program_line(grid_src_color_connected((r, c), color="black"))
            solver.add_program_line(count_reachable_src(num + 1, (r, c), color="black"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")
        else:
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Kurotto",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VbNbtpAEL7zFGjPe/Cs1783moZeKGkLVRRZFjLUUVCMTA2uqkW8e2bGbnbd5NAeSi+R2dF887ffDoOXw/e2aEoJij5+LD0J+OhE8/KjgJfXP8vtsSrTsZy0x4e6QUXKm+lU3hfVoRxlfVQ+OpkkNRNpPqSZACGFwgUil+ZzejIfUzOXZoEuITXaZl2QQvXaqrfsJ+2qM4KH+rzTQ1TvUN1sm01VrmboRcunNDNLKWifd5xNqtjVP0rR8yC8qXfrLRnWxREPc3jY7nvPof1WP7Z9LORnaSYd3cUrdH1Ll9SOLmn/jG61r18jmuTnMzb8C1JdpRmx/mrV2KqL9IRynp6ErzE1kGH3nQjtIfQsDBD6zzAAhLGFlKufYUi5YJNDio4sDAc7RRRtS0dqEBz7g51iyrU7JVRZjLGZvwyUDWBxPNgLvCFTAKpnywNEv+Fk0AZQVN/JV9QXx+/TYZx8n+q7fqpn6YEm7NTjToYOpnzbDQipHc75gJtpuwchHTixOBr2HhIibDdQHhF2MR3QwUB+t8MKiILdQQ1ahMMEPFJ3LKcsFcslTpw0Psv3LD2WAcsZx1yzvGV5xVKzDDkmopn9w6kWGg+ucHDxPLob8Qtwy3zNb8qXT/BmpycfZWLRNvfFpsTX1rzdrctmPK+bXVEJvCHOI/FT8MKZxgvn7dK4+KVBzff+6ur4/7/5DPuqQZobKfbtqlht6krgPw7JdvXCfnH2+GIQj21TH4+1yEdP",
        },
        {
            "url": "https://puzz.link/p?kurotto/17/13/7i4i-1ai4iay1i6ibi0y3ibi9i-14iay4i7i-10i4y-11iei6ici3y1ibi7i2y-10i8i0i4i1",  # this example will probably TLE
            "test": False,
        },
    ],
}
