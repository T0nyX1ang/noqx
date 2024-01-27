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

    not_color = "not_color(R, C) :- grid(R+1, C), not grid(R, C).\n"
    not_color += "not_color(R, C) :- grid(R, C+1), not grid(R, C).\n"
    not_color += f"not_color(R, C) :- grid(R, C), not {color}(R, C)."

    upleft = f"upleft(R, C) :- grid(R, C), {color}(R, C), not_color(R - 1, C), not_color(R, C - 1)."
    left = f"left(R, C) :- grid(R, C), {color}(R, C), upleft(R - 1, C), {color}(R - 1, C), not_color(R, C - 1).\n"
    left += f"left(R, C) :- grid(R, C), {color}(R, C), left(R - 1, C), {color}(R - 1, C), not_color(R, C - 1)."
    up = f"up(R, C) :- grid(R, C), {color}(R, C), upleft(R, C - 1), {color}(R, C - 1), not_color(R - 1, C).\n"
    up += f"up(R, C) :- grid(R, C), {color}(R, C), up(R, C - 1), {color}(R, C - 1), not_color(R - 1, C).\n"
    remain = "remain(R, C) :- grid(R, C), left(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), left(R, C - 1), remain(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), remain(R - 1, C)."

    constraint = f":- grid(R, C), {color}(R, C), not upleft(R, C), not left(R, C), not up(R, C), not remain(R, C)."
    constraint += f":- grid(R, C), remain(R, C), not {color}(R, C)."
    return not_color + "\n" + upleft + "\n" + left + "\n" + up + "\n" + remain + "\n" + constraint


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

    for (r, c), clue in E.clues.items():
        if clue == "darkgray":
            solver.add_program_line(f"darkgray({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not darkgray({r}, {c}).")

    solver.add_program_line(display(color="darkgray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
