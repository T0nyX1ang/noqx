"""The Castle Wall solver."""

from typing import List, Tuple

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import single_loop, connected_loop, fill_path
from .utilsx.rule import adjacent
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def wall_length(r: int, c: int, direc: str, num: int) -> str:
    if direc == "l":
        return f':- #count{{ C: grid_direction({r}, C, "r"), C < {c} }} != {num}.'
    elif direc == "u":
        return f':- #count{{ R: grid_direction(R, {c}, "d"), R < {r} }} != {num}.'
    elif direc == "r":
        return f':- #count{{ C: grid_direction({r}, C, "r"), C > {c} }} != {num}.'
    elif direc == "d":
        return f':- #count{{ R: grid_direction(R, {c}, "d"), R > {r} }} != {num}.'


def black_out_white_in() -> str:
    in_loop = "binary(0..1).\n"
    in_loop += "in_loop(R, C, 0) :- R = -1, grid(_, C).\n"
    in_loop += 'in_loop(R, C, N) :- grid(R, C), binary(N), in_loop(R-1, C, N), not grid_direction(R, C, "r").\n'
    in_loop += 'in_loop(R, C, N) :- grid(R, C), binary(N), in_loop(R-1, C, 1-N), grid_direction(R, C, "r").\n'
    constraint = ":- white(R, C), in_loop(R, C, 0).\n"
    constraint = ":- black(R, C), in_loop(R, C, 1)."
    return in_loop + constraint


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ wall(R, C) } :- grid(R, C), not black(R, C), not white(R, C), not gray(R, C).")
    solver.add_program_line(fill_path(color="wall"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(connected_loop(color="wall"))
    solver.add_program_line(single_loop(color="wall", visit_all=True))
    solver.add_program_line(black_out_white_in())

    for (r, c), clue in E.clues.items():
        num, direc, color = clue
        if direc in ["u", "l", "d", "r"]:
            solver.add_program_line(wall_length(r, c, direc, int(num)))
        if color in "wgb":
            color_dict = {"w": "white", "g": "gray", "b": "black"}
            color = color_dict[color]
            solver.add_program_line(f"{color}({r}, {c}).")

    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
