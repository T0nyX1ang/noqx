"""The Country Road solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid, area
from .utilsx.loop import single_loop, connected_loop, fill_path, pass_area_one_time
from .utilsx.rule import adjacent, count, shade_c
from .utilsx.region import full_bfs
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="country_road"))
    solver.add_program_line(fill_path(color="country_road"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(connected_loop(color="country_road"))
    solver.add_program_line(single_loop(color="country_road", visit_all=True))

    num_dict = {}
    for (r, c), clue in E.clues.items():
        num_dict[(r, c)] = clue

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        for r, c in ar:
            if (r, c) in num_dict:
                solver.add_program_line(area(_id=i, src_cells=ar))
                solver.add_program_line(count(num_dict[(r, c)], color="country_road", _type="area", _id=i))
            if (r + 1, c) not in ar and r + 1 < E.R:
                solver.add_program_line(f":- not country_road({r}, {c}), not country_road({r+1}, {c}).")
            if (r, c + 1) not in ar and c + 1 < E.C:
                solver.add_program_line(f":- not country_road({r}, {c}), not country_road({r}, {c+1}).")
        solver.add_program_line(pass_area_one_time(ar))

    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
