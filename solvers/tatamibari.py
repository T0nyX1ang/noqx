"""The Tatamibari solver."""

from typing import List

from . import utilsx
from .utils.encoding import Encoding
from .utilsx.fact import display, edge, grid
from .utilsx.rule import adjacent
from .utilsx.shape import all_rect_region
from .utilsx.solution import solver


def tatamibari_constraint() -> str:
    """Generate a constraint for tatamibari."""
    size_range = "R1 >= R, R1 <= MR, C1 >= C, C1 <= MC"
    size_spawn = f"rect_edge(R1, C1, 0) :- grid(R1, C1), rect(R, C, MR, MC), MR - R = MC - C, {size_range}.\n"
    size_spawn += f"rect_edge(R1, C1, 1) :- grid(R1, C1), rect(R, C, MR, MC), MR - R < MC - C, {size_range}.\n"
    size_spawn += f"rect_edge(R1, C1, -1) :- grid(R1, C1), rect(R, C, MR, MC), MR - R > MC - C, {size_range}."

    unique = f":- rect(R, C, MR, MC), #count {{ R1, C1: clue(R1, C1), {size_range} }} != 1."
    no_rect_adjacent_by_point = [
        "vertical_line(R, C + 1)",
        "vertical_line(R + 1, C + 1)",
        "horizontal_line(R + 1, C)",
        "horizontal_line(R + 1, C + 1)",
    ]
    no_rect = f":- grid(R, C), {', '.join(no_rect_adjacent_by_point)}."

    return size_spawn + "\n" + unique + "\n" + no_rect


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    if len(E.clues) == 0:
        raise ValueError("Please provide at least one clue.")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(all_rect_region())
    solver.add_program_line(tatamibari_constraint())

    for (r, c), clue in E.clues.items():
        solver.add_program_line(f"clue({r}, {c}).")
        if clue == "+":
            solver.add_program_line(f":- not rect_edge({r}, {c}, 0).")
        elif clue == "-":
            solver.add_program_line(f":- not rect_edge({r}, {c}, 1).")
        elif clue == "|":
            solver.add_program_line(f":- not rect_edge({r}, {c}, -1).")

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
