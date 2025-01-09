"""The Rail Pool solver."""

from typing import List

from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, defined, direction, display, fill_path, grid
from noqx.rule.helper import full_bfs
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def len_segment_area(color: str = "grid") -> str:
    """
    Generate a rule to get the length of segments.
    """
    rule = 'nth_horizontal(R, C, 0) :- grid_direction(R, C, "r"), not grid_direction(R, C, "l").\n'
    rule += 'nth_horizontal(R, C, N) :- grid_direction(R, C, "l"), nth_horizontal(R, C - 1, N - 1).\n'
    rule += 'nth_vertical(R, C, 0) :- grid_direction(R, C, "d"), not grid_direction(R, C, "u").\n'
    rule += 'nth_vertical(R, C, N) :- grid_direction(R, C, "u"), nth_vertical(R - 1, C, N - 1).\n'

    rule += f'len_horizontal(R, C, N) :- nth_horizontal(R, C, 0), {color}(R, C + N), nth_horizontal(R, C + N, N), not grid_direction(R, C + N, "r").\n'
    rule += f'len_vertical(R, C, N) :- nth_vertical(R, C, 0), {color}(R + N, C), nth_vertical(R + N, C, N), not grid_direction(R + N, C, "d").\n'
    rule += f"len_horizontal(R, C, L) :- {color}(R, C), nth_horizontal(R, C, N), len_horizontal(R, C - N, L).\n"
    rule += f"len_vertical(R, C, L) :- {color}(R, C), nth_vertical(R, C, N), len_vertical(R - N, C, L).\n"

    rule += f"area_len(A, L) :- {color}(R, C), area(A, R, C), len_horizontal(R, C, L).\n"
    rule += f"area_len(A, L) :- {color}(R, C), area(A, R, C), len_vertical(R, C, L).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="black"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("railpool(R, C) :- grid(R, C), not black(R, C).")
    solver.add_program_line(fill_path(color="railpool"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="railpool", adj_type="loop"))
    solver.add_program_line(single_loop(color="railpool"))
    solver.add_program_line(len_segment_area(color="railpool"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            len_data = 0
            for j in range(4):
                num = puzzle.text.get(Point(*rc, Direction.CENTER, f"tapa_{j}"))
                if isinstance(num, int):
                    solver.add_program_line(f":- not area_len({i}, {num}).")
                    len_data += 1
                len_data += num == "?"
            solver.add_program_line(f":- #count{{ N: area_len({i}, N) }} != {len_data}.")

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Rail Pool",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VVNa9tKFN37V4RZz2I+JY02IU2Tblz3tU4JQZjgOEpjasevdlQeMv7vOXd0ZalxoA8CJYsi63J8dObeM3dGo82ParouZcBlM6mkxmUzFe/M0U/xdTF/XJT5kTypHu9XawApP52fy7vpYlMOClZNBts65PWJrD/khdBCCoNbi4msP+fb+mNej2U9xiMhHbhhIzKAZx28jM8JnTakVsAjYAcMeAU4m69ni/J62DD/5EV9IQXVeRdHExTL1c9SsA/6P1stb+ZEPFTLuwWTm+p29b1imZ7sZH3SOB2+4NS+5JTI505Z8GqnN9NHtH1zP//3Jbthstuh419g+DovyPvXDmYdHOdbkTmRO+ARsNPtfCV6iqwODwtxfNxjkgMmRKYjkuy5JFXEYMn3hDmQHFQKkemZCQelQ1OpI7SKlfoarRt/fcoclNfmoL426a8UmqTzLeJVjOcxmhgv0E9Z2xjfx6hi9DEOo+YMDdYhkTogr0H+kEqj4RfYqNBhY6WxmCthmwA3emNcD0NDlgk7jE0wI8KJAbYN9qrDpPGcP0We1DP20mToIuEMflrsNcZy/gT6hPWe8rcYGs91U4wNnD+gbsBOinzWw9CknN+grmWMA8ZYLFLkab4thsY0fdCB+sO1NDxonpdCLcZRQ+sfeXjT7F/Dv2bPisa2GBrFOQ28OR7rkJPehMjD2x5DY9r+oP8Jr1ECzwmvi6detRgazx5SeAtcK8BDYP84TveYNBl78Jg7vUcxPzwk3BNPtVoMjWcPBmMd53fI7zinpbkwJo1t+0M9YZ+a9iHXUsi5x9Ao7lWGnFnrmfwzH6Cn99Jgg1/GbX4ao4sxids/pcPmfx5HzUH0+jftt3YKrCx91PqXf1vMZFCIcbW+m85KHPLD+UN5NFqtl1P6Qp3dfuv9G1XLm3Ld/sfHdjcQ/4l4Fxap3N/v75///lL31Vvb9m/NDl7EyeAJ",
        },
    ],
}
