"""Akari (Light up) solver."""

from typing import List

from .core.common import display, grid
from .core.helper import tag_encode
from .core.penpa import Puzzle
from .core.neighbor import adjacent, count_adjacent
from .core.solution import solver


def lightup(color: str = "black") -> str:
    """
    A lit rule specially designed for akari.

    A grid fact and an adjacent rule should be defined first.
    """
    tag = tag_encode("reachable", "sun_moon__3__0", "branch", "adj", 4, color)
    initial = f"{tag}(R0, C0, R, C) :- grid(R, C), sun_moon__3__0(R, C), R0 = R, C0 = C."
    propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), {color}(R, C), adj_4(R, C, R1, C1), (R - R0) * (C - C0) = 0."
    constraint1 = f":- sun_moon__3__0(R0, C0), sun_moon__3__0(R, C), |R0 - R| + |C0 - C| != 0, {tag}(R0, C0, R, C)."
    constraint2 = f":- grid(R, C), not black(R, C), not sun_moon__3__0(R, C), {{ {tag}(R0, C0, R, C) }} = 0."

    return initial + "\n" + propagation + "\n" + constraint1 + "\n" + constraint2


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line("{ sun_moon__3__0(R, C) } :- grid(R, C), not black(R, C).")
    solver.add_program_line(adjacent())
    solver.add_program_line(lightup(color="not black"))

    for (r, c), clue in puzzle.text.items():
        solver.add_program_line(f"black({r}, {c}).")
        if isinstance(clue, int):
            solver.add_program_line(count_adjacent(clue, (r, c), color="sun_moon__3__0"))

    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name == "sun_moon__3__0":
            solver.add_program_line(f"sun_moon__3__0({r}, {c}).")

    solver.add_program_line(display(item="sun_moon__3__0"))
    solver.solve()

    return solver.solutions
