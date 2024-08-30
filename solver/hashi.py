"""The Hashi solver."""

from typing import List

from .core.common import direction, display, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.solution import solver


def hashi_bridge() -> str:
    """
    Generate a rule for hashi constraints.

    A grid fact and a direction fact should be defined first.
    """
    rule = "num(1..2)."
    rule += "{ grid_direction(R, C, D, N) : direction(D), num(N) } :- grid(R, C), hashi(R, C).\n"
    rule += ":- N != -1, number(R, C, N), #sum{ N1, D: grid_direction(R, C, D, N1) } != N.\n"

    rule += "pass_by_loop(R, C) :- grid(R, C), #count { D: grid_direction(R, C, D, _) } = 2.\n"
    rule += 'pass_by_straight(R, C) :- grid(R, C), num(N), grid_direction(R, C, "l", N), grid_direction(R, C, "r", N).\n'
    rule += 'pass_by_straight(R, C) :- grid(R, C), num(N), grid_direction(R, C, "u", N), grid_direction(R, C, "d", N).\n'
    rule += ":- grid(R, C), hashi(R, C), not number(R, C, _), not pass_by_straight(R, C).\n"
    rule += ":- grid(R, C), hashi(R, C), not number(R, C, _), not pass_by_loop(R, C).\n"

    # path along the edges should be connected
    rule += ':- grid(R, C), grid_direction(R, C, "l", _), not grid_direction(R, C - 1, "r", _).\n'
    rule += ':- grid(R, C), grid_direction(R, C, "u", _), not grid_direction(R - 1, C, "d", _).\n'
    rule += ':- grid(R, C), grid_direction(R, C, "r", _), not grid_direction(R, C + 1, "l", _).\n'
    rule += ':- grid(R, C), grid_direction(R, C, "d", _), not grid_direction(R + 1, C, "u", _).\n'

    # path along the edges should have the same bridges
    rule += ':- grid(R, C), grid_direction(R, C, "l", N1), grid_direction(R, C - 1, "r", N2), N1 != N2.\n'
    rule += ':- grid(R, C), grid_direction(R, C, "u", N1), grid_direction(R - 1, C, "d", N2), N1 != N2.\n'
    rule += ':- grid(R, C), grid_direction(R, C, "r", N1), grid_direction(R, C + 1, "l", N2), N1 != N2.\n'
    rule += ':- grid(R, C), grid_direction(R, C, "d", N1), grid_direction(R + 1, C, "u", N2), N1 != N2.\n'

    # path inside the cell (not number) should have the same bridges, not sure if this is necessary
    rule += ':- grid(R, C), num(N), not number(R, C, _), grid_direction(R, C, "l", N), not grid_direction(R, C, "r", N).\n'
    rule += ':- grid(R, C), num(N), not number(R, C, _), grid_direction(R, C, "u", N), not grid_direction(R, C, "d", N).\n'

    adj = 'adj_loop(R0, C0, R, C) :- R = R0, C = C0 + 1, grid(R, C), grid(R0, C0), grid_direction(R, C, "l", _).\n'
    adj += 'adj_loop(R0, C0, R, C) :- R = R0 + 1, C = C0, grid(R, C), grid(R0, C0), grid_direction(R, C, "u", _).\n'
    adj += "adj_loop(R0, C0, R, C) :- adj_loop(R, C, R0, C0)."
    return rule + adj.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lrud"))
    solver.add_program_line(shade_c(color="hashi"))
    solver.add_program_line(hashi_bridge())
    solver.add_program_line(grid_color_connected(color="hashi", adj_type="loop"))

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(f"hashi({r}, {c}).")
        solver.add_program_line(f"number({r}, {c}, {num if isinstance(num, int) else -1}).")

    solver.add_program_line(display(item="grid_direction", size=4))
    solver.solve()

    return solver.solutions
