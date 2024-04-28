"""The Jousan solver."""

from typing import Dict, List

from .core.helper import full_bfs
from .core.common import area, display, grid, shade_c
from .core.encoding import Encoding
from .core.solution import solver


def jousan_constraint():
    """Constrain consecutive lines."""
    # black for horizontal, not black for vertical
    rule = ":- grid(R, C), grid(R+2, C), black(R, C), black(R+1, C), black(R+2, C).\n"
    rule += ":- grid(R, C), grid(R, C+2), not black(R, C), not black(R, C+1), not black(R, C+2).\n"
    rule += 'content(R, C, "—") :- grid(R, C), black(R, C).\n'
    rule += 'content(R, C, "|") :- grid(R, C), not black(R, C).'
    return rule


def count_hor_ver(area: int = 0, num1: int = 0, num2: int = 0):
    """Limit the number of horizontal or vertical lines."""
    rule = f"count_area({area}, N) :- #count{{ R, C: area({area}, R, C), black(R, C) }} = N.\n"
    rule += f":- not count_area({area}, {num1}), not count_area({area}, {num2})."
    return rule


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(jousan_constraint())

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        num = None
        for r, c in ar:
            if (r, c) in E.clues:
                num = E.clues[(r, c)]
        if num:
            solver.add_program_line(count_hor_ver(i, num, len(ar) - num))

    solver.add_program_line(display(item="content", size=3))
    solver.solve()

    return solver.solutions
