"""The Aquarium solver."""

from typing import Dict, List

from .core.common import area, count, display, grid, shade_c
from .core.encoding import Encoding
from .core.helper import full_bfs
from .core.solution import solver


def area_gravity(color: str = "black") -> str:
    """
    Generates a constraint to fill the {color} areas according to gravity.

    A grid rule should be defined first.
    """
    target = f":- area(A, R, C), area(A, R1, C1), R1 >= R, {color}(R, C), not {color}(R1, C1)."
    return target.replace("not not ", "")


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="blue"))

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(area_gravity(color="blue"))

    for c, num in E.top.items():
        solver.add_program_line(count(int(num), color="blue", _type="col", _id=c))

    for r, num in E.left.items():
        solver.add_program_line(count(int(num), color="blue", _type="row", _id=r))

    for (r, c), clue in E.clues.items():
        if clue == "blue":
            solver.add_program_line(f"blue({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not blue({r}, {c}).")

    solver.add_program_line(display(item="blue"))
    solver.solve()

    return solver.solutions
