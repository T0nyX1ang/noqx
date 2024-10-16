"""The Shakashaka solver."""

from typing import List

from .core.common import display, grid
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def shaka() -> str:
    """
    Generate a constraint to force rectangles.

    A grid rule should be defined first.
    """
    definition = "white_down(R, C) :- grid(R, C), white(R, C).\n"
    definition += 'white_down(R, C) :- grid(R, C), triangle(R, C, "ul").\n'
    definition += 'white_down(R, C) :- grid(R, C), triangle(R, C, "ur").\n'
    definition += "white_right(R, C) :- grid(R, C), white(R, C).\n"
    definition += 'white_right(R, C) :- grid(R, C), triangle(R, C, "ul").\n'
    definition += 'white_right(R, C) :- grid(R, C), triangle(R, C, "dl").\n'

    rule_rect = "rect_ul(R, C) :- grid(R, C), white(R, C), not white_down(R - 1, C), not white_right(R, C - 1).\n"
    rule_rect += "rect_l(R, C) :- grid(R, C), white(R, C), rect_ul(R - 1, C), not white_right(R, C - 1).\n"
    rule_rect += "rect_l(R, C) :- grid(R, C), white(R, C), rect_l(R - 1, C), not white_right(R, C - 1).\n"
    rule_rect += "rect_u(R, C) :- grid(R, C), white(R, C), rect_ul(R, C - 1), not white_down(R - 1, C).\n"
    rule_rect += "rect_u(R, C) :- grid(R, C), white(R, C), rect_u(R, C - 1), not white_down(R - 1, C).\n"
    rule_rect += "remain(R, C) :- grid(R, C), rect_l(R, C - 1), rect_u(R - 1, C).\n"
    rule_rect += "remain(R, C) :- grid(R, C), rect_l(R, C - 1), remain(R - 1, C).\n"
    rule_rect += "remain(R, C) :- grid(R, C), remain(R, C - 1), rect_u(R - 1, C).\n"
    rule_rect += 'remain(R, C) :- grid(R, C), remain(R, C - 1), remain(R - 1, C), not triangle(R, C, "dr").\n'

    rule_slant = 'slant_ul(R, C) :- grid(R, C), triangle(R, C, "ul"), triangle(R, C+1, "ur"), triangle(R+1, C, "dl").\n'
    rule_slant += 'slant_ul(R, C) :- grid(R, C), triangle(R, C, "ul"), triangle(R, C+1, "ur"), triangle(R+1, C-1, "ul").\n'
    rule_slant += 'slant_ul(R, C) :- grid(R, C), triangle(R, C, "ul"), triangle(R+1, C, "dl"), triangle(R-1, C+1, "ul").\n'
    rule_slant += 'slant_ul(R, C) :- grid(R, C), triangle(R, C, "ul"), triangle(R-1, C+1, "ul"), triangle(R+1, C-1, "ul"), white(R+1, C), white(R, C+1).\n'
    rule_slant += 'slant_ur(R, C) :- grid(R, C), triangle(R, C, "ur"), triangle(R, C-1, "ul"), triangle(R+1, C, "dr").\n'
    rule_slant += 'slant_ur(R, C) :- grid(R, C), triangle(R, C, "ur"), triangle(R, C-1, "ul"), triangle(R+1, C+1, "ur").\n'
    rule_slant += 'slant_ur(R, C) :- grid(R, C), triangle(R, C, "ur"), triangle(R+1, C, "dr"), triangle(R-1, C-1, "ur").\n'
    rule_slant += 'slant_ur(R, C) :- grid(R, C), triangle(R, C, "ur"), triangle(R-1, C-1, "ur"), triangle(R+1, C+1, "ur"), white(R+1, C), white(R, C-1).\n'
    rule_slant += 'slant_dl(R, C) :- grid(R, C), triangle(R, C, "dl"), triangle(R, C+1, "dr"), triangle(R-1, C, "ul").\n'
    rule_slant += 'slant_dl(R, C) :- grid(R, C), triangle(R, C, "dl"), triangle(R, C+1, "dr"), triangle(R-1, C-1, "dl").\n'
    rule_slant += 'slant_dl(R, C) :- grid(R, C), triangle(R, C, "dl"), triangle(R-1, C, "ul"), triangle(R+1, C+1, "dl").\n'
    rule_slant += 'slant_dl(R, C) :- grid(R, C), triangle(R, C, "dl"), triangle(R-1, C-1, "dl"), triangle(R+1, C+1, "dl"), white(R-1, C), white(R, C+1).\n'
    rule_slant += 'slant_dr(R, C) :- grid(R, C), triangle(R, C, "dr"), triangle(R, C-1, "dl"), triangle(R-1, C, "ur").\n'
    rule_slant += 'slant_dr(R, C) :- grid(R, C), triangle(R, C, "dr"), triangle(R, C-1, "dl"), triangle(R-1, C+1, "dr").\n'
    rule_slant += 'slant_dr(R, C) :- grid(R, C), triangle(R, C, "dr"), triangle(R-1, C, "ur"), triangle(R+1, C-1, "dr").\n'
    rule_slant += 'slant_dr(R, C) :- grid(R, C), triangle(R, C, "dr"), triangle(R-1, C+1, "dr"), triangle(R+1, C-1, "dr"), white(R-1, C), white(R, C-1).\n'
    rule_slant += "remain(R, C) :- grid(R, C), slant_ul(R, C-1), slant_ul(R-1, C).\n"
    rule_slant += "remain(R, C) :- grid(R, C), slant_dl(R, C-1), slant_dl(R+1, C).\n"
    rule_slant += "remain(R, C) :- grid(R, C), slant_ur(R, C+1), slant_ur(R-1, C).\n"

    constraint = ':- grid(R, C), triangle(R, C, "ul"), not slant_ul(R, C).\n'
    constraint += ':- grid(R, C), triangle(R, C, "ur"), not slant_ur(R, C).\n'
    constraint += ':- grid(R, C), triangle(R, C, "dl"), not slant_dl(R, C).\n'
    constraint += ':- grid(R, C), triangle(R, C, "dr"), not slant_dr(R, C).\n'
    constraint += ":- grid(R, C), remain(R, C), not white(R, C).\n"
    constraint += ":- grid(R, C), white(R, C), not rect_ul(R, C), not rect_l(R, C), not rect_u(R, C), not remain(R, C).\n"

    data = definition + rule_rect + rule_slant + constraint
    return data.replace("not not ", "").strip()


def shade_shaka() -> str:
    """Generate a constraint to shade the cells in shakashaka."""
    rule = '{white(R, C); triangle(R, C, "ul"); triangle(R, C, "ur"); triangle(R, C, "dl"); triangle(R, C, "dr")} = 1 :- grid(R, C), not black(R, C).'
    return rule


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_shaka())
    solver.add_program_line(adjacent())

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")

    for (r, c), clue in puzzle.text.items():
        if isinstance(clue, int):
            solver.add_program_line(f":- #count{{ R, C: adj_4({r}, {c}, R, C), triangle(R, C, _) }} != {clue}.")

    for (r, c), symbol in puzzle.symbol.items():
        if symbol.startswith("tri__"):
            solver.add_program_line(f"triangle({r}, {c}, {symbol.split('__')[1]}).")
        else:
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(shaka())
    solver.add_program_line(display(item="triangle", size=3))
    solver.solve()

    return solver.solutions
