"""The Yajilin solver."""

from typing import List, Tuple

from .core.common import direction, display, fill_path, grid
from .core.loop import single_loop
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.solution import solver


def yajilin_count(target: int, src_cell: Tuple[int, int], arrow_direction: int, color: str = "black") -> str:
    """
    Generates a constraint for counting the number of {color} cells in a row / col.

    A grid fact should be defined first.
    """
    src_r, src_c = src_cell
    op = "<" if arrow_direction in [0, 1] else ">"

    if arrow_direction in [1, 2]:  # left, right
        return f":- #count {{ C1 : {color}({src_r}, C1), C1 {op} {src_c} }} != {target}."

    if arrow_direction in [0, 3]:  # up, down
        return f":- #count {{ R1 : {color}(R1, {src_c}), R1 {op} {src_r} }} != {target}."

    raise AssertionError("Invalid direction, must be one of 'l', 'r', 'u', 'd'.")


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
    solver.add_program_line(fill_path(color="white"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
    solver.add_program_line(grid_color_connected(color="white", adj_type="loop"))
    solver.add_program_line(single_loop(color="white"))

    for (r, c), clue in puzzle.text.items():
        solver.add_program_line(f"gray({r}, {c}).")

        # empty clue or space or question mark clue (for compatibility)
        if isinstance(clue, str) and (len(clue) == 0 or clue.isspace() or clue == "?"):
            continue

        assert isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows."
        num, d = clue.split("_")
        assert num.isdigit() and d.isdigit(), "Invalid arrow or number clue."
        solver.add_program_line(yajilin_count(int(num), (r, c), int(d), color="black"))

    solver.add_program_line(display(item="black"))
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
