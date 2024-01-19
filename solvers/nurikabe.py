"""The Nurikabe solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.rules import (
    avoid_rect,
    avoid_unknown_region,
    count_connected_from_src,
    display,
    grid,
    orth_adjacent,
    reachable_from_src,
    shade_c,
    reachable,
    connected,
)
from .utilsx.solutions import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    # Reduce IntVar size by counting clue cells and assigning each one an id.
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(orth_adjacent())
    solver.add_program_line(reachable(color="black"))
    solver.add_program_line(connected(color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))

    all_src = []
    for (r, c), clue in E.clues.items():
        if isinstance(clue, int) or clue == "yellow":
            all_src.append((r, c))

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        else:
            current_excluded = [src for src in all_src if src != (r, c)]
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(reachable_from_src((r, c), current_excluded, color="not black"))

            if clue != "yellow":
                num = int(clue)
                solver.add_program_line(count_connected_from_src(num, (r, c), color="not black"))

    solver.add_program_line(avoid_unknown_region(all_src, color="not black"))
    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
