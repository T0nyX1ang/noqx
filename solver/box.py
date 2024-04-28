"""The Box solver."""

from typing import Dict, List

from .core.common import display, grid, shade_c
from .core.encoding import Encoding
from .core.solution import solver


def count_box_col(target: int, c: int, color: str = "black") -> str:
    """Generate a rule to count the number of 'boxes' in each column."""
    return f":- #sum {{ N: box_col(R, N), {color}(R, {c}) }} != {target}."


def count_box_row(target: int, r: int, color: str = "black") -> str:
    """Generate a rule to count the number of 'boxes' in each column."""
    return f":- #sum {{ N: box_row(C, N), {color}({r}, C) }} != {target}."


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())

    for (r, c), color in E.clues.items():
        if color == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif color == "green":
            solver.add_program_line(f"not black({r}, {c}).")

    for c in range(E.C):
        target = int(E.bottom[c]) if c in E.bottom else c + 1
        solver.add_program_line(f"box_row({c}, {target}).")

    for r, num in E.left.items():
        solver.add_program_line(count_box_row(int(num), r, color="black"))

    for r in range(E.R):
        target = int(E.right[r]) if r in E.right else r + 1
        solver.add_program_line(f"box_col({r}, {target}).")

    for c, num in E.top.items():
        solver.add_program_line(count_box_col(int(num), c, color="black"))

    solver.add_program_line(display())
    solver.solve()
    return solver.solutions
