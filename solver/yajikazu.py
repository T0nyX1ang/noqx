"""The Yajilin-Kazusan solver."""

from typing import List, Tuple

from .core.common import display, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.reachable import grid_color_connected
from .core.solution import solver


def yajikazu_count(target: int, src_cell: Tuple[int, int], arrow_direction: int, color: str = "black") -> str:
    """
    Generates a constraint for counting the number of {color} cells in a row / col.

    A grid fact should be defined first.
    """
    src_r, src_c = src_cell
    op = "<" if arrow_direction in [0, 1] else ">"

    if arrow_direction in [1, 2]:  # left, right
        return f":- not {color}({src_r}, {src_c}), #count {{ C1 : {color}({src_r}, C1), C1 {op} {src_c} }} != {target}."

    if arrow_direction in [0, 3]:  # up, down
        return f":- not {color}({src_r}, {src_c}), #count {{ R1 : {color}(R1, {src_c}), R1 {op} {src_r} }} != {target}."

    raise AssertionError("Invalid direction.")


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="gray"))
    solver.add_program_line(grid_color_connected(color="not gray"))

    # avoid all cells are unshaded
    solver.add_program_line(":- { gray(R, C) } = 0.")

    for (r, c), clue in puzzle.text.items():
        assert isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows."
        num, direction = clue.split("_")
        assert num.isdigit() and direction.isdigit(), "Invalid arrow or number clue."
        solver.add_program_line(yajikazu_count(int(num), (r, c), int(direction), color="gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
