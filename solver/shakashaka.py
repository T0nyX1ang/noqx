"""The Shakashaka solver."""

from typing import List

from .core.common import display, grid
from .core.penpa import Puzzle
from .core.neighbor import adjacent
from .core.solution import solver


def shaka() -> str:
    """
    Generate a constraint to force rectangles.

    A grid rule should be defined first.
    *** Triangle direction notations: ul = 1, ur = 4, dl = 2, dr = 3 ***
    """
    definition = "white_down(R, C) :- grid(R, C), white(R, C).\n"
    definition += "white_down(R, C) :- grid(R, C), triangle(R, C, 1).\n"
    definition += "white_down(R, C) :- grid(R, C), triangle(R, C, 4).\n"
    definition += "white_right(R, C) :- grid(R, C), white(R, C).\n"
    definition += "white_right(R, C) :- grid(R, C), triangle(R, C, 1).\n"
    definition += "white_right(R, C) :- grid(R, C), triangle(R, C, 2).\n"

    rule_rect = "rect_ul(R, C) :- grid(R, C), white(R, C), not white_down(R - 1, C), not white_right(R, C - 1).\n"
    rule_rect += "rect_l(R, C) :- grid(R, C), white(R, C), rect_ul(R - 1, C), not white_right(R, C - 1).\n"
    rule_rect += "rect_l(R, C) :- grid(R, C), white(R, C), rect_l(R - 1, C), not white_right(R, C - 1).\n"
    rule_rect += "rect_u(R, C) :- grid(R, C), white(R, C), rect_ul(R, C - 1), not white_down(R - 1, C).\n"
    rule_rect += "rect_u(R, C) :- grid(R, C), white(R, C), rect_u(R, C - 1), not white_down(R - 1, C).\n"
    rule_rect += "remain(R, C) :- grid(R, C), rect_l(R, C - 1), rect_u(R - 1, C).\n"
    rule_rect += "remain(R, C) :- grid(R, C), rect_l(R, C - 1), remain(R - 1, C).\n"
    rule_rect += "remain(R, C) :- grid(R, C), remain(R, C - 1), rect_u(R - 1, C).\n"
    rule_rect += "remain(R, C) :- grid(R, C), remain(R, C - 1), remain(R - 1, C), not triangle(R, C, 3).\n"

    rule_slant = "slant_ul(R, C) :- grid(R, C), triangle(R, C, 1), triangle(R, C+1, 4), triangle(R+1, C, 2).\n"
    rule_slant += "slant_ul(R, C) :- grid(R, C), triangle(R, C, 1), triangle(R, C+1, 4), triangle(R+1, C-1, 1).\n"
    rule_slant += "slant_ul(R, C) :- grid(R, C), triangle(R, C, 1), triangle(R+1, C, 2), triangle(R-1, C+1, 1).\n"
    rule_slant += "slant_ul(R, C) :- grid(R, C), triangle(R, C, 1), triangle(R-1, C+1, 1), triangle(R+1, C-1, 1), white(R+1, C), white(R, C+1).\n"
    rule_slant += "slant_ur(R, C) :- grid(R, C), triangle(R, C, 4), triangle(R, C-1, 1), triangle(R+1, C, 3).\n"
    rule_slant += "slant_ur(R, C) :- grid(R, C), triangle(R, C, 4), triangle(R, C-1, 1), triangle(R+1, C+1, 4).\n"
    rule_slant += "slant_ur(R, C) :- grid(R, C), triangle(R, C, 4), triangle(R+1, C, 3), triangle(R-1, C-1, 4).\n"
    rule_slant += "slant_ur(R, C) :- grid(R, C), triangle(R, C, 4), triangle(R-1, C-1, 4), triangle(R+1, C+1, 4), white(R+1, C), white(R, C-1).\n"
    rule_slant += "slant_dl(R, C) :- grid(R, C), triangle(R, C, 2), triangle(R, C+1, 3), triangle(R-1, C, 1).\n"
    rule_slant += "slant_dl(R, C) :- grid(R, C), triangle(R, C, 2), triangle(R, C+1, 3), triangle(R-1, C-1, 2).\n"
    rule_slant += "slant_dl(R, C) :- grid(R, C), triangle(R, C, 2), triangle(R-1, C, 1), triangle(R+1, C+1, 2).\n"
    rule_slant += "slant_dl(R, C) :- grid(R, C), triangle(R, C, 2), triangle(R-1, C-1, 2), triangle(R+1, C+1, 2), white(R-1, C), white(R, C+1).\n"
    rule_slant += "slant_dr(R, C) :- grid(R, C), triangle(R, C, 3), triangle(R, C-1, 2), triangle(R-1, C, 4).\n"
    rule_slant += "slant_dr(R, C) :- grid(R, C), triangle(R, C, 3), triangle(R, C-1, 2), triangle(R-1, C+1, 3).\n"
    rule_slant += "slant_dr(R, C) :- grid(R, C), triangle(R, C, 3), triangle(R-1, C, 4), triangle(R+1, C-1, 3).\n"
    rule_slant += "slant_dr(R, C) :- grid(R, C), triangle(R, C, 3), triangle(R-1, C+1, 3), triangle(R+1, C-1, 3), white(R-1, C), white(R, C-1).\n"
    rule_slant += "remain(R, C) :- grid(R, C), slant_ul(R, C-1), slant_ul(R-1, C).\n"
    rule_slant += "remain(R, C) :- grid(R, C), slant_dl(R, C-1), slant_dl(R+1, C).\n"
    rule_slant += "remain(R, C) :- grid(R, C), slant_ur(R, C+1), slant_ur(R-1, C).\n"

    constraint = ":- grid(R, C), triangle(R, C, 1), not slant_ul(R, C).\n"
    constraint += ":- grid(R, C), triangle(R, C, 4), not slant_ur(R, C).\n"
    constraint += ":- grid(R, C), triangle(R, C, 2), not slant_dl(R, C).\n"
    constraint += ":- grid(R, C), triangle(R, C, 3), not slant_dr(R, C).\n"
    constraint += ":- grid(R, C), remain(R, C), not white(R, C).\n"
    constraint += ":- grid(R, C), white(R, C), not rect_ul(R, C), not rect_l(R, C), not rect_u(R, C), not remain(R, C).\n"

    data = definition + rule_rect + rule_slant + constraint
    return data.replace("not not ", "").strip()


def shade_shaka() -> str:
    """Generate a constraint to shade the cells in shakashaka."""
    rule = "{white(R, C); triangle(R, C, 1); triangle(R, C, 4); triangle(R, C, 2); triangle(R, C, 3)} = 1 :- grid(R, C), not black(R, C)."
    return rule


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_shaka())
    solver.add_program_line(adjacent())

    for (r, c), clue in puzzle.text.items():
        solver.add_program_line(f"black({r}, {c}).")
        if isinstance(clue, int):
            solver.add_program_line(f":- #count{{ R, C: adj_4({r}, {c}, R, C), triangle(R, C, _) }} != {clue}.")

    for (r, c), symbol in puzzle.symbol.items():
        if symbol.startswith("tri__"):
            solver.add_program_line(f"triangle({r}, {c}, {symbol.split('__')[1]}).")
        else:
            solver.add_program_line(f"white({r}, {c}).")

    solver.add_program_line(shaka())
    solver.add_program_line(display(item="triangle", size=3))
    solver.solve()

    return solver.solutions
