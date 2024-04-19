"""The Heyawake solver."""

from typing import Dict, List

from .core.common import area, count, display, grid, shade_c
from .core.encoding import Direction, Encoding
from .core.helper import full_bfs, mark_and_extract_clues
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.reachable import grid_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c("gray"))

    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="gray"))
    solver.add_program_line(grid_color_connected(color="not gray"))

    clues, rules = mark_and_extract_clues(E.clues, shaded_color="gray", safe_color="green")
    if clues:
        areas = full_bfs(E.R, E.C, E.edges, clues)
        if isinstance(areas, dict):
            for i, (ar, rc) in enumerate(areas.items()):
                solver.add_program_line(area(_id=i, src_cells=ar))
                if rc:
                    solver.add_program_line(count(clues[rc], color="gray", _type="area", _id=i))

    for r in range(E.R):
        borders_in_row = [c for c in range(1, E.C) if (r, c, Direction.LEFT) in E.edges]
        for i in range(len(borders_in_row) - 1):
            b1, b2 = borders_in_row[i], borders_in_row[i + 1]
            solver.add_program_line(avoid_rect(1, b2 - b1 + 2, color="not gray", corner=(r, b1 - 1)))

    for c in range(E.C):
        borders_in_col = [r for r in range(1, E.R) if (r, c, Direction.TOP) in E.edges]
        for i in range(len(borders_in_col) - 1):
            b1, b2 = borders_in_col[i], borders_in_col[i + 1]
            solver.add_program_line(avoid_rect(b2 - b1 + 2, 1, color="not gray", corner=(b1 - 1, c)))

    solver.add_program_line(rules)
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
