"""The Aqre solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import area, display, grid
from .utilsx.helper import mark_and_extract_clues
from .utilsx.region import full_bfs
from .utilsx.rule import adjacent, connected, count, shade_c
from .utilsx.shape import avoid_rect
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(connected(color="gray"))
    solver.add_program_line(avoid_rect(4, 1, color="gray"))
    solver.add_program_line(avoid_rect(1, 4, color="gray"))
    solver.add_program_line(avoid_rect(4, 1, color="not gray"))
    solver.add_program_line(avoid_rect(1, 4, color="not gray"))

    clues = mark_and_extract_clues(solver, E.clues, shaded_color="gray", safe_color="green")
    if clues:
        areas = full_bfs(E.R, E.C, E.edges, clues)
        for i, (rc, ar) in enumerate(areas.items()):
            solver.add_program_line(area(_id=i, src_cells=ar))
            solver.add_program_line(count(clues[rc], color="gray", _type="area", _id=i))

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
