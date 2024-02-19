"""Solve Fillomino puzzles."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid, edge
from .utilsx.rule import adjacent, reachable_edge
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def fillomino_count():
    constriant = ":- number(R0, C0, N), #count { R, C: reachable_edge(R0, C0, R, C) } != N.\n"

    # same number, adjacent cell, no line
    constriant += ":- number(R, C, N), number(R, C+1, N), vertical_line(R, C+1).\n"
    constriant += ":- number(R, C, N), number(R+1, C, N), horizontal_line(R+1, C).\n"

    # different number, adjacent cell, have line
    constriant += ":- number(R, C, N1), number(R, C+1, N2), N1 != N2, not vertical_line(R, C+1).\n"
    constriant += ":- number(R, C, N1), number(R+1, C, N2), N1 != N2, not horizontal_line(R+1, C).\n"

    # propagation of number
    constriant += "number(R, C, N) :- number(R0, C0, N), adj_edge(R0, C0, R, C).\n"

    # special case for 1
    constriant += "{ horizontal_line(R, C); horizontal_line(R+1, C); vertical_line(R, C); vertical_line(R, C+1) } = 4 :- number(R, C, 1).\n"
    constriant += "number(R, C, 1) :- horizontal_line(R, C), horizontal_line(R+1, C), vertical_line(R, C), vertical_line(R, C+1).\n"

    # case for unclued parts (unsafe)
    constriant += ":- adj_4(R0, C0, R, C), not adj_edge(R0, C0, R, C), number(R, C, N), #count{ R1, C1: reachable_edge(R0, C0, R1, C1) } = N.\n"
    return constriant.strip()


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(4))
    solver.add_program_line(adjacent("edge"))
    solver.add_program_line(reachable_edge())
    solver.add_program_line(fillomino_count())

    for r in range(E.R):
        solver.add_program_line(f"vertical_line({r}, {0}).")
        solver.add_program_line(f"vertical_line({r}, {E.C}).")
    for c in range(E.C):
        solver.add_program_line(f"horizontal_line({0}, {c}).")
        solver.add_program_line(f"horizontal_line({E.R}, {c}).")

    for (r, c), num in E.clues.items():
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.add_program_line(display(item="number", size=3))

    if not E.params["fast"]:  # precise solution
        solver.add_program_line(
            "{ numberx(R, C, N) } = 1 :- grid(R, C), not number(R, C, _), #count{ R1, C1: reachable_edge(R, C, R1, C1) } = N."
        )
        solver.add_program_line(
            ":- numberx(R, C, N), numberx(R1, C1, N), not adj_edge(R, C, R1, C1), adj_4(R, C, R1, C1)."
        )
        solver.add_program_line(display(item="numberx", size=3))

    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
