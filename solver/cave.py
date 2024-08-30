"""The Cave solver."""

from typing import List, Tuple

from .core.common import display, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.helper import tag_encode
from .core.neighbor import adjacent
from .core.reachable import (
    border_color_connected,
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from .core.solution import solver


def cave_product_rule(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4):
    """
    Product rule for cave.

    A bulb_src_color_connected rule should be defined first.
    """
    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"
    return f":- {count_r}, {count_c}, CR * CC != {target}."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not black"))
    solver.add_program_line(border_color_connected(puzzle.row, puzzle.col, color="black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(bulb_src_color_connected((r, c), color="not black"))

        if num == "?":  # question mark case
            continue

        assert isinstance(num, int), "Clue must be an integer."
        if puzzle.param["product"]:
            solver.add_program_line(cave_product_rule(num, (r, c), color="not black"))
        else:
            solver.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions
