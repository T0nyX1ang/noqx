"""The Lits solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import area, display, grid, omino
from .utilsx.helper import tag_encode
from .utilsx.region import full_bfs
from .utilsx.rule import adjacent, area_adjacent, connected, count, shade_c
from .utilsx.shape import avoid_rect, valid_omino
from .utilsx.solution import solver


def avoid_adjacent_same_omino(num: int = 4, color: str = "black", adj_type: int = 4) -> None:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An area adjacent rule, an omino rule should be defined first.
    """
    tag = tag_encode("valid_omino", num, color)
    return f":- area_adj_{adj_type}_{color}(A, A1), A < A1, {tag}(A, T, _, _), {tag}(A1, T1, _, _), T = T1."


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset(mode="shade")
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(omino(4, ["L", "I", "T", "S"]))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(connected(color="gray"))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count(4, color="gray", _type="area", _id=i))

    solver.add_program_line(connected(color="gray", _type="area"))
    solver.add_program_line(valid_omino(4, color="gray", _type="area"))
    solver.add_program_line(area_adjacent(color="gray"))
    solver.add_program_line(avoid_adjacent_same_omino(4, color="gray"))

    for (r, c), clue in E.clues.items():
        if clue == "gray":
            solver.add_program_line(f"gray({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
