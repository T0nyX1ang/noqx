"""The Hitori solver."""

from typing import List, Dict

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import (
    avoid_adjacent,
    col_num_unique,
    connected,
    display,
    grid,
    orth_adjacent,
    row_num_unique,
    shade_c,
)
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(row_num_unique(color="not black"))
    solver.add_program_line(col_num_unique(color="not black"))
    solver.add_program_line(orth_adjacent())
    solver.add_program_line(avoid_adjacent())
    solver.add_program_line(connected(color="not black"))

    for (r, c), clue in E.clues.items():
        if isinstance(clue, list):
            assert clue[1] == "black"  # initial color is gray
            solver.add_program_line(f"black({r}, {c}).")
        else:
            num = int(clue)
            solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
