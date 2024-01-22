"""The Tents solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import (
    adjacent,
    avoid_adjacent,
    count,
    count_adjacent,
    display,
    grid,
    shade_c,
)
from .utilsx.solutions import solver

neighbor_offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_adjacent(color="black", adj_type=8))

    total_trees = 0
    for (r, c), clue in E.clues.items():
        if clue == "e":
            total_trees += 1
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(count_adjacent(1, color="black", adj_type=4, src_cell=(r, c)).replace("!=", "<"))
        elif clue == "n":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")

    for c, num in E.top.items():
        solver.add_program_line(count(int(num), color="black", _type="col", _id=c))

    for r, num in E.left.items():
        solver.add_program_line(count(int(num), color="black", _type="row", _id=r))

    solver.add_program_line(count(total_trees, color="black", _type="grid"))
    solver.add_program_line(display(color="black"))
    solver.solve()

    for solution in solver.solutions:
        for rc, color in solution.items():
            if color == "black":
                solution[rc] = "tent.png"

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
