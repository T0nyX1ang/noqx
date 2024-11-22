"""The Masyu solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import defined, direction, display, fill_path, grid, shade_c
from noqx.rule.loop import loop_straight, loop_turning, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def masyu_black_rule() -> str:
    """
    Generate a rule for black masyu.

    A straight rule, a turning rule, and an loop_adjacent rule should be defined first.
    """
    black_rule = ":- grid(R, C), black(R, C), not turning(R, C).\n"
    black_rule += ":- grid(R, C), black(R, C), turning(R, C), adj_loop(R, C, R1, C1), not straight(R1, C1).\n"
    return black_rule


def masyu_white_rule() -> str:
    """
    Generate a rule for white masyu rule.

    A straight rule and a turning rule should be defined first.
    """
    white_rule = ":- grid(R, C), white(R, C), not straight(R, C).\n"
    white_rule += ":- grid(R, C), white(R, C), straight(R, C), { turning(R1, C1): adj_loop(R, C, R1, C1) } = 0.\n"
    return white_rule


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="black"))
    solver.add_program_line(defined(item="white"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="masyu"))
    solver.add_program_line(fill_path(color="masyu"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="masyu", adj_type="loop"))
    solver.add_program_line(single_loop(color="masyu"))
    solver.add_program_line(loop_straight(color="masyu"))
    solver.add_program_line(loop_turning(color="masyu"))
    solver.add_program_line(masyu_black_rule())
    solver.add_program_line(masyu_white_rule())

    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert d == Direction.CENTER, "The symbol should be placed in the center."
        solver.add_program_line(f"masyu({r}, {c}).")
        if symbol_name == "circle_L__1":
            solver.add_program_line(f"white({r}, {c}).")
        if symbol_name == "circle_L__2":
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Masyu",
    "category": "loop",
    "aliases": ["mashu"],
    "examples": [
        {
            "data": "m=edit&p=7VXBjtMwEL3nK1Zz9sETp23iW1m2XEKBbdGqiqJVtgQ1IiWladDiqv++40mkgJgTCLRIKPXr67NTvzeaxO2XrjiWCrX/mFjRN10RxjzCeMpDD9e6OtWlvVLz7rRrjkSUerNYqI9F3ZZBNqzKg7NLrJsr98pmEILigZAr986e3WvrNsqtaAoUkpYSQ1Ah0ZuR3vG8Z9e9iJr4cuBEN0S31XFbl/dpr7y1mVsr8Pu84Ls9hX3ztYT+Nv69bfYPlRceihOFaXfVYZhpuw/Np25Yi/lFuXlvNxXsmtGup71dzwS7PsVv262rz+Wj5DTJLxeq+C15vbeZt/1+pPFIV/ZMuGRExo09QzSjv0Ha53tvEMWSOkFRDUU1kdSpEdVIUmcTUZ2KqrhbrEVVTByLiRMxcSImRi2GQy2mQy3aQC36QBSLgShWA1EsB4ZiPdCIIdHIKY33Hf4kR3L4SA4vdx1KbUd9uuBuDRnX1MzKGcaXjJpxwpjymhvGO8Zrxohxymtm/nH45QfmD9nJTP/i/fGa/HtaHmSQ0qvqatkc90VNL6zVrjiUQIfCJYBH4JEZf8b8Pyf+/jnhq6+fW/M/Nzv0OMK+aL91kAdP",
        },
        {
            "url": "https://puzz.link/p?masyu/21/15/000a0l2943300030l00200i10j0063c60091000670303010606j3600133013ia16l0110000600306b2063000300020960ai301030",
            "test": False,
        },
    ],
}
