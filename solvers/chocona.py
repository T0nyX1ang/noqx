"""The Chocona solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.regions import full_bfs
from .utilsx.rules import (
    adjacent,
    area,
    count,
    display,
    grid,
    shade_c,
)
from .utilsx.solutions import solver


def all_rectangles(color: str = "black") -> str:
    """
    Generate a constraint to force rectangles.

    An adjacent rule should be defined first.
    """

    not_start = f"not_start(R, C) :- grid(R, C), not {color}(R, C).\n"
    not_start += f"not_start(R, C) :- grid(R, C), grid(R-1,C), {color}(R-1, C).\n"
    not_start += f"not_start(R, C) :- grid(R, C), grid(R,C-1), {color}(R, C-1)."

    connected = f"reachable(R0, C0, R, C) :- grid(R0, C0), darkgray(R0, C0), R = R0, C = C0.\n"
    connected += f"reachable(R0, C0, R, C) :- reachable(R0, C0, R1, C1), adj_4(R, C, R1, C1), grid(R, C), {color}(R, C)."

    min_reachable = "min_reachable(R, C, MR, MC) :- grid(R, C), #min { R1 : reachable(R, C, R1, _) } = MR, #min { C1 : reachable(R, C, _, C1) } = MC.\n"
    max_reachable = "max_reachable(R, C, MR, MC) :- grid(R, C), #max { R1 : reachable(R, C, R1, _) } = MR, #max { C1 : reachable(R, C, _, C1) } = MC.\n"
    rectangle = "rectangle(R, C) :- grid(R, C), max_reachable(R, C, MR, MC), #count { R1, C1 : grid(R1, C1), reachable(R, C, R1, C1)} = (MR - R + 1) * (MC - C + 1)."

    constraint = ":- grid(R, C), not not_start(R, C), not min_reachable(R, C, R, C).\n"
    constraint += ":- grid(R, C), not not_start(R, C), not rectangle(R, C)."
    return not_start + "\n" + connected + "\n" + min_reachable + "\n" + max_reachable + "\n" + rectangle + "\n" + constraint


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c("darkgray"))
    solver.add_program_line(adjacent())

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        num = -1
        for cell in ar:
            if cell in E.clues:
                num = E.clues[cell]
        solver.add_program_line(area(_id=i, src_cells=ar))
        if num >= 0:
            solver.add_program_line(count(num, color="darkgray", _type="area", _id=i))
    solver.add_program_line(all_rectangles(color="darkgray"))

    # 桶后面统一把初值加了吧
    # for (r, c), clue in E.clues.items():
    #     if clue == "darkgray":
    #         solver.add_program_line(f"darkgray({r}, {c}).")
    #     elif clue == "green":
    #         solver.add_program_line(f"not darkgray({r}, {c}).")

    solver.add_program_line(display(color="darkgray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
