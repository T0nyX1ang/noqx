"""The Shimaguni solver."""

from typing import List

from . import utilsx
from .utilsx.borders import Direction
from .utilsx.encoding import Encoding
from .utilsx.regions import full_bfs
from .utilsx.rules import (
    adjacent,
    area,
    area_adjacent,
    avoid_rect,
    connected,
    count,
    display,
    grid,
    shade_c,
)
from .utilsx.solutions import solver


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

        solver.add_program_line(connected(area_id=i, color="darkgray"))

    for r in range(E.R):
        borders_in_row = [c for c in range(1, E.C) if (r, c, Direction.LEFT) in E.edges]
        for i in borders_in_row:
            solver.add_program_line(avoid_rect(1, 2, color="darkgray", corner=(r, i - 1)))

    for c in range(E.C):
        borders_in_col = [r for r in range(1, E.R) if (r, c, Direction.TOP) in E.edges]
        for i in borders_in_col:
            solver.add_program_line(avoid_rect(2, 1, color="darkgray", corner=(i - 1, c)))

    solver.add_program_line(area_adjacent())
    solver.add_program_line(adjacent_area_different_size(color="darkgray"))
    solver.add_program_line(display(color="darkgray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
