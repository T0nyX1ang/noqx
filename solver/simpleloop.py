"""The Simple Loop solver."""

from typing import Dict, List

from .core.common import direction, display, fill_path, grid
from .core.encoding import Encoding
from .core.loop import single_loop
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("simpleloop(R, C) :- grid(R, C), not black(R, C).")
    solver.add_program_line(fill_path(color="simpleloop"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="simpleloop", adj_type="loop"))
    solver.add_program_line(single_loop(color="simpleloop"))

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
