"""The Moon-or-Sun solver."""

from typing import List

from .core.common import area, direction, display, fill_path, grid, shade_c
from .core.helper import full_bfs
from .core.loop import pass_area_once, single_loop
from .core.neighbor import adjacent, area_adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.solution import solver


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
