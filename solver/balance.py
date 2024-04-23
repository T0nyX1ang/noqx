"""The Balance Loop solver."""

from typing import Dict, List, Tuple

from .core.common import direction, display, fill_path, grid, shade_c
from .core.encoding import Encoding, reverse_op
from .core.loop import single_loop, loop_sign
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.solution import solver

def balance_rule(color: str = "black") -> str:
    """
    Generate a rule for balance loop.

    A loop_sign rule should be defined first.
    """
    op = "=" if color == "black" else "!="

    # detect the longest straight line
    max_u = '#max { R0: grid(R0 + 1, C), not loop_sign(R0, C, "ud"), R0 < R }'
    min_d = '#min { R0: grid(R0 - 1, C), not loop_sign(R0, C, "ud"), R0 > R }'
    max_l = '#max { C0: grid(R, C0 + 1), not loop_sign(R, C0, "lr"), C0 < C }'
    min_r = '#min { C0: grid(R, C0 - 1), not loop_sign(R, C0, "lr"), C0 > C }'

    rule = f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "lu"), N1 = {max_u}, N2 = {max_l}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "ld"), N1 = {min_d}, N2 = {max_l}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "ru"), N1 = {max_u}, N2 = {min_r}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "rd"), N1 = {min_d}, N2 = {min_r}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "ud"), N1 = {max_u}, N2 = {min_d}.\n'
    rule += f'balance_{color}(R, C, N1, N2) :- {color}(R, C), loop_sign(R, C, "lr"), N1 = {max_l}, N2 = {min_r}.\n'

    for sign in ["lu", "ld", "ru", "rd"]:
        rule += f':- balance_{color}(R, C, N1, N2), loop_sign(R, C, "{sign}"), |R - N1| {op} |C - N2|.\n'

    # special case for straight line
    rule += f':- balance_{color}(R, C, N1, N2), loop_sign(R, C, "ud"), |R - N1| {op} |R - N2|.\n'
    rule += f':- balance_{color}(R, C, N1, N2), loop_sign(R, C, "lr"), |C - N1| {op} |C - N2|.\n'
    return rule.strip()


def count_balance(target: int, src_cell: Tuple[int, int], color: str = "black", op: str = "eq") -> str:
    """
    Generate a constraint to count the length of "2-way" straight lines.

    A balance loop rule should be defined first.
    """
    rop = reverse_op(op)
    r, c = src_cell
    constraint = ""
    for sign in ["lu", "ld", "ru", "rd"]:
        constraint += (
            f':- balance_{color}({r}, {c}, N1, N2), loop_sign({r}, {c}, "{sign}"), |{r} - N1| + |{c} - N2| {rop} {target}.\n'
        )

    # special case for straight line
    constraint += f':- balance_{color}({r}, {c}, N1, N2), loop_sign({r}, {c}, "ud"), |{r} - N1| + |{r} - N2| {rop} {target}.\n'
    constraint += f':- balance_{color}({r}, {c}, N1, N2), loop_sign({r}, {c}, "lr"), |{c} - N1| + |{c} - N2| {rop} {target}.\n'
    return constraint.strip()


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="balance"))
    solver.add_program_line(fill_path(color="balance"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="balance", adj_type="loop"))
    solver.add_program_line(single_loop(color="balance"))
    solver.add_program_line(loop_sign(color="balance"))
    solver.add_program_line(balance_rule(color="black"))
    solver.add_program_line(balance_rule(color="white"))

    for (r, c), (clue, color) in E.clues.items():
        solver.add_program_line(f"balance({r}, {c}).")
        if color == "b":
            solver.add_program_line(f"black({r}, {c}).")
            if clue != "":
                solver.add_program_line(count_balance(int(clue), (r, c), color="black"))
        elif color == "w":
            solver.add_program_line(f"white({r}, {c}).")
            if clue != "":
                solver.add_program_line(count_balance(int(clue), (r, c), color="white"))

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
