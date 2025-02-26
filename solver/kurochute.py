"""The Kurochute solver."""

from typing import Tuple

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def count_sight(src_cell: Tuple[int, int], distance: int, color: str = "black") -> str:
    """Generate a rule to count the number of color cells in the distance of sight."""
    r, c = src_cell
    cells = ((r + distance, c), (r - distance, c), (r, c + distance), (r, c - distance))
    return f":- {{ {';'.join(f'{color}({r0}, {c0})' for r0, c0 in cells)} }} != 1."


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="black"))
    solver.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        solver.add_program_line(f"not black({r}, {c}).")
        if isinstance(num, int):
            solver.add_program_line(count_sight((r, c), num))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")
        else:
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display())

    return solver.program


__metadata__ = {
    "name": "Kurochute",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VZNj9o8EL7zK1Y+zyG280Fyqeh26YWybaFaraIIhTQr0AaFBvKqMuK/78wkwknEoa8q0UOryKN55osn43HM4UedVjlIDVKCHoMDEh9PK3A9H6QKeDnts9weizy6g0l93JQVKgCP0ym8pMUhH8VtVDI6mTAyEzAfo1hIAULhkiIB8yU6mU+RmYNZoEuAi7ZZE6RQfbDqE/tJu2+M0kF93uqoPqOabausyFezxvI5is0SBP3Oe84mVezK/3LR8iCclbv1lgzr9Igvc9hs963nUH8vX+s2ViZnMJOG7uIKXW3pktrQJe0KXXqL36db7MtrRMPkfMaGf0Wqqygm1t+sOrbqIjqhnEcnoX1KfYcsml0ROkSDukBX9iGF01C0cIwQp6WFHkEb7FEp9wJ9KmWDA7dXKqDKnoVUynrHqlc5pFxbOfR6UDrkttHSIb8tJp1+cSmJWRdTfCdfkb9TX/W54qHoxw+aJl1ijwfoggd8XMrvYG5cJ993+n6/vwvSH/x+MMgfE+7EhwN+4aBe2I9XkvjbnVOS+osfgwvu9gsHS/J4PbOcslQslzh9YDTLDywdlh7LGcc8sHxiec/SZelzTEDz+4sTzrOtcAy1iNxm3G/ALda00dcfGpm/3JOMYrGoq5c0y/EDNq9367y6m5fVLi0E3hXnkfgpePG8uf+uj5tfH9R8539dIn/+xMfYV0+DeQSxr1fpKisLgf89gOx4Hof2m7PHz4J4rasy29THXCSjNw==",
        }
    ],
}
