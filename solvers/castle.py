"""The Castle castle solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import connected_loop, fill_path, single_loop
from .utilsx.rule import adjacent, shade_c
from .utilsx.solution import solver


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


def black_out_white_in() -> str:
    """
    Generate a constraint to make black cells outside of the loop, and make white cells inside of loop.

    A grid direction fact should be defined first.
    """
    out_loop = "out_loop(-1, C) :- grid(_, C).\n"
    out_loop += 'out_loop(R, C) :- grid(R, C), out_loop(R - 1, C), not grid_direction(R, C, "r").\n'
    out_loop += 'out_loop(R, C) :- grid(R, C), not out_loop(R - 1, C), grid_direction(R, C, "r").\n'
    constraint = ":- white(R, C), out_loop(R, C).\n"
    constraint += ":- black(R, C), not out_loop(R, C)."
    return out_loop + constraint


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="castle"))
    solver.add_program_line(fill_path(color="castle"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(connected_loop(color="castle"))
    solver.add_program_line(single_loop(color="castle"))
    solver.add_program_line(black_out_white_in())

    for (r, c), clue in E.clues.items():
        num, d, color = clue
        if d in ["u", "l", "d", "r"]:
            solver.add_program_line(wall_length(r, c, d, int(num)))
        if color in "wgb":
            color_dict = {"w": "white", "g": "gray", "b": "black"}
            color = color_dict[color]
            solver.add_program_line(f"{color}({r}, {c}).")
            solver.add_program_line(f"not castle({r}, {c}).")

    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
