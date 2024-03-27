"""The N Cells solver."""

from typing import List

from . import utilsx
from .utilsx.coord import Direction
from .utilsx.encoding import Encoding
from .utilsx.fact import display, edge, grid
from .utilsx.rule import adjacent, count_adjacent_lines, count_reachable_edge, reachable_edge
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    size = int(E.params["region_size"])
    assert E.R * E.C % size == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(reachable_edge())
    solver.add_program_line(count_reachable_edge(size))

    for r, c, d in E.edges:
        if d == Direction.LEFT:
            solver.add_program_line(f"vertical_line({r}, {c}).")
        elif d == Direction.TOP:
            solver.add_program_line(f"horizontal_line({r}, {c}).")

    for (r, c), clue in E.clues.items():
        solver.add_program_line(count_adjacent_lines(int(clue), (r, c)))

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
