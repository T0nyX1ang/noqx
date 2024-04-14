"""Akari (Light up) solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding, tag_encode
from .utilsx.fact import display, grid
from .utilsx.rule import adjacent, count_adjacent
from .utilsx.solution import solver


def lightup(color: str = "black") -> str:
    """
    A lit rule specially designed for akari.

    A grid fact and an adjacent rule should be defined first.
    """
    tag = tag_encode("reachable", "bulb", "branch", "adj", 4, color)
    initial = f"{tag}(R0, C0, R, C) :- grid(R, C), bulb(R, C), R0 = R, C0 = C."
    propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), {color}(R, C), adj_4(R, C, R1, C1), (R - R0) * (C - C0) = 0."
    constraint1 = f":- bulb(R0, C0), bulb(R, C), |R0 - R| + |C0 - C| != 0, {tag}(R0, C0, R, C)."
    constraint2 = f":- grid(R, C), not black(R, C), not bulb(R, C), {{ {tag}(R0, C0, R, C) }} = 0."

    return initial + "\n" + propagation + "\n" + constraint1 + "\n" + constraint2


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line("{ bulb(R, C) } :- grid(R, C), not black(R, C).")
    solver.add_program_line(adjacent())
    solver.add_program_line(lightup(color="not black"))

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "o":
            solver.add_program_line(f"bulb({r}, {c}).")
        else:
            num = int(clue)
            solver.add_program_line(f"black({r}, {c}).")
            solver.add_program_line(count_adjacent(num, (r, c), color="bulb"))

    solver.add_program_line(display(item="bulb"))
    solver.solve()

    for solution in solver.solutions:
        for rc, color in solution.items():
            if color == "bulb":
                solution[rc] = "bulb.png"

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
