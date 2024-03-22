"""The Shikaku solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, edge, grid
from .utilsx.rule import adjacent
from .utilsx.shape import all_rect_region
from .utilsx.solution import solver


def shikaku_constraint() -> str:
    """Generate a constraint for shikaku."""
    size_range = "R1 >= R, R1 <= MR, C1 >= C, C1 <= MC"
    size_spawn = f"rect_size(R1, C1, S) :- grid(R1, C1), rect(R, C, MR, MC), S = (MR - R + 1) * (MC - C + 1), {size_range}."
    unique = f":- rect(R, C, MR, MC), #count {{ R1, C1: clue(R1, C1), {size_range} }} != 1."

    return size_spawn + "\n" + unique


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    if len(E.clues) == 0:
        raise ValueError("Please provide at least one clue.")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(all_rect_region())
    solver.add_program_line(shikaku_constraint())

    for (r, c), clue in E.clues.items():
        solver.add_program_line(f"clue({r}, {c}).")
        if clue != "?":
            num = int(clue)
            solver.add_program_line(f":- not rect_size({r}, {c}, {num}).")

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
