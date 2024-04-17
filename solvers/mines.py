"""The blacksweeper solver."""

from typing import Dict, List

from .utilsx.common import count, display, grid, shade_c
from .utilsx.encoding import Encoding
from .utilsx.neighbor import adjacent, count_adjacent
from .utilsx.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    mine_count = E.params["m"]

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent(_type=8))

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        else:
            num = int(clue)
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(count_adjacent(num, (r, c), color="black", adj_type=8))

    if mine_count:
        solver.add_program_line(count(mine_count, color="black", _type="grid"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions
