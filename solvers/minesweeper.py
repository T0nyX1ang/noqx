"""The blacksweeper solver."""

from typing import Dict, List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import (
    diag_adjacent,
    display,
    grid,
    orth_adjacent,
    ranged,
    shade_without_num,
)
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(ranged(0, 8))
    solver.add_program_line(shade_without_num())
    solver.add_program_line(orth_adjacent())
    solver.add_program_line(diag_adjacent())
    solver.add_program_line("{black(R1, C1) : adj(R, C, R1, C1)} = N :- number(R, C, N).")

    for (r, c), num in E.clues.items():
        if num != "?":
            solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display())
    solver.solve()
    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
