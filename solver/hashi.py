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
    rule = ':- hashi_bridge(R, C, "H", N), not hashi_bridge(R, C+1, "H", N), not number(R, C+1, _).\n'
    rule += ':- hashi_bridge(R, C, "H", N), not hashi_bridge(R, C-1, "H", N), not number(R, C-1, _).\n'
    rule += ':- hashi_bridge(R, C, "V", N), not hashi_bridge(R+1, C, "V", N), not number(R+1, C, _).\n'
    rule += ':- hashi_bridge(R, C, "V", N), not hashi_bridge(R-1, C, "V", N), not number(R-1, C, _).\n'

    rule += f"grid_big(-1..{R}, -1..{C}).\n"
    rule += "num_bridge(R, C, D, N) :- grid(R, C), hashi_bridge(R, C, D, N).\n"
    rule += "num_bridge(R, C, D, 0) :- grid_big(R, C), direction(D), not hashi_bridge(R, C, D, _).\n"
    rule += ':- number(R, C, N), num_bridge(R, C-1, "H", N1), num_bridge(R-1, C, "V", N2), num_bridge(R, C+1, "H", N3), num_bridge(R+1, C, "V", N4), N != N1 + N2 + N3 + N4.\n'

    show = 'loop_sign(R, C, "-") :- grid(R, C), hashi_bridge(R, C, "H", 1).\n'
    show += 'loop_sign(R, C, "=") :- grid(R, C), hashi_bridge(R, C, "H", 2).\n'
    show += 'loop_sign(R, C, "1") :- grid(R, C), hashi_bridge(R, C, "V", 1).\n'
    show += 'loop_sign(R, C, "‖") :- grid(R, C), hashi_bridge(R, C, "V", 2).\n'

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

    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions
