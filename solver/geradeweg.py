"""The Geradeweg solver."""

from typing import Tuple

from noqx.puzzle import Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.loop import loop_segment, loop_sign, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def count_geradeweg_constraint(target: int, src_cell: Tuple[int, int]) -> str:
    """Generate a constraint to count the geradeweg clue."""
    r, c = src_cell
    rule = f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "T"), |{c} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "V"), |{r} - N1| + |{r} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "H"), |{c} - N1| + |{c} - N2| != {target}.\n'
    return rule.strip()


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(defined(item="clue"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="geradeweg"))
    solver.add_program_line(fill_path(color="geradeweg"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="geradeweg", adj_type="loop"))
    solver.add_program_line(single_loop(color="geradeweg"))
    solver.add_program_line(loop_sign(color="geradeweg"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        solver.add_program_line(loop_segment((r, c)))
        solver.add_program_line(f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| != |{c} - N2|.')

        if isinstance(num, int):
            solver.add_program_line(count_geradeweg_constraint(num, (r, c)))
            if num > 0:
                solver.add_program_line(f"geradeweg({r}, {c}).")
            else:
                solver.add_program_line(f"not geradeweg({r}, {c}).")
        else:
            solver.add_program_line(f"geradeweg({r}, {c}).")

    for (r, c, _, d), draw in puzzle.line.items():
        solver.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

    solver.add_program_line(display(item="grid_direction", size=3))

    return solver.program


__metadata__ = {
    "name": "Geradeweg",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VZRb9owEH7nV1R+voc4tpOQl6nrur0wuq2dqiqKEKVZiwajg7JVQfz3fndJG+gwtNpWadIUcnznz7mcv7MPZt/n/WlBOuCPSQjfuKxO5A6TSO6gvk6GN6Mi3aP9+c3VZApAdNSlL/3RrGhl9aS8tSjbablP5bs0U1qRCnFrlVP5MV2U79OyS+UxKEUaY51qUgh42MBT4RkdVIM6AO5WOAI8AxwMp4NR0etUgT6kWXlCit/zWp5mqMaTH4Wq82B/MBmfD3ngvH+Dtcyuhtc1M5tfTL7O67k6X1K5X6Xb2ZCuadJlWKXL6G+lOxp+K243ZdrOl0so/gm59tKM0/7cwKSBx+kCtpsulAnwqKGoKooybbjhg2tjuLpxk3WXJzeu41CNG7HbhIrcGhvbNTbhyI2rg5BXFECvh5Fo7XkdcGq28TXzKxFCvc7LQld4w/ms8Jb9Fd4+iidSrPqPMnY8X71ayVhWrMz9CATXIvuZ2LdiQ7EnqAqVRuwbsYFYJ7Yjcw7Fnoo9EGvFRjIn5ro+q/K/k46yoVFpO8EWCFFHAawvg8igdALs/QhLycBoYtIAhWQQgREaDSoFZC05aArkEorreQFZvIBRjIZUoYR4lzJqk6uiOOxg1Mc8UacMcbmzrV/u3xvLW5nqoBnsdSfTcX+EltCdj8+L6b2P9rtsqVslN445mvn/jvzyHZnVD17sdP6ZZpFB2PrEUnlE6nre6/cGE+wxaFeRcoh9pJxrD1kddQ9ZnX5/WDQEHyk9wkdK2/CR0kl8CUlz2UyiEW4m0AY9hI18oayHwKI9oTwEft1i0s6rv0bWmOKlHVoLfr18dBSC9soFCrS3SKC2BHdW+wiPnjEKu5nw6Rk7j2zPIZ5C/ZrAlqS3LHSLODtl3VmWnWXduS12bqud2xITXrz74V+Auiym/YviZ3Gp8tYd",
        },
        {
            "url": "https://puzz.link/p?geradeweg/v:/17/17/0000i000i0000000i3g0g2i000000g1m3g000000j3g2j0000000g1k1g00000000000i00000000j0k0h2g0g2g1i.g.h4l1g3q2g2g2g0h2h0g2k1g00k00h3g0h000h1h000h0000000k000000000000g2g2g0000000000000i000000000000000g0000000000000000g00000000",
            "test": False,
        },
    ],
}
