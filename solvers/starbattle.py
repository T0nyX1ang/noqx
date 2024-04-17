"""The Star Battle solver."""

from typing import Dict, List

from .utilsx.common import area, count, display, grid, shade_c
from .utilsx.encoding import Encoding
from .utilsx.helper import full_bfs
from .utilsx.neighbor import adjacent, avoid_adjacent_color
from .utilsx.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    num_stars = int(E.params["stars"])

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="gray"))

    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_adjacent_color(color="gray", adj_type=8))

    solver.add_program_line(count(num_stars, color="gray", _type="row"))
    solver.add_program_line(count(num_stars, color="gray", _type="col"))

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count(num_stars, color="gray", _type="area", _id=i))

    for (r, c), clue in E.clues.items():
        if clue == "gray":
            solver.add_program_line(f"gray({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
