"""The Castle Wall solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import single_loop, connected_loop, fill_path
from .utilsx.rule import adjacent
from .utilsx.solution import solver


def wall_length(r: int, c: int, d: str, num: int) -> str:
    """
    Constrain the wall length.

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
    in_loop = "in_loop(-1, C) :- grid(_, C).\n"
    in_loop += 'in_loop(R, C) :- grid(R, C), in_loop(R - 1, C), not grid_direction(R, C, "r").\n'
    in_loop += 'in_loop(R, C) :- grid(R, C), not in_loop(R - 1, C), grid_direction(R, C, "r").\n'
    constraint = ":- white(R, C), in_loop(R, C).\n"
    constraint = ":- black(R, C), not in_loop(R, C)."
    return in_loop + constraint


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ wall(R, C) } :- grid(R, C), not clue(R, C).")
    solver.add_program_line(fill_path(color="wall"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(connected_loop(color="wall"))
    solver.add_program_line(single_loop(color="wall", visit_all=True))
    solver.add_program_line(black_out_white_in())

    for (r, c), clue in E.clues.items():
        num, d, color = clue
        if d in ["u", "l", "d", "r"]:
            solver.add_program_line(wall_length(r, c, d, int(num)))
        if color in "wgb":
            color_dict = {"w": "white", "g": "gray", "b": "black"}
            color = color_dict[color]
            solver.add_program_line(f"{color}({r}, {c}).")
            solver.add_program_line(f"clue({r}, {c}).")

    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
