"""The Balance Loop solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import single_loop, connected_loop
from .utilsx.rule import adjacent, fill_path, shade_c
from .utilsx.solution import solver


def balance_loop_rule(color: str = "black") -> str:
    """
    Generate a rule for balance loop.

    A loop_sign rule should be defined first.
    """
    op = "=" if color == "black" else "!="

    # must be some methods to simplify these codes
    rule = f'balance_{color}(R, C, R1, C1) :- {color}(R, C), loop_sign(R, C, "J"), R1 = #max {{ R0: grid(R0, C), not loop_sign(R0, C, "1"), R0 < R }}, C1 = #max {{ C0: grid(R, C0), not loop_sign(R, C0, "-"), C0 < C }}.\n'
    rule += f'balance_{color}(R, C, R1, C1) :- {color}(R, C), loop_sign(R, C, "7"), R1 = #min {{ R0: grid(R0, C), not loop_sign(R0, C, "1"), R0 > R }}, C1 = #max {{ C0: grid(R, C0), not loop_sign(R, C0, "-"), C0 < C }}.\n'
    rule += f'balance_{color}(R, C, R1, C1) :- {color}(R, C), loop_sign(R, C, "L"), R1 = #max {{ R0: grid(R0, C), not loop_sign(R0, C, "1"), R0 < R }}, C1 = #min {{ C0: grid(R, C0), not loop_sign(R, C0, "-"), C0 > C }}.\n'
    rule += f'balance_{color}(R, C, R1, C1) :- {color}(R, C), loop_sign(R, C, "r"), R1 = #min {{ R0: grid(R0, C), not loop_sign(R0, C, "1"), R0 > R }}, C1 = #min {{ C0: grid(R, C0), not loop_sign(R, C0, "-"), C0 > C }}.\n'
    rule += f'balance_{color}(R, C, R1, C1) :- {color}(R, C), loop_sign(R, C, "1"), R1 = #max {{ R0: grid(R0, C), not loop_sign(R0, C, "1"), R0 < R }}, C1 = #min {{ R0: grid(R0, C), not loop_sign(R0, C, "1"), R0 > R }}.\n'
    rule += f'balance_{color}(R, C, R1, C1) :- {color}(R, C), loop_sign(R, C, "-"), R1 = #max {{ C0: grid(R, C0), not loop_sign(R, C0, "-"), C0 < C }}, C1 = #min {{ C0: grid(R, C0), not loop_sign(R, C0, "-"), C0 > C }}.\n'
    rule += f':- balance_{color}(R, C, R1, C1), loop_sign(R, C, "J"), |R - R1| {op} |C - C1|.\n'
    rule += f':- balance_{color}(R, C, R1, C1), loop_sign(R, C, "7"), |R - R1| {op} |C - C1|.\n'
    rule += f':- balance_{color}(R, C, R1, C1), loop_sign(R, C, "L"), |R - R1| {op} |C - C1|.\n'
    rule += f':- balance_{color}(R, C, R1, C1), loop_sign(R, C, "r"), |R - R1| {op} |C - C1|.\n'
    rule += f':- balance_{color}(R, C, R1, C1), loop_sign(R, C, "1"), |R - R1| {op} |R - C1|.\n'
    rule += f':- balance_{color}(R, C, R1, C1), loop_sign(R, C, "-"), |C - R1| {op} |C - C1|.\n'
    rule += f':- balance_{color}(R, C, R1, C1), number(R, C, N), loop_sign(R, C, "J"), |R - R1| + |C - C1| != N.\n'
    rule += f':- balance_{color}(R, C, R1, C1), number(R, C, N), loop_sign(R, C, "7"), |R - R1| + |C - C1| != N.\n'
    rule += f':- balance_{color}(R, C, R1, C1), number(R, C, N), loop_sign(R, C, "L"), |R - R1| + |C - C1| != N.\n'
    rule += f':- balance_{color}(R, C, R1, C1), number(R, C, N), loop_sign(R, C, "r"), |R - R1| + |C - C1| != N.\n'
    rule += f':- balance_{color}(R, C, R1, C1), number(R, C, N), loop_sign(R, C, "1"), |R - R1| + |R - C1| != N.\n'
    rule += f':- balance_{color}(R, C, R1, C1), number(R, C, N), loop_sign(R, C, "-"), |C - R1| + |C - C1| != N.\n'
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
    solver.add_program_line(balance_loop_rule(color="black"))
    solver.add_program_line(balance_loop_rule(color="white"))

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
