"""The Norinori solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.regions import full_bfs
from .utilsx.rules import adjacent, area, grid, shade_c, count, display, nori_adjacent
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c("darkgray"))

    solver.add_program_line(adjacent())
    solver.add_program_line(nori_adjacent(color="darkgray"))

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(i, src_cells=ar))
        solver.add_program_line(count(2, color="darkgray", _type=f"area_{i}"))

    for (r, c), clues in E.clues.items():
        if clues == "darkgray":
            solver.add_program_line(f"darkgray({r}, {c}).")
        elif clues == "green":
            solver.add_program_line(f"not darkgray({r}, {c}).")

    solver.add_program_line(display(color="darkgray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
