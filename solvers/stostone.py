"""The Stostone solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import area, display, grid
from .utilsx.helper import mark_and_extract_clues
from .utilsx.region import full_bfs
from .utilsx.rule import adjacent, avoid_area_adjacent, connected, count, shade_c
from .utilsx.solution import solver


def valid_stostone(color: str = "black") -> str:
    """
    Generate a constraint to enforce a valid stostone dropping.

    A grid rule should be defined first.
    """
    below_C = f"grid(R, C), {color}(R, C), #count {{ R1: grid(R1, C), {color}(R1, C), R1 < R }} = BC"
    below_C1 = f"grid(R, C + 1), {color}(R, C + 1), #count {{ R1: grid(R1, C + 1), {color}(R1, C + 1), R1 < R }} = BC1"
    return f":- {below_C}, {below_C1}, BC != BC1."


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    if E.R % 2 != 0:
        raise ValueError("The stostone grid must have an even # rows.")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(count(E.R // 2, color="gray", _type="col"))

    clues = mark_and_extract_clues(solver, E.clues, shaded_color="gray", safe_color="green")
    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))

        tag = False
        for rc in ar:
            if rc in clues:
                solver.add_program_line(count(clues[rc], color="gray", _type="area", _id=i))
                tag = True
        if not tag:
            solver.add_program_line(count(1, op="ge", color="gray", _type="area", _id=i))

    solver.add_program_line(connected(color="gray", _type="area"))
    solver.add_program_line(avoid_area_adjacent(color="gray"))
    solver.add_program_line(valid_stostone(color="gray"))
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
