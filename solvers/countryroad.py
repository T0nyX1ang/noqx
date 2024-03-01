"""The Country Road solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import area, direction, display, grid
from .utilsx.loop import connected_loop, fill_path, pass_area_one_time, single_loop
from .utilsx.region import full_bfs
from .utilsx.rule import adjacent, avoid_area_adjacent, count, shade_c
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="country_road"))
    solver.add_program_line(fill_path(color="country_road"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(connected_loop(color="country_road"))
    solver.add_program_line(single_loop(color="country_road", visit_all=True))

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(pass_area_one_time(ar))

        for rc in ar:
            if rc in E.clues:
                solver.add_program_line(count(E.clues[rc], color="country_road", _type="area", _id=i))

    solver.add_program_line(avoid_area_adjacent(color="not country_road"))
    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
