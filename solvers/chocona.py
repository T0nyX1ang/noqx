"""The Chocona solver."""

from typing import List

from .utilsx.common import area, count, display, grid, shade_c
from .utilsx.encoding import Encoding
from .utilsx.helper import full_bfs, mark_and_extract_clues
from .utilsx.neighbor import adjacent
from .utilsx.shape import all_rect
from .utilsx.solution import solver


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent())

    clues, rules = mark_and_extract_clues(E.clues, shaded_color="gray", safe_color="green")
    if clues:
        areas = full_bfs(E.R, E.C, E.edges, clues)
        if isinstance(areas, dict):
            for i, (rc, ar) in enumerate(areas.items()):
                solver.add_program_line(area(_id=i, src_cells=ar))
                solver.add_program_line(count(clues[rc], color="gray", _type="area", _id=i))

    solver.add_program_line(rules)
    solver.add_program_line(all_rect(color="gray"))
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
