"""The Hitori solver."""

from typing import Dict, List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import (
    adjacent,
    avoid_adjacent,
    connected,
    display,
    grid,
    reachable,
    shade_c,
    unique_num,
)
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(unique_num(color="not black", _type="row"))
    solver.add_program_line(unique_num(color="not black", _type="col"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent())
    solver.add_program_line(reachable(color="not black"))
    solver.add_program_line(connected(color="not black"))

    for (r, c), clue in E.clues.items():
        if isinstance(clue, list):
            if clue[1] == "black":
                solver.add_program_line(f"black({r}, {c}).")
            elif clue[1] == "green":
                num = int(clue[0])
                solver.add_program_line(f"not black({r}, {c}).")
                solver.add_program_line(f"number({r}, {c}, {num}).")
        else:
            num = int(clue)
            solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
