"""The Shimaguni solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import area, display, grid
from .utilsx.helper import mark_and_extract_clues
from .utilsx.region import full_bfs
from .utilsx.rule import adjacent, area_adjacent, avoid_area_adjacent, connected, count, shade_c
from .utilsx.solution import solver


def adjacent_area_different_size(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to enforce that adjacent areas have different sizes.

    An adjacent area rule and an area rule should be defined first.
    """
    size_count = f"#count {{R, C: area(A, R, C), {color}(R, C) }} = N"
    size1_count = f"#count {{R, C: area(A1, R, C), {color}(R, C) }} = N1"
    return f":- area_adj_{adj_type}(A, A1), A < A1, {size_count}, {size1_count}, N = N1."


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="darkgray"))
    solver.add_program_line(adjacent())

    clues = mark_and_extract_clues(solver, E.clues, shaded_color="darkgray", safe_color="green")
    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))

        tag = False
        for rc in ar:
            if rc in clues:
                solver.add_program_line(count(clues[rc], color="darkgray", _type="area", _id=i))
                tag = True
        if not tag:
            solver.add_program_line(count(1, op="ge", color="darkgray", _type="area", _id=i))

    solver.add_program_line(connected(color="darkgray", _type="area"))
    solver.add_program_line(avoid_area_adjacent(color="darkgray"))
    solver.add_program_line(area_adjacent())
    solver.add_program_line(adjacent_area_different_size(color="darkgray"))
    solver.add_program_line(display(color="darkgray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
