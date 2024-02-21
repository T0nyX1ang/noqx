"""The N Cell solver."""

from typing import List

from . import utilsx
from .utilsx.border import Direction
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid, edge
from .utilsx.rule import adjacent, reachable_edge, count_reachable_edge
from .utilsx.solution import solver


def count_adj_lines(r: int, c: int, number: int) -> str:
    """Return a rule that counts the adjacent lines around a cell."""
    v_1 = f"vertical_line({r},{c})"
    v_2 = f"vertical_line({r},{c+1})"
    h_1 = f"horizontal_line({r},{c})"
    h_2 = f"horizontal_line({r+1},{c})"
    return f":- #count{{ 1: {v_1}; 2: {v_2}; 3: {h_1}; 4: {h_2} }} != {number}."


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    size = int(E.params["region_size"])
    assert E.R * E.C % size == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(_type="edge"))
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
