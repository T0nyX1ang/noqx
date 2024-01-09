"""The blacksweeper solver."""

from typing import Dict, List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import adjacent, display, grid, ranged, shading
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(ranged(0, 8))
    solver.add_program_line(shading())
    solver.add_program_line(adjacent())
    solver.add_program_line("N {black(R1, C1) : adj(R, C, R1, C1)} N :- number(R, C, N).")

    for (r, c), num in E.clues.items():
        if num != "?":
            solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display())
    solver.solve()
    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
