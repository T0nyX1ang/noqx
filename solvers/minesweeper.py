"""The blacksweeper solver."""

from typing import Dict, List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import (
    adjacent_num,
    count,
    diag_adjacent,
    display,
    grid,
    orth_adjacent,
    shade_nc,
)
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List[Dict[str, str]]:
    mine_count = E.params["m"]

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_nc(num_range="0..8", color="black"))
    solver.add_program_line(orth_adjacent())
    solver.add_program_line(diag_adjacent())
    solver.add_program_line(adjacent_num())

    print(E.clues.items())

    for (r, c), clue in E.clues.items():
        if isinstance(clue, list):
            assert clue[2] == "black"
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        else:
            solver.add_program_line(f"number({r}, {c}, {clue}).")

    if mine_count:
        solver.add_program_line(count(mine_count, color="black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
