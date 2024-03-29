"""The Moon-or-Sun solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import area, direction, display, grid
from .utilsx.loop import connected_loop, fill_path, pass_area_one_time, single_loop
from .utilsx.region import full_bfs
from .utilsx.rule import adjacent, area_adjacent, shade_c
from .utilsx.solution import solver


def moon_sun_area() -> str:
    """
    Genearate a constraint to determine the area of the moon or sun.
    A sun area should only contain sun cells, and a moon area should only contain moon cells.
    A sun area should be adjacent to a moon area, and vice versa.

    A grid fact and an area adjacent rule should be defined first.
    """
    rule = "{ sun_area(A) } :- area(A, _, _).\n"
    rule += ":- sun_area(A), area(A, R, C), sun(R, C), not moon_sun_loop(R, C).\n"
    rule += ":- sun_area(A), area(A, R, C), moon(R, C), moon_sun_loop(R, C).\n"
    rule += ":- not sun_area(A), area(A, R, C), sun(R, C), moon_sun_loop(R, C).\n"
    rule += ":- not sun_area(A), area(A, R, C), moon(R, C), not moon_sun_loop(R, C).\n"

    constraint = ":- area_adj_loop(A1, A2), sun_area(A1), sun_area(A2).\n"
    constraint += ":- area_adj_loop(A1, A2), not sun_area(A1), not sun_area(A2).\n"
    return (rule + constraint).strip()


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="moon_sun_loop"))
    solver.add_program_line(fill_path(color="moon_sun_loop"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(connected_loop(color="moon_sun_loop"))
    solver.add_program_line(single_loop(color="moon_sun_loop"))

    for (r, c), clue in E.clues.items():
        if clue == "m":
            solver.add_program_line(f"moon({r}, {c}).")
        elif clue == "s":
            solver.add_program_line(f"sun({r}, {c}).")

    areas = full_bfs(E.R, E.C, E.edges)
    assert len(areas) % 2 == 0, "The number of areas should be even."
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(pass_area_one_time(ar))

    solver.add_program_line(area_adjacent(adj_type="loop"))
    solver.add_program_line(moon_sun_area())
    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
