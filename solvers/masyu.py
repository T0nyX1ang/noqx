"""The Masyu solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import single_loop, connected_loop, fill_path
from .utilsx.rule import adjacent, shade_c
from .utilsx.solution import solver


def masyu_black_rule() -> str:
    """
    Generate a rule for black masyu rule.

    A loop sign rule should be defined first.
    """
    black_rule = 'black_rule(R, C) :- loop_sign(R, C, "J"), loop_sign(R - 1, C, "1"), loop_sign(R, C - 1, "-").\n'
    black_rule += 'black_rule(R, C) :- loop_sign(R, C, "7"), loop_sign(R + 1, C, "1"), loop_sign(R, C - 1, "-").\n'
    black_rule += 'black_rule(R, C) :- loop_sign(R, C, "L"), loop_sign(R - 1, C, "1"), loop_sign(R, C + 1, "-").\n'
    black_rule += 'black_rule(R, C) :- loop_sign(R, C, "r"), loop_sign(R + 1, C, "1"), loop_sign(R, C + 1, "-").\n'
    black_rule += ":- grid(R, C), black(R, C), not black_rule(R, C).\n"
    return black_rule


def masyu_white_rule() -> str:
    """
    Generate a rule for white masyu rule.

    A loop sign rule should be defined first.
    """
    white_rule = ""
    for sign in ["J", "7", "L", "r"]:
        white_rule += f'white_rule(R, C) :- loop_sign(R, C, "1"), loop_sign(R - 1, C, "{sign}").\n'
        white_rule += f'white_rule(R, C) :- loop_sign(R, C, "1"), loop_sign(R + 1, C, "{sign}").\n'
        white_rule += f'white_rule(R, C) :- loop_sign(R, C, "-"), loop_sign(R, C - 1, "{sign}").\n'
        white_rule += f'white_rule(R, C) :- loop_sign(R, C, "-"), loop_sign(R, C + 1, "{sign}").\n'
    white_rule += ":- grid(R, C), white(R, C), not white_rule(R, C).\n"
    return white_rule


def encode(string: str) -> Encoding:
    def string_encoder(string):
        if string not in {"w", "b", ""}:
            raise ValueError("Invalid input: cells must be w, b, or empty")
        return string

    return utilsx.encode(string, string_encoder)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="masyu_loop"))
    solver.add_program_line(fill_path(color="masyu_loop"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(connected_loop(color="masyu_loop"))
    solver.add_program_line(single_loop(color="masyu_loop"))
    solver.add_program_line(masyu_black_rule())
    solver.add_program_line(masyu_white_rule())

    for (r, c), clue in E.clues.items():
        solver.add_program_line(f"masyu_loop({r}, {c}).")
        if clue == "b":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "w":
            solver.add_program_line(f"white({r}, {c}).")

    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
