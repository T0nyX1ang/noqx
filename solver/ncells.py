"""The N Cells solver."""

from typing import Dict, List

from .core.common import display, edge, grid
from .core.helper import extract_initial_edges
from .core.encoding import Encoding, tag_encode
from .core.neighbor import adjacent, count_adjacent_edges
from .core.reachable import grid_branch_color_connected
from .core.solution import solver


def count_reachable_edge(target: int) -> str:
    """
    Generates a constraint for counting grids in a region divided by edges.

    An edge rule and a grid_branch_color_connected rule should be defined first.
    """
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")

    return f":- grid(R0, C0), #count {{ R, C: {tag}(R0, C0, R, C) }} != {target}."


def solve(E: Encoding) -> List[Dict[str, str]]:
    size = int(E.params["region_size"])
    assert E.R * E.C % size == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(grid_branch_color_connected(color=None, adj_type="edge"))
    solver.add_program_line(count_reachable_edge(size))
    solver.add_program_line(extract_initial_edges(E.edges))

    for (r, c), clue in E.clues.items():
        solver.add_program_line(count_adjacent_edges(int(clue), (r, c)))

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions
