"""The Nurimisaki solver."""

from typing import List, Tuple

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import adjacent, connected, count_adjacent, count_lit, lit, shade_c
from .utilsx.shape import avoid_rect
from .utilsx.solution import solver


def avoid_unknown_misaki(known_cells: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to avoid dead ends that does not have a record.

    A grid rule and an adjacent rule should be defined first.
    """

    included = ", ".join(f"|R - {src_r}| + |C - {src_c}| != 0" for src_r, src_c in known_cells)
    main = f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }} = 1."

    if not known_cells:
        return main
    return f"{main}, {included}."


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
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
