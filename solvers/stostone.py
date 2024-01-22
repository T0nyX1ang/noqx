"""The Stostone solver."""

from typing import List

from . import utilsx
from .utilsx.borders import Direction
from .utilsx.encoding import Encoding
from .utilsx.regions import full_bfs
from .utilsx.rules import (
    adjacent,
    area,
    avoid_rect,
    connected_in_area,
    count,
    display,
    grid,
    reachable_in_area,
    shade_c,
)
from .utilsx.solutions import solver


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
    solver.add_program_line(shade_c(color="darkgray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(count(E.R // 2, color="darkgray", _type="col"))

    clues = {}  # remove color-relevant clues here
    for (r, c), clue in E.clues.items():
        if isinstance(clue, list):
            if clue[1] == "darkgray":
                solver.add_program_line(f"darkgray({r}, {c}).")
            elif clue[1] == "green":
                solver.add_program_line(f"not darkgray({r}, {c}).")
            clues[(r, c)] = int(clue[0])
        elif clue == "darkgray":
            solver.add_program_line(f"darkgray({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not darkgray({r}, {c}).")
        else:
            clues[(r, c)] = int(clue)

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

        solver.add_program_line(reachable_in_area(_id=i, color="darkgray"))
        solver.add_program_line(connected_in_area(_id=i, color="darkgray"))

    for r in range(E.R):
        borders_in_row = [c for c in range(1, E.C) if (r, c, Direction.LEFT) in E.edges]
        for i in borders_in_row:
            solver.add_program_line(avoid_rect(1, 2, color="darkgray", corner=(r, i - 1)))

    for c in range(E.C):
        borders_in_col = [r for r in range(1, E.R) if (r, c, Direction.TOP) in E.edges]
        for i in borders_in_col:
            solver.add_program_line(avoid_rect(2, 1, color="darkgray", corner=(i - 1, c)))

    solver.add_program_line(valid_stostone(color="darkgray"))
    solver.add_program_line(display(color="darkgray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
