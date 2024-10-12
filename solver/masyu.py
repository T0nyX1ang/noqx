"""The Masyu solver."""

from typing import List

from .core.common import direction, display, fill_path, grid, shade_c
from .core.loop import loop_sign, single_loop
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.solution import solver


def masyu_black_rule() -> str:
    """
    Generate a rule for black masyu rule.

    A loop sign rule should be defined first.
    """
    black_rule = 'black_rule(R, C) :- loop_sign(R, C, "lu"), loop_sign(R - 1, C, "ud"), loop_sign(R, C - 1, "lr").\n'
    black_rule += 'black_rule(R, C) :- loop_sign(R, C, "ld"), loop_sign(R + 1, C, "ud"), loop_sign(R, C - 1, "lr").\n'
    black_rule += 'black_rule(R, C) :- loop_sign(R, C, "ru"), loop_sign(R - 1, C, "ud"), loop_sign(R, C + 1, "lr").\n'
    black_rule += 'black_rule(R, C) :- loop_sign(R, C, "rd"), loop_sign(R + 1, C, "ud"), loop_sign(R, C + 1, "lr").\n'
    black_rule += ":- grid(R, C), black(R, C), not black_rule(R, C).\n"
    return black_rule


def masyu_white_rule() -> str:
    """
    Generate a rule for white masyu rule.

    A loop sign rule should be defined first.
    """
    white_rule = ""
    for sign in ["lu", "ld", "ru", "rd"]:
        white_rule += f'white_rule(R, C) :- loop_sign(R, C, "ud"), loop_sign(R - 1, C, "{sign}").\n'
        white_rule += f'white_rule(R, C) :- loop_sign(R, C, "ud"), loop_sign(R + 1, C, "{sign}").\n'
        white_rule += f'white_rule(R, C) :- loop_sign(R, C, "lr"), loop_sign(R, C - 1, "{sign}").\n'
        white_rule += f'white_rule(R, C) :- loop_sign(R, C, "lr"), loop_sign(R, C + 1, "{sign}").\n'
    white_rule += ":- grid(R, C), white(R, C), not white_rule(R, C).\n"
    return white_rule


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="masyu"))
    solver.add_program_line(fill_path(color="masyu"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="masyu", adj_type="loop"))
    solver.add_program_line(single_loop(color="masyu"))
    solver.add_program_line(loop_sign(color="masyu"))
    solver.add_program_line(masyu_black_rule())
    solver.add_program_line(masyu_white_rule())

    for (r, c), symbol_name in puzzle.symbol.items():
        solver.add_program_line(f"masyu({r}, {c}).")
        if symbol_name == "circle_L__1__0":
            solver.add_program_line(f"white({r}, {c}).")
        elif symbol_name == "circle_L__2__0":
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
