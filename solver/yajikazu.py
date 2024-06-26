"""The Yajilin-Kazusan solver."""

from typing import Dict, List, Tuple

from .core.common import display, grid, shade_c
from .core.encoding import Encoding
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.reachable import grid_color_connected
from .core.solution import solver


def yajikazu_count(target: int, src_cell: Tuple[int, int], direction: str, color: str = "black") -> str:
    """
    Generates a constraint for counting the number of {color} cells in a row / col.

    A grid fact should be defined first.
    """
    src_r, src_c = src_cell

    if direction == "l":
        return f":- not {color}({src_r}, {src_c}), #count {{ C1 : {color}({src_r}, C1), C1 < {src_c} }} != {target}."

    if direction == "r":
        return f":- not {color}({src_r}, {src_c}), #count {{ C1 : {color}({src_r}, C1), C1 > {src_c} }} != {target}."

    if direction == "u":
        return f":- not {color}({src_r}, {src_c}), #count {{ R1 : {color}(R1, {src_c}), R1 < {src_r} }} != {target}."

    if direction == "d":
        return f":- not {color}({src_r}, {src_c}), #count {{ R1 : {color}(R1, {src_c}), R1 > {src_r} }} != {target}."

    raise ValueError("Invalid direction, must be one of 'l', 'r', 'u', 'd'.")


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="gray"))
    solver.add_program_line(grid_color_connected(color="not gray"))

    for (r, c), clue in E.clues.items():
        if clue == "gray":
            solver.add_program_line(f"gray({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not gray({r}, {c}).")
        elif clue[1] == "gray":
            num, direction = clue[0]
            solver.add_program_line(f"gray({r}, {c}).")
            solver.add_program_line(yajikazu_count(int(num), (r, c), direction, color="gray"))
        elif clue[1] == "green":
            num, direction = clue[0]
            solver.add_program_line(f"not gray({r}, {c}).")
            solver.add_program_line(yajikazu_count(int(num), (r, c), direction, color="gray"))
        else:
            num, direction = clue
            solver.add_program_line(yajikazu_count(int(num), (r, c), direction, color="gray"))

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions
