"""The Tents solver."""

import itertools
from typing import List, Tuple

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import adjacent, avoid_adjacent, count, shade_c
from .utilsx.solution import solver

neighbor_offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))


def identical_adjacent_map(known_cells: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate n * (n - 1) / 2 constraints and n rules to enfroce identical adjacent cell maps.

    A grid fact and an adjacent rule should be defined first. n is the number of known source cells.
    """
    rules = "\n".join(
        f"{{ map_{r}_{c}(R, C): adj_{adj_type}(R, C, {r}, {c}), {color}(R, C) }} = 1 :- grid({r}, {c})."
        for r, c in known_cells
    )  # n rules are generated
    constraints = "\n".join(
        f":- map_{r1}_{c1}(R, C), map_{r2}_{c2}(R, C). "
        for (r1, c1), (r2, c2) in itertools.combinations(known_cells, 2)
    )  # n * (n - 1) / 2 constraints are generated
    return rules + "\n" + constraints


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    solver.reset(mode="shade")
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_adjacent(color="black", adj_type=8))

    all_trees = []
    for (r, c), clue in E.clues.items():
        if clue == "e":
            all_trees.append((r, c))
            solver.add_program_line(f"not black({r}, {c}).")
        elif clue == "n":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")

    for c, num in E.top.items():
        solver.add_program_line(count(int(num), color="black", _type="col", _id=c))

    for r, num in E.left.items():
        solver.add_program_line(count(int(num), color="black", _type="row", _id=r))

    solver.add_program_line(identical_adjacent_map(all_trees, color="black", adj_type=4))
    solver.add_program_line(count(len(all_trees), color="black", _type="grid"))
    solver.add_program_line(display(item="black"))
    solver.solve()

    for solution in solver.solutions:
        for rc, color in solution.items():
            if color == "black":
                solution[rc] = "tent.png"

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
