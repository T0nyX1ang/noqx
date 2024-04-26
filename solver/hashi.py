"""The Hashi solver."""

from typing import Dict, List

from .core.common import direction, display, grid
from .core.encoding import Encoding
from .core.reachable import grid_color_connected
from .core.solution import solver


def hashi_bridge(R: int, C: int) -> str:
    """
    Generate a rule for hashi constraints.

    A grid fact and a direction fact should be defined first.
    """
    rule = 'direction1("l";"u";"r";"d").\n'
    rule += "{ grid_direction(R, C, D, N) : num(N) } 1 :- grid(R, C), number(R, C, _), direction1(D).\n"
    rule += ":- number(R, C, N), #sum{ N1, D: grid_direction(R, C, D, N1) } != N.\n"
    rule += ':- grid(R, C), num(N), grid_direction(R, C, "l", N), not grid_direction(R, C-1, "r", N).\n'
    rule += ':- grid(R, C), num(N), grid_direction(R, C, "r", N), not grid_direction(R, C+1, "l", N).\n'
    rule += ':- grid(R, C), num(N), grid_direction(R, C, "u", N), not grid_direction(R-1, C, "d", N).\n'
    rule += ':- grid(R, C), num(N), grid_direction(R, C, "d", N), not grid_direction(R+1, C, "u", N).\n'

    show = 'grid_direction(R, C, "l", 1) :- grid(R, C), hashi_bridge(R, C, "H", 1).\n'
    show += 'grid_direction(R, C, "r", 1) :- grid(R, C), hashi_bridge(R, C, "H", 1).\n'
    show += 'grid_direction(R, C, "l", 2) :- grid(R, C), hashi_bridge(R, C, "H", 2).\n'
    show += 'grid_direction(R, C, "r", 2) :- grid(R, C), hashi_bridge(R, C, "H", 2).\n'
    show += 'grid_direction(R, C, "u", 1) :- grid(R, C), hashi_bridge(R, C, "V", 1).\n'
    show += 'grid_direction(R, C, "d", 1) :- grid(R, C), hashi_bridge(R, C, "V", 1).\n'
    show += 'grid_direction(R, C, "u", 2) :- grid(R, C), hashi_bridge(R, C, "V", 2).\n'
    show += 'grid_direction(R, C, "d", 2) :- grid(R, C), hashi_bridge(R, C, "V", 2).\n'

    adj = "hashi_all(R, C) :- hashi_bridge(R, C, _, _).\n"
    adj += "hashi_all(R, C) :- number(R, C, _).\n"
    adj += "adj_loop(R0, C0, R, C) :- R=R0, C=C0+1, hashi_all(R, C), hashi_all(R0, C0).\n"
    adj += "adj_loop(R0, C0, R, C) :- R=R0+1, C=C0, hashi_all(R, C), hashi_all(R0, C0).\n"
    adj += "adj_loop(R0, C0, R, C) :- adj_loop(R, C, R0, C0)."
    return rule + show + adj.strip()


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("HV"))
    solver.add_program_line("num(1..2).")
    solver.add_program_line("{ hashi_bridge(R, C, D, N): direction(D), num(N) } 1 :- grid(R, C), not number(R, C, _).")
    solver.add_program_line(hashi_bridge(E.R, E.C))
    solver.add_program_line(grid_color_connected(color="hashi_all", adj_type="loop"))

    for (r, c), clue in E.clues.items():
        solver.add_program_line(f"number({r}, {c}, {clue}).")

    solver.add_program_line(display(item="grid_direction", size=4))
    solver.solve()

    return solver.solutions
