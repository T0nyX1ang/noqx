"""The Doppelblock solver."""

from typing import List

from . import utilsx
from .utilsx.common import count, display, fill_num, grid, unique_num
from .utilsx.encoding import Encoding
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    assert E.R == E.C, "Doppelblock puzzles must be square."
    n = E.R

    solver.reset()
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=range(1, n - 1), color="black"))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(count(2, _type="row", color="black"))
    solver.add_program_line(unique_num(_type="col", color="grid"))
    solver.add_program_line(count(2, _type="col", color="black"))

    for c, num in E.top.items():
        begin_r = f"Rb = #min {{ R: black(R, {c}) }}"
        end_r = f"Re = #max {{ R: black(R, {c}) }}"
        solver.add_program_line(f":- {begin_r}, {end_r}, #sum {{ N: number(R, {c}, N), R > Rb, R < Re }} != {num}.")

    for r, num in E.left.items():
        begin_c = f"Cb = #min {{ C: black({r}, C) }}"
        end_c = f"Ce = #max {{ C: black({r}, C) }}"
        solver.add_program_line(f":- {begin_c}, {end_c}, #sum {{ N: number({r}, C, N), C > Cb, C < Ce }} != {num}.")

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        else:
            num = int(clue)
            solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))
    solver.add_program_line(display(item="black", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
