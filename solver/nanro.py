"""The Nanro solver."""

from typing import Dict, List

from . import core
from .core.common import area, count, display, fill_num, grid
from .core.encoding import Encoding
from .core.helper import full_bfs
from .core.neighbor import adjacent, area_adjacent
from .core.reachable import grid_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def nanro_fill_constraint(color: str = "black") -> str:
    """Generate a constraint for the number filling in nanro."""
    return f":- number(R0, C0, N), area(A, R0, C0), #count {{ R, C : area(A, R, C), {color}(R, C) }} != N."


def nanro_avoid_adjacent() -> str:
    """Generate a rule to avoid adjacent cells with the same number."""
    area_adj = area_adjacent()
    area_adj = area_adj[area_adj.find(":-") : -1]
    return f"{area_adj}, number(R, C, N), number(R1, C1, N)."


def encode(string: str) -> Encoding:
    E = core.encode(string)

    # separate signpost clues from regular clues
    new_clues = {}
    E.signpost_clues = {}
    for key in E.clues:
        s = E.clues[key]
        if isinstance(s, str) and s[0] == "s" and s[1:].isnumeric():  # signpost clue
            E.signpost_clues[key] = int(s[1:])
        else:
            new_clues[key] = s
    E.clues = new_clues
    return E


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not gray"))
    solver.add_program_line(avoid_rect(2, 2, color="not gray"))

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i, color="gray"))

        flag = True
        for cell in ar:
            if cell in E.signpost_clues:  # signpost variant
                solver.add_program_line(count(E.signpost_clues[cell], color="not gray", _type="area", _id=i))
                flag = False
        if flag:
            solver.add_program_line(count(("gt", 0), color="not gray", _type="area", _id=i))

    for (r, c), clue in E.clues.items():
        if clue == "gray":
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            num = int(clue)
            solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(nanro_fill_constraint(color="not gray"))
    solver.add_program_line(nanro_avoid_adjacent())
    solver.add_program_line(display(item="gray", size=2))
    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions
