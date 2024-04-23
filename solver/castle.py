"""The Castle castle solver."""

from typing import Dict, List

from .core.common import direction, display, fill_path, grid, shade_c
from .core.encoding import Encoding
from .core.loop import separate_item_from_loop, single_loop
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.solution import solver


def wall_length(r: int, c: int, d: str, num: int) -> str:
    """
    Constrain the castle length.

    A grid direction fact should be defined first.
    """
    if d == "l":
        return f':- #count{{ C: grid_direction({r}, C, "r"), C < {c} }} != {num}.'
    if d == "u":
        return f':- #count{{ R: grid_direction(R, {c}, "d"), R < {r} }} != {num}.'
    if d == "r":
        return f':- #count{{ C: grid_direction({r}, C, "r"), C > {c} }} != {num}.'
    if d == "d":
        return f':- #count{{ R: grid_direction(R, {c}, "d"), R > {r} }} != {num}.'

    raise ValueError("Invalid direction.")


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="castle"))
    solver.add_program_line(fill_path(color="castle"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="castle", adj_type="loop"))
    solver.add_program_line(single_loop(color="castle"))
    solver.add_program_line(separate_item_from_loop(inside_item="white", outside_item="black"))

    for (r, c), clue in E.clues.items():
        num, d, color = clue
        if d in ["u", "l", "d", "r"]:
            solver.add_program_line(wall_length(r, c, d, int(num)))
        if color in "wgb":
            color_dict = {"w": "white", "g": "gray", "b": "black"}
            color = color_dict[color]
            solver.add_program_line(f"{color}({r}, {c}).")
            solver.add_program_line(f"not castle({r}, {c}).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
