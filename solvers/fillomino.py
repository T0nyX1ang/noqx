"""Solve Fillomino puzzles."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid, edge
from .utilsx.rule import adjacent, reachable_edge, fill_num
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def fillomino_constraint():
    """Generate the Fillomino constraints."""
    # propagation of number
    constraint = "number(R, C, N) :- number(R0, C0, N), reachable_edge(R0, C0, R, C).\n"
    constraint += ":- number(R0, C0, N), #count { R, C: reachable_edge(R0, C0, R, C) } != N.\n"

    # same number, adjacent cell, no line
    constraint += ":- number(R, C, N), number(R, C + 1, N), vertical_line(R, C + 1).\n"
    constraint += ":- number(R, C, N), number(R + 1, C, N), horizontal_line(R + 1, C).\n"

    # different number, adjacent cell, have line
    constraint += ":- number(R, C, N1), number(R, C + 1, N2), N1 != N2, not vertical_line(R, C + 1).\n"
    constraint += ":- number(R, C, N1), number(R + 1, C, N2), N1 != N2, not horizontal_line(R + 1, C).\n"

    # special case for 1
    mutual = ["horizontal_line(R, C)", "horizontal_line(R + 1, C)", "vertical_line(R, C)", "vertical_line(R, C + 1)"]
    constraint += f"{{ {'; '.join(mutual)} }} = 4 :- number(R, C, 1).\n"
    constraint += f"number(R, C, 1) :- {', '.join(mutual)}.\n"
    constraint += ":- number(R, C, 1), number(R1, C1, 1), adj_4(R, C, R1, C1).\n"

    return constraint.strip()


def fillomino_slow() -> str:
    """Generate the Fillomino rules for precise solving."""
    count_edge = "#count{ R1, C1: reachable_edge(R, C, R1, C1) } = N"
    slow = f":- adj_4(R, C, R0, C0), not reachable_edge(R, C, R0, C0), number(R0, C0, N), {count_edge}.\n"
    slow += f"{{ numberx(R, C, N) }} = 1 :- grid(R, C), not number(R, C, _), {count_edge}.\n"
    slow += ":- numberx(R, C, N), numberx(R1, C1, N), not reachable_edge(R, C, R1, C1), adj_4(R, C, R1, C1).\n"
    return slow.strip()


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(4))
    solver.add_program_line(adjacent("edge"))
    solver.add_program_line(reachable_edge())
    solver.add_program_line(fillomino_constraint())

    occurances = {1, 2, 3, 4, 5}
    for (r, c), num in E.clues.items():
        occurances.add(num)
        solver.add_program_line(f"number({r}, {c}, {num}).")

        if num == 1:
            solver.add_program_line(f"vertical_line({r}, {c}).")
            solver.add_program_line(f"horizontal_line({r}, {c}).")
            solver.add_program_line(f"vertical_line({r}, {c + 1}).")
            solver.add_program_line(f"horizontal_line({r + 1}, {c}).")

        if (r, c + 1) in E.clues:
            prefix = "not" if E.clues[(r, c + 1)] == num else ""
            solver.add_program_line(f"{prefix} vertical_line({r}, {c + 1}).".strip())

        if (r + 1, c) in E.clues:
            prefix = "not" if E.clues[(r + 1, c)] == num else ""
            solver.add_program_line(f"{prefix} horizontal_line({r + 1}, {c}).".strip())

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.add_program_line(display(item="number", size=3))

    if E.params["fast"]:
        solver.add_program_line(fill_num(_range=occurances))
    else:
        solver.add_program_line(fillomino_slow())
        solver.add_program_line(display(item="numberx", size=3))

    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
