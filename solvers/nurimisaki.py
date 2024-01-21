"""The Nurimisaki solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import (
    adjacent,
    avoid_rect,
    avoid_unknown_misaki,
    connected,
    count_adjacent,
    count_lit,
    display,
    grid,
    lit,
    reachable,
    shade_c,
)
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(reachable(color="not black"))
    solver.add_program_line(connected(color="not black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="not black"))

    all_src = []
    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        elif clue == "yellow":
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(count_adjacent(1, (r, c), color="not black"))
            all_src.append((r, c))
        else:
            num = int(clue)
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(count_adjacent(1, (r, c), color="not black"))
            solver.add_program_line(lit((r, c), color="not black"))
            solver.add_program_line(count_lit(num, (r, c), color="not black"))
            all_src.append((r, c))

    solver.add_program_line(avoid_unknown_misaki(all_src, color="not black"))
    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
