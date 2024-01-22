"""The Norinori solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.regions import full_bfs
from .utilsx.rules import adjacent, area, count, display, grid, nori_adjacent, shade_c
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
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count(2, color="darkgray", _type="area", _id=i))

    for (r, c), clue in E.clues.items():
        if clue == "darkgray":
            solver.add_program_line(f"darkgray({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not darkgray({r}, {c}).")

    solver.add_program_line(display(color="darkgray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
