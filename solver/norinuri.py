"""The Norinuri solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import count_reachable_src, grid_src_color_connected
from .core.solution import solver


def nori_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint for Norinori puzzles.

    A grid rule and an adjacent rule should be defined first.
    """
    return f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }} != 1."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("black"))

    solver.add_program_line(adjacent())
    solver.add_program_line(nori_adjacent(color="black"))

    all_src = []
    for (r, c), clue in puzzle.text.items():
        all_src.append((r, c))
    assert len(all_src) > 0, "No clues found."

    for (r, c), clue in puzzle.text.items():
        assert isinstance(clue, int) or (isinstance(clue, str) and clue == "?"), "Clue must be an integer or '?'."
        solver.add_program_line(f"not black({r}, {c}).")

        current_excluded = [src for src in all_src if src != (r, c)]
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color="not black"))
        if clue != "?":
            solver.add_program_line(count_reachable_src(clue, (r, c), color="not black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Norinuri",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VTfj5NAEH7nr2jmeR9YoEj3xdR69aXiKTVNQ8gFkMsRQU7oGrOE/70zA4pn+mJMmjMx2/n45tuBfvuz+6rTthDSpp8bCHxi82TA4QQ+hz21fXmqCrUQa316aFokQrzbbsV9WnWFFU9VidWblTJrYd6oGCQIcDAkJMK8V715q0woTIRdIDzUdmORg/RmpgfuJ7YZRWkjDyeO9Ig0L9u8Ku52o3KrYrMXQP/zit8mCnXzrYDJB+V5U2clCVl6wsF0D+Xj1NPpT81nPdXKZBBmPdqNLth1Z7tER7vELtilUfy93eqxuWR0lQwDTvgHtHqnYnL9cabBTCPVI4aqB1fiqz6uMq8JeD6mwc906dKHX6LHSfCp36F9MebSWaFAG+aH4DkoeL/kvxf43pNvog/Jbo6MW0aHcY9mhXEZXzPajEvGHdfcMB4YN4weo881L2i4fzQhV7ATu+O5etqW/56WWDFEur1P8wI3Y6jrrGgXYdPWaQV47gcLvgNH7NI18v8quPpVQJNvP7f9/9zs4ImEL7ots0ZDYp0B",
        }
    ],
}
