"""The Hitori solver."""

from typing import Dict, List

from .core.common import display, grid, shade_c, unique_num
from .core.encoding import Encoding
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.reachable import grid_color_connected
from .core.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(unique_num(color="not black", _type="row"))
    solver.add_program_line(unique_num(color="not black", _type="col"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color())
    solver.add_program_line(grid_color_connected(color="not black", initial_cells=[(0, 0), (0, 1)]))

    for (r, c), clue in E.clues.items():
        if isinstance(clue, list):
            if clue[1] == "black":
                solver.add_program_line(f"black({r}, {c}).")
            elif clue[1] == "green":
                num = int(clue[0])
                solver.add_program_line(f"not black({r}, {c}).")
                solver.add_program_line(f"number({r}, {c}, {num}).")
        else:
            num = int(clue)
            solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions
