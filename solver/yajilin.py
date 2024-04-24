"""The Yajilin solver."""

from typing import Dict, List, Tuple

from .core.common import direction, display, fill_path, grid
from .core.encoding import Encoding
from .core.loop import single_loop
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.reachable import grid_color_connected
from .core.solution import solver


def yajilin_count(target: int, src_cell: Tuple[int, int], _direction: str, color: str = "black") -> str:
    """
    Generates a constraint for counting the number of {color} cells in a row / col.

    A grid fact should be defined first.
    """
    src_r, src_c = src_cell
    op = "<" if _direction in "lu" else ">"

    if _direction in "lr":
        return f":- #count {{ C1 : {color}({src_r}, C1), C1 {op} {src_c} }} != {target}."

    if _direction in "ud":
        return f":- #count {{ R1 : {color}(R1, {src_c}), R1 {op} {src_r} }} != {target}."

    raise ValueError("Invalid direction, must be one of 'l', 'r', 'u', 'd'.")


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
    solver.add_program_line(fill_path(color="white"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
    solver.add_program_line(grid_color_connected(color="white", adj_type="loop"))
    solver.add_program_line(single_loop(color="white"))

    for (r, c), clue in E.clues.items():
        if clue == "gray":
            solver.add_program_line(f"gray({r}, {c}).")
        elif clue[1] == "gray":
            num, d = clue[0]
            solver.add_program_line(f"gray({r}, {c}).")
            solver.add_program_line(yajilin_count(int(num), (r, c), d, color="black"))

    solver.add_program_line(display(item="black"))
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
