"""The Shimaguni solver."""

from typing import Dict, List

from .utilsx.common import area, count, display, grid, shade_c
from .utilsx.encoding import Encoding
from .utilsx.helper import full_bfs, mark_and_extract_clues
from .utilsx.neighbor import adjacent, area_adjacent, avoid_area_adjacent
from .utilsx.reachable import area_color_connected
from .utilsx.solution import solver


def adjacent_area_different_size(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to enforce that adjacent areas have different sizes.

    An adjacent area rule and an area rule should be defined first.
    """
    size_count = f"#count {{R, C: area(A, R, C), {color}(R, C) }} = N"
    size1_count = f"#count {{R, C: area(A1, R, C), {color}(R, C) }} = N1"
    return f":- area_adj_{adj_type}(A, A1), A < A1, {size_count}, {size1_count}, N = N1."


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())

    clues, rules = mark_and_extract_clues(E.clues, shaded_color="gray", safe_color="green")
    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))

        tag = False
        for rc in ar:
            if rc in clues:
                solver.add_program_line(count(clues[rc], color="gray", _type="area", _id=i))
                tag = True
        if not tag:
            solver.add_program_line(count(("ge", 1), color="gray", _type="area", _id=i))

    solver.add_program_line(rules)
    solver.add_program_line(area_color_connected(color="gray"))
    solver.add_program_line(avoid_area_adjacent(color="gray"))
    solver.add_program_line(area_adjacent())
    solver.add_program_line(adjacent_area_different_size(color="gray"))
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
