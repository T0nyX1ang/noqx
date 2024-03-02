"""The Skyscrapers solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import fill_num, unique_num
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    assert E.R == E.C, "Skyscrapers puzzles must be square."
    n = E.R

    solver.reset()
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=range(1, n + 1)))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(unique_num(_type="col", color="grid"))

    for c, num in E.top.items():
        solver.add_program_line(f"blocked_t(R, {c}) :- number(R, {c}, N), number(R1, {c}, N1), R1 < R, N1 > N.")
        solver.add_program_line(f":- #count {{ R: blocked_t(R, {c}) }} != {n - num}.")

    for c, num in E.bottom.items():
        solver.add_program_line(f"blocked_b(R, {c}) :- number(R, {c}, N), number(R1, {c}, N1), R1 > R, N1 > N.")
        solver.add_program_line(f":- #count {{ R: blocked_b(R, {c}) }} != {n - num}.")

    for r, num in E.left.items():
        solver.add_program_line(f"blocked_l({r}, C) :- number({r}, C, N), number({r}, C1, N1), C1 < C, N1 > N.")
        solver.add_program_line(f":- #count {{ C: blocked_l({r}, C) }} != {n - num}.")

    for r, num in E.right.items():
        solver.add_program_line(f"blocked_r({r}, C) :- number({r}, C, N), number({r}, C1, N1), C1 > C, N1 > N.")
        solver.add_program_line(f":- #count {{ C: blocked_r({r}, C) }} != {n - num}.")

    for (r, c), num in E.clues.items():
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
