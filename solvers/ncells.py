"""The N Cell solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import (
    adjacent,
    rev_op_dict,
)
from .utilsx.helper import tag_encode
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def edge(rows: int, cols: int, border_shade: bool = True) -> str:
    """
    Generates facts for grid edges.
    Note grid borders are also included.
    """
    fact = f"vertical_range(0..{rows - 1}, 0..{cols}).\n"
    fact += f"horizontal_range(0..{rows}, 0..{cols - 1}).\n"
    fact += "{ vertical_line(R, C) } :- vertical_range(R, C).\n"
    fact += "{ horizontal_line(R, C) } :- horizontal_range(R, C).\n"
    if border_shade:
        fact += "vertical_line(R, C):- vertical_range(R, C), C = 0.\n"
        fact += f"vertical_line(R, C):- vertical_range(R, C), C = {cols}.\n"
        fact += "horizontal_line(R, C):- horizontal_range(R, C), R = 0.\n"
        fact += f"horizontal_line(R, C):- horizontal_range(R, C), R = {rows}.\n"
    return fact[:-1]


def reachable_edge() -> str:
    """
    Define edges as numbers on its adjacent grids are different.
    A grid fact should be defined first.
    """
    adj_edge = "adj_edge(R0, C0, R, C) :- R=R0, C=C0+1, grid(R, C), grid(R0, C0), not vertical_line(R, C).\n"
    adj_edge += "adj_edge(R0, C0, R, C) :- R=R0+1, C=C0, grid(R, C), grid(R0, C0), not horizontal_line(R, C).\n"
    adj_edge += "adj_edge(R0, C0, R, C) :- adj_edge(R, C, R0, C0).\n"

    reachable_edge = "reachable_edge(R0, C0, R, C) :- grid(R, C), grid(R0, C0), R = R0, C = C0.\n"
    reachable_edge += (
        "reachable_edge(R0, C0, R, C) :- grid(R, C), reachable_edge(R0, C0, R1, C1), adj_edge(R1, C1, R, C).\n"
    )
    # edge between two reachable grids is forbidden.
    constraint = ":- reachable_edge(R0, C0, R, C), R=R0, C=C0+1, vertical_line(R, C).\n"
    constraint += ":- reachable_edge(R0, C0, R, C), R=R0+1, C=C0, horizontal_line(R, C)."
    return adj_edge + reachable_edge + constraint


def count_reachable_edge(target: int, op: str = "eq") -> str:
    """
    Generates a constraint for counting grids in a region divided by edges.
    A grid fact should be defined first.
    """
    op = rev_op_dict[op]
    return f":- grid(R0, C0), #count {{ R, C: reachable_edge(R0, C0, R, C) }} {op} {target}."


def count_adj_lines(r: int, c: int, number: int) -> str:
    return f":- #count{{ R, C, 0: vertical_line(R, C), R={r}, C>={c}, C<={c+1}; R, C, 1: horizontal_line(R, C), R>={r}, R<={r+1}, C={c} }} != {number}."


def solve(E: Encoding) -> List:
    size = int(E.params["region_size"])
    assert E.R * E.C % size == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset(mode="region", R=E.R, C=E.C)
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    # solver.add_program_line(adjacent())
    solver.add_program_line(reachable_edge())
    solver.add_program_line(count_reachable_edge(size))

    for (r, c), clue in E.clues.items():
        solver.add_program_line(count_adj_lines(r, c, clue))

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
