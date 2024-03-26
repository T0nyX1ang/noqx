"""The Shikaku solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, edge, grid
from .utilsx.helper import tag_encode
from .utilsx.rule import adjacent, reachable_row, reachable_col
from .utilsx.shape import all_rect_region
from .utilsx.solution import solver


def shikaku_constraint() -> str:
    """Generate a constraint for shikaku."""
    tag_col = tag_encode("reachable", "row", "edge")
    tag_row = tag_encode("reachable", "col", "edge")

    size_range = [
        f"R = #min{{ R0: grid(R0, C1), {tag_row}(R0, R1, C1) }}",
        f"MR = #max{{ R0: grid(R0, C1), {tag_row}(R0, R1, C1) }}",
        f"C = #min{{ C0: grid(R1, C0), {tag_col}(R1, C0, C1) }}",
        f"MC = #max{{ C0: grid(R1, C0), {tag_col}(R1, C0, C1) }}",
    ]

    rule = f"rect_size(R1, C1, S) :- grid(R1, C1), clue(R1, C1), S = (MR - R + 1) * (MC - C + 1), {', '.join(size_range)}.\n"
    rule += f":- clue(R0, C0), clue(R1, C1), (R0, C0) != (R1, C1), {tag_row}(R0, R1, C1), {tag_col}(R0, C0, C1)."
    return rule


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
    solver.add_program_line(reachable_row(adj_type="edge"))
    solver.add_program_line(reachable_col(adj_type="edge"))
    solver.add_program_line(shikaku_constraint())

    for (r, c), clue in E.clues.items():
        solver.add_program_line(f"clue({r}, {c}).")
        if clue != "?":
            num = int(clue)
            solver.add_program_line(f":- not rect_size({r}, {c}, {num}).")

    solver.add_program_line(f":- {{ upleft(R, C) }} != {len(E.clues)}.")
    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
