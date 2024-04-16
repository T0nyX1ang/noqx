"""The N Cells solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Direction, Encoding, tag_encode
from .utilsx.fact import display, edge, grid
from .utilsx.reachable import grid_branch_color_connected
from .utilsx.rule import adjacent, count_adjacent_edges
from .utilsx.solution import solver


def count_reachable_edge(target: int) -> str:
    """
    Generates a constraint for counting grids in a region divided by edges.

    An edge rule and a grid_branch_color_connected rule should be defined first.
    """
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")

    return f":- grid(R0, C0), #count {{ R, C: {tag}(R0, C0, R, C) }} != {target}."


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    size = int(E.params["region_size"])
    assert E.R * E.C % size == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(grid_branch_color_connected(color=None, adj_type="edge"))
    solver.add_program_line(count_reachable_edge(size))

    for r, c, d in E.edges:
        if d == Direction.LEFT:
            solver.add_program_line(f"vertical_line({r}, {c}).")
        elif d == Direction.TOP:
            solver.add_program_line(f"horizontal_line({r}, {c}).")

    for (r, c), clue in E.clues.items():
        solver.add_program_line(count_adjacent_edges(int(clue), (r, c)))

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
