"""Solve Fillomino puzzles."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.helper import tag_encode
from .utilsx.rule import adjacent, fill_num
from .utilsx.solution import solver


def fillomino_connectivity(adj_type: int = 4) -> str:
    """Return a string representing the Fillomino puzzle connectivity rules."""

    tag = tag_encode("num_connectivity", adj_type)
    adj_num = f"adj_num(R, C, R1, C1) :- number(R, C, N), number(R1, C1, N), adj_{adj_type}(R, C, R1, C1)."

    initial = f"{tag}(R0, C0, R, C) :- grid(R, C), R = R0, C = C0."
    propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), grid(R, C), adj_num(R, C, R1, C1)."
    constraint = f":- grid(R, C), number(R, C, N), #count {{ R1, C1: {tag}(R, C, R1, C1) }} != N."

    return adj_num + "\n" + initial + "\n" + propagation + "\n" + constraint


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(adjacent())
    solver.add_program_line(fillomino_connectivity())

    max_num = E.R * E.C
    occurance = set()

    for (r, c), num in E.clues.items():
        max_num -= 1
        occurance.add(num)
        solver.add_program_line(f"number({r}, {c}, {num}).")
    max_num -= sum(occurance) - len(occurance)  # this bound is sort of conservative

    solver.add_program_line(fill_num(_range=f"1..{max_num}"))
    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
