"""The Aqre solver."""

from typing import Dict, List

from .core.common import area, count, display, grid, shade_c
from .core.encoding import Encoding
from .core.helper import full_bfs, mark_and_extract_clues
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="gray"))
    solver.add_program_line(avoid_rect(4, 1, color="gray"))
    solver.add_program_line(avoid_rect(1, 4, color="gray"))
    solver.add_program_line(avoid_rect(4, 1, color="not gray"))
    solver.add_program_line(avoid_rect(1, 4, color="not gray"))

    clues, rules = mark_and_extract_clues(E.clues, shaded_color="gray", safe_color="green")
    if clues:
        areas = full_bfs(E.R, E.C, E.edges, clues)
        for i, (ar, rc) in enumerate(areas.items()):
            solver.add_program_line(area(_id=i, src_cells=ar))
            if rc:
                solver.add_program_line(count(clues[rc], color="gray", _type="area", _id=i))

    solver.add_program_line(rules)
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
