"""The N Cell solver."""

from typing import List

from . import utilsx
from .utilsx.border import Direction
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import rev_op_dict, adjacent
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def edge(rows: int, cols: int) -> str:
    """
    Generates facts for grid edges.
    Note grid borders are also included.
    """
    fact = f"vertical_range(0..{rows - 1}, 0..{cols}).\n"
    fact += f"horizontal_range(0..{rows}, 0..{cols - 1}).\n"
    fact += "{ vertical_line(R, C) } :- vertical_range(R, C).\n"
    fact += "{ horizontal_line(R, C) } :- horizontal_range(R, C)."
    return fact


def reachable_edge() -> str:
    """
    Define edges as numbers on its adjacent grids are different.
    A grid fact should be defined first.
    """
    initial = "reachable_edge(R0, C0, R, C) :- grid(R, C), grid(R0, C0), R = R0, C = C0.\n"
    propagation = (
        "reachable_edge(R0, C0, R, C) :- grid(R, C), reachable_edge(R0, C0, R1, C1), adj_edge(R1, C1, R, C).\n"
    )
    # edge between two reachable grids is forbidden.
    constraint = ":- reachable_edge(R0, C0, R, C), R=R0, C=C0+1, vertical_line(R, C).\n"
    constraint += ":- reachable_edge(R0, C0, R, C), R=R0+1, C=C0, horizontal_line(R, C)."
    return initial + propagation + constraint


def count_reachable_edge(target: int, op: str = "eq") -> str:
    """
    Generates a constraint for counting grids in a region divided by edges.
    A grid fact should be defined first.
    """
    op = rev_op_dict[op]
    return f":- grid(R0, C0), #count {{ R, C: reachable_edge(R0, C0, R, C) }} {op} {target}."


def count_adj_lines(r: int, c: int, number: int) -> str:
    return f":- #count{{ 1: vertical_line({r},{c}); 2: vertical_line({r},{c+1}); 3: horizontal_line({r},{c}); 4: horizontal_line({r+1},{c}) }} != {number}."


def solve(E: Encoding) -> List:
    size = int(E.params["region_size"])
    assert E.R * E.C % size == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent("edge"))
    solver.add_program_line(reachable_edge())
    solver.add_program_line(count_reachable_edge(size))

    for r, c, d in E.edge_ids:
        if d in [Direction.LEFT, Direction.RIGHT]:
            c += d == Direction.RIGHT
            solver.add_program_line(f"vertical_line({r}, {c}).")
        elif d in [Direction.TOP, Direction.BOTTOM]:
            r += d == Direction.BOTTOM
            solver.add_program_line(f"horizontal_line({r}, {c}).")

    for (r, c), clue in E.clues.items():
        solver.add_program_line(count_adj_lines(r, c, clue))

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
