"""The Skyscrapers solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import grid, display
from .utilsx.rule import fill_num, unique_num
from .utilsx.solution import solver


def skyscraper_blocked_rule() -> str:
    """Generate rule for skyscraper puzzle."""
    blocked = "blocked_t(R, C) :- number(R, C, N), number(R1, C, N1), R1 < R, N1 > N.\n"
    blocked += "blocked_b(R, C) :- number(R, C, N), number(R1, C, N1), R1 > R, N1 > N.\n"
    blocked += "blocked_l(R, C) :- number(R, C, N), number(R, C1, N1), C1 < C, N1 > N.\n"
    blocked += "blocked_r(R, C) :- number(R, C, N), number(R, C1, N1), C1 > C, N1 > N."
    return blocked


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    if E.R != E.C:
        raise ValueError("Skyscrapers puzzles must be square.")
    n = E.R

    solver.reset()
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=f"1..{n}"))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(unique_num(_type="col", color="grid"))
    solver.add_program_line(skyscraper_blocked_rule())

    for c, num in E.top.items():
        solver.add_program_line(f":- #count {{ R: blocked_t(R, {c}) }} != {n - num}.")

    for c, num in E.bottom.items():
        solver.add_program_line(f":- #count {{ R: blocked_b(R, {c}) }} != {n - num}.")

    for r, num in E.left.items():
        solver.add_program_line(f":- #count {{ C: blocked_l({r}, C) }} != {n - num}.")

    for r, num in E.right.items():
        solver.add_program_line(f":- #count {{ C: blocked_r({r}, C) }} != {n - num}.")

    for (r, c), num in E.clues.items():
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
