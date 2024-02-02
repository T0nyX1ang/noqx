"""The Nurikabe solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import adjacent, connected, count_region, region, shade_c
from .utilsx.shape import avoid_rect
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    # Reduce IntVar size by counting clue cells and assigning each one an id.
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(connected(color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))

    all_src = []
    for (r, c), clue in E.clues.items():
        if isinstance(clue, int) or clue == "yellow":
            all_src.append((r, c))

    if not all_src:
        raise ValueError("No clues found.")

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        else:
            current_excluded = [src for src in all_src if src != (r, c)]
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(region((r, c), current_excluded, color="not black", avoid_unknown=True))

            if clue != "yellow":
                num = int(clue)
                solver.add_program_line(count_region(num, (r, c), color="not black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
