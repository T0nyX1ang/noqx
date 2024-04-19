"""The Yin-Yang solver."""

from typing import Dict, List

from .core.common import display, grid, shade_c
from .core.encoding import Encoding, rcd_to_elt
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black"))
    solver.add_program_line(avoid_rect(rect_r=2, rect_c=2, color="black"))
    solver.add_program_line(grid_color_connected(color="not black"))
    solver.add_program_line(avoid_rect(rect_r=2, rect_c=2, color="not black"))

    for (r, c), color in E.clues.items():
        color = "black" if color == "b" else "not black"
        solver.add_program_line(f"{color}({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    for solution in solver.solutions:
        for r in range(E.R):
            for c in range(E.C):
                rc = rcd_to_elt(r, c)
                solution[rc] = "white_circle.png" if rc not in solution else "black_circle.png"

    return solver.solutions
