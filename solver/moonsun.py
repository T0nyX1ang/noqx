"""The Moon-or-Sun solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.loop import pass_area_once, single_loop
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def moon_sun_area() -> str:
    """
    Genearate a constraint to determine the area of the moon or sun.
    A sun area should only contain sun cells, and a moon area should only contain moon cells.
    A sun area should be adjacent to a moon area, and vice versa.

    A grid fact and an area adjacent rule should be defined first.
    """
    rule = "{ sun_area(A) } :- area(A, _, _).\n"
    rule += ":- sun_area(A), area(A, R, C), sun(R, C), not moon_sun(R, C).\n"
    rule += ":- sun_area(A), area(A, R, C), moon(R, C), moon_sun(R, C).\n"
    rule += ":- not sun_area(A), area(A, R, C), sun(R, C), moon_sun(R, C).\n"
    rule += ":- not sun_area(A), area(A, R, C), moon(R, C), not moon_sun(R, C).\n"

    constraint = ":- area_adj_loop(A1, A2), sun_area(A1), sun_area(A2).\n"
    constraint += ":- area_adj_loop(A1, A2), not sun_area(A1), not sun_area(A2).\n"
    return (rule + constraint).strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="moon_sun"))
    solver.add_program_line(fill_path(color="moon_sun"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="moon_sun", adj_type="loop"))
    solver.add_program_line(single_loop(color="moon_sun"))

    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name == "sun_moon__1__0":
            solver.add_program_line(f"moon({r}, {c}).")
        elif symbol_name == "sun_moon__2__0":
            solver.add_program_line(f"sun({r}, {c}).")

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    assert len(areas) % 2 == 0, "The number of areas should be even."
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(pass_area_once(ar))

    solver.add_program_line(area_adjacent(adj_type="loop"))
    solver.add_program_line(moon_sun_area())
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Moon-or-Sun",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VZdaxs5FH33rzB61sNImu+3bJr0xU0/khKCMcFp3I2p7UntuIQx/u85545cp/iWQhaWLCzj0RxfSfeee/S5+r4eLyfWJfyF0uKLJ3WlvL7M5U3iczF9mE3qvj1aP9w1SwBr35+e2q/j2WrSG8ZWo96mrer2yLZv66HxxsrrzMi2H+tN+65ur2x7jipjHWwDIGesBzzZw0upJzrujC4BPosY8ApwtV5cz5tm0Vk+1MP2whrG+Ut6E5p582Nium7y/0szv5nScDN+QDKru+l9rFmtb5tv69jWjba2PeroDhS6YU+XsKNLpNBlFv+Y7my6mDxqTKvRdgvFP4HrdT0k7c97WO7heb1BeSalk/Kq3pjg4MbT5TNuJnjVmqnWHFZ3YC01a5qq1kKzZkGLllVa2zxRrWoWhcqsVHUomduhlXwPrbpflW+l8q3I4dCqZlGp6lSqvhXH7cDqEpWES1QlXEIaSmuVh0tIRDH/hok6hVxCRRUnlPTQ7NTcnVcHwAUmf+hEn/gu6OnoU9+lupNUXT4uU0fdZeqicPpMd7k+aDlHR2mtpIP94FR2BS/lBTYN2wYp30iZSJlJOZA2J9g/vAvWe3CFO+9wWlBYwRUwwhP7wvoUDIlDAoz4gtGXi584ddZnUEhwCozBF4y+zI44y4AxnoJxOhUQmjhH3yL2zRG3jHELz9MrYvTlYiQuEbeKcXG6Ba4EwRVw7FsVNrguLuqBO86oB+76ot4G38VFPXDHGfU2cGMl9hlwFxf1NnByEAf05YwQjLjc7ohTD9xxRj1w5Iw2Po08U2oYNaFu0Se+wJF/Sm2jztQzxsIXOGqSYrx+6s8x2mkObdOdVvBfRv8l9Yz+qWEZ/ZfwX0b/JXWO/uX2sNMZ/rlFCubNYucfeXE7FM2RFzdB0Qo6+6i5p7ZRK+rpoz4eYxfnHr57/akz171gaBvnJL77caH+XO2CobnMVUzqS5nax1KmUuYy5Queoi8+Z1+2uv5IZ4iMeF/79cn+e7ZRb2gGuOH0z5rlfDzDPefk9u9n/87vxvcTg5vltmcejbzDwIvq/5fNf/+ySfWT17YUXhsdLE7o2yz6zbKPsTCj3hM=",
        },
        {
            "url": "http://pzv.jp/p.html?moonsun/15/15/928i4h492940i814g28h2h25248g0h01208g0h01200000000vvv0000003vvs00000fvvg0000vvv0000001800jn33l000f6ig100109inb6i4003a3f00600fclh01i0910032f31ii290003631lk5ai100",
            "test": False,
        },
    ],
}
