"""The Aqre solver."""

from typing import List

from . import utilsx
from .utilsx.common import area, display, grid
from .utilsx.encoding import Encoding
from .utilsx.helper import full_bfs, mark_and_extract_clues
from .utilsx.reachable import grid_color_connected
from .utilsx.rule import adjacent, count, shade_c
from .utilsx.shape import avoid_rect
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
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
        if isinstance(areas, dict):
            for i, (rc, ar) in enumerate(areas.items()):
                solver.add_program_line(area(_id=i, src_cells=ar))
                solver.add_program_line(count(clues[rc], color="gray", _type="area", _id=i))

    solver.add_program_line(rules)
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
