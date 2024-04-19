"""The Chocona solver."""

from typing import List, Dict

from .core.common import area, count, display, grid, shade_c
from .core.encoding import Encoding
from .core.helper import full_bfs, mark_and_extract_clues
from .core.neighbor import adjacent
from .core.shape import all_rect
from .core.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent())

    clues, rules = mark_and_extract_clues(E.clues, shaded_color="gray", safe_color="green")
    if clues:
        areas = full_bfs(E.R, E.C, E.edges, clues)
        for i, (ar, rc) in enumerate(areas.items()):
            solver.add_program_line(area(_id=i, src_cells=ar))
            if rc:
                solver.add_program_line(count(clues[rc], color="gray", _type="area", _id=i))

    solver.add_program_line(rules)
    solver.add_program_line(all_rect(color="gray"))
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
