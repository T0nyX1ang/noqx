"""The Country Road solver."""

from typing import Dict, List

from .core.common import area, count, direction, display, fill_path, grid, shade_c
from .core.encoding import Encoding
from .core.helper import full_bfs
from .core.loop import pass_area_once, single_loop
from .core.neighbor import adjacent, avoid_area_adjacent
from .core.reachable import grid_color_connected
from .core.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="country_road"))
    solver.add_program_line(fill_path(color="country_road"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="country_road", adj_type="loop"))
    solver.add_program_line(single_loop(color="country_road"))

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(pass_area_once(ar))

        for rc in ar:
            if rc in E.clues:
                solver.add_program_line(count(E.clues[rc], color="country_road", _type="area", _id=i))

    solver.add_program_line(avoid_area_adjacent(color="not country_road", adj_type=4))
    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions
