"""The Balance Loop solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import single_loop, connected_loop, fill_path
from .utilsx.rule import adjacent, shade_c
from .utilsx.solution import solver


def balance_loop_rule(r: int, c: int, color: str = "black") -> str:
    """
    Generate a rule for balance loop.

    A loop_sign rule should be defined first.
    """
    op = "=" if color == "black" else "!="

    # detect the longest straight line
    max_u = '#max { R0: grid(R0 + 1, C), not loop_sign(R0, C, "1"), R0 < R }'
    min_d = '#min { R0: grid(R0 - 1, C), not loop_sign(R0, C, "1"), R0 > R }'
    max_l = '#max { C0: grid(R, C0 + 1), not loop_sign(R, C0, "-"), C0 < C }'
    min_r = '#min { C0: grid(R, C0 - 1), not loop_sign(R, C0, "-"), C0 > C }'

    rule = f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "J"), N1 = {max_u}, N2 = {max_l}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "7"), N1 = {min_d}, N2 = {max_l}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "L"), N1 = {max_u}, N2 = {min_r}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "r"), N1 = {min_d}, N2 = {min_r}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "1"), N1 = {max_u}, N2 = {min_d}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "-"), N1 = {max_l}, N2 = {min_r}.\n'

    for sign in "J7Lr":
        rule += f':- balance_{color}(R, C, N1, N2), loop_sign(R, C, "{sign}"), |R - N1| {op} |C - N2|.\n'
        rule += f':- balance_{color}(R, C, N1, N2), number(R, C, N), loop_sign(R, C, "{sign}"), |R - N1| + |C - N2| != N.\n'

    # special case for straight line
    rule += f':- balance_{color}(R, C, N1, N2), loop_sign(R, C, "1"), |R - N1| {op} |R - N2|.\n'
    rule += f':- balance_{color}(R, C, N1, N2), loop_sign(R, C, "-"), |C - N1| {op} |C - N2|.\n'
    rule += f':- balance_{color}(R, C, N1, N2), number(R, C, N), loop_sign(R, C, "1"), |R - N1| + |R - N2| != N.\n'
    rule += f':- balance_{color}(R, C, N1, N2), number(R, C, N), loop_sign(R, C, "-"), |C - N1| + |C - N2| != N.\n'
    return rule


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="balance_loop"))
    solver.add_program_line(fill_path(color="balance_loop"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(connected_loop(color="balance_loop"))
    solver.add_program_line(single_loop(color="balance_loop", visit_all=True))
    solver.add_program_line(balance_loop_rule(E.R, E.C, color="black"))
    solver.add_program_line(balance_loop_rule(E.R, E.C, color="white"))

    for (r, c), (clue, color) in E.clues.items():
        solver.add_program_line(f"balance_loop({r}, {c}).")
        if color == "b":
            solver.add_program_line(f"black({r}, {c}).")
            if clue != "":
                num = int(clue)
                solver.add_program_line(f"number({r}, {c}, {num}).")
        elif color == "w":
            solver.add_program_line(f"white({r}, {c}).")
            if clue != "":
                num = int(clue)
                solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
