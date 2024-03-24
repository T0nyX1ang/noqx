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

    rule = "reachable_row(R, C1, C2) :- grid(R, C1), C1 = C2.\n"
    rule += "reachable_row(R, C1, C2) :- grid(R, C1), grid(R, C2), C1 < C2, adj_edge(R, C2-1, R, C2), reachable_row(R, C1, C2-1).\n"
    rule += "reachable_row(R, C1, C2) :- grid(R, C1), grid(R, C2), C1 > C2, reachable_row(R, C2, C1).\n"
    rule += "reachable_col(R1, R2, C) :- grid(R1, C), R1 = R2.\n"
    rule += "reachable_col(R1, R2, C) :- grid(R1, C), grid(R2, C), R1 < R2, adj_edge(R2, C, R2-1, C), reachable_col(R1, R2-1, C).\n"
    rule += "reachable_col(R1, R2, C) :- grid(R1, C), grid(R2, C), R1 > R2, reachable_col(R2, R1, C).\n"

    size_range = "R = #min{ R0: grid(R0, C1), reachable_col(R0, R1, C1) }, MR = #max{ R0: grid(R0, C1), reachable_col(R0, R1, C1) }, C = #min{ C0: grid(R1, C0), reachable_row(R1, C0, C1) }, MC = #max{ C0: grid(R1, C0), reachable_row(R1, C0, C1) }"
    rule += f"rect_size(R1, C1, S) :- grid(R1, C1), clue(R1, C1), S = (MR - R + 1) * (MC - C + 1), {size_range}.\n"
    rule += ":- clue(R0, C0), clue(R1, C1), (R0, C0) != (R1, C1), reachable_row(R0, C0, C1), reachable_col(R0, R1, C1)."

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
