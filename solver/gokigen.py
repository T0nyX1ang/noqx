"""The Gokigen solver."""

from typing import List

from .core.common import direction, display, fill_path, grid
from .core.penpa import Puzzle
from .core.solution import solver


def slant_rule() -> str:
    """Generate slant rules."""
    rule = ':- grid(R, C), grid_direction(R, C, "ul"), not grid_direction(R - 1, C - 1, "dr").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "ur"), not grid_direction(R - 1, C + 1, "dl").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "dl"), not grid_direction(R + 1, C - 1, "ur").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "dr"), not grid_direction(R + 1, C + 1, "ul").\n'

    rule += "grid_direc_num(R, C, D, 0) :- grid(R, C), direction(D), not grid_direction(R, C, D).\n"
    rule += "grid_direc_num(R, C, D, 1) :- grid_direction(R, C, D).\n"
    rule += ':- grid(R, C), grid(R + 1, C + 1), { grid_direction(R, C, "dr"); grid_direction(R, C + 1, "dl") } != 1.'
    return rule.strip()


def no_loop() -> str:
    """Ensure there is no loop in the grid."""
    rule = "reachable(R, C) :- grid(R, C), not grid(R - 1, C - 1).\n"
    rule += "reachable(R, C) :- grid(R, C), not grid(R + 1, C + 1).\n"
    rule += 'reachable(R, C) :- grid(R, C), reachable(R - 1, C - 1), not grid_direction(R, C - 1, "ur").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R - 1, C + 1), not grid_direction(R, C + 1, "ul").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R + 1, C - 1), not grid_direction(R, C - 1, "dr").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R + 1, C + 1), not grid_direction(R, C + 1, "dl").\n'
    rule += ":- grid(R, C), not reachable(R, C).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
    solver.add_program_line(direction(["ul", "ur", "dl", "dr"]))
    solver.add_program_line(fill_path(color="grid"))
    solver.add_program_line(slant_rule())
    solver.add_program_line(no_loop())

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be an integer."
        solver.add_program_line(f":- #count{{ D: grid_direction({r + 1}, {c + 1}, D) }} != {num}.")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
