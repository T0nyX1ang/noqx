"""The Cave solver."""

from typing import List, Tuple

from . import utilsx
from .utilsx.common import display, grid, shade_c
from .utilsx.encoding import Encoding, tag_encode
from .utilsx.neighbor import adjacent
from .utilsx.reachable import (
    border_color_connected,
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from .utilsx.solution import solver


def cave_product_rule(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: str = 4):
    """
    Product rule for cave.

    A bulb_src_color_connected rule should be defined first.
    """
    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"
    return f":- {count_r}, {count_c}, CR * CC != {target}."


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not black"))
    solver.add_program_line(border_color_connected(E.R, E.C, color="black"))

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        else:
            num = int(clue)
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(bulb_src_color_connected((r, c), color="not black"))
            if E.params["Product"]:
                solver.add_program_line(cave_product_rule(num, (r, c), color="not black"))
            else:
                solver.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions):
    return utilsx.decode(solutions)
