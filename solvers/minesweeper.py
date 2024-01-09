"""The blacksweeper solver."""

from typing import Dict, List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import get_grid_rule, get_ranged_number_rule, get_surroundings_rule
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(get_grid_rule(E.R, E.C))
    solver.add_program_line(get_ranged_number_rule(0, 8))
    solver.add_program_line("1 {number(R, C, N) : range(N) ; black(R, C)} 1 :- grid(R, C).")
    solver.add_program_line(get_surroundings_rule())
    solver.add_program_line("N {black(R1, C1) : adj(R, C, R1, C1)} N :- number(R, C, N).")

    for cell, num in E.clues.items():
        r, c = cell
        if num != "?":
            solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line("#show black/2.")
    solver.solve()
    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
