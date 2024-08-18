"""The Castle castle solver."""

from typing import List

from .core.common import direction, display, fill_path, grid, shade_c
from .core.penpa import Puzzle
from .core.loop import separate_item_from_loop, single_loop
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.solution import solver


def wall_length(r: int, c: int, d: int, num: int) -> str:
    """
    Constrain the castle length.

    A grid direction fact should be defined first.
    """
    if d == 0:
        return f':- #count{{ R: grid_direction(R, {c}, "d"), R < {r} }} != {num}.'
    if d == 1:
        return f':- #count{{ C: grid_direction({r}, C, "r"), C < {c} }} != {num}.'
    if d == 2:
        return f':- #count{{ C: grid_direction({r}, C, "r"), C > {c} }} != {num}.'
    if d == 3:
        return f':- #count{{ R: grid_direction(R, {c}, "d"), R > {r} }} != {num}.'

    raise ValueError("Invalid direction.")


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="castle"))
    solver.add_program_line(fill_path(color="castle"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="castle", adj_type="loop"))
    solver.add_program_line(single_loop(color="castle"))
    solver.add_program_line(separate_item_from_loop(inside_item="white", outside_item="black"))

    for (r, c), color_code in puzzle.surface.items():
        solver.add_program_line(f"not castle({r}, {c}).")
        if color_code == 4:
            solver.add_program_line(f"black({r}, {c}).")
        elif color_code in [1, 3, 8]:  # shaded color (DG, GR, LG)
            solver.add_program_line(f"gray({r}, {c}).")

    for (r, c), clue in puzzle.text.items():
        if isinstance(clue, str) and len(clue) == 0:
            continue

        assert isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows."
        num, d = clue.split("_")
        assert num.isdigit() and d.isdigit(), "Invalid arrow or number clue."
        solver.add_program_line(wall_length(r, c, int(d), int(num)))

        if (r, c) not in puzzle.surface:
            solver.add_program_line(f"white({r}, {c}).")
            solver.add_program_line(f"not castle({r}, {c}).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
