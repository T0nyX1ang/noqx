"""The Slitherlink solver."""

from typing import Dict, List

from .utilsx.common import direction, display, fill_path, grid, shade_c
from .utilsx.encoding import Encoding
from .utilsx.loop import separate_item_from_loop, single_loop
from .utilsx.neighbor import adjacent, count_adjacent_edges
from .utilsx.reachable import grid_color_connected
from .utilsx.solution import solver


def convert_direction_to_edge() -> str:
    """Convert grid direction fact to edge fact."""
    rule = 'horizontal_line(R, C) :- grid_direction(R, C, "r").\n'
    rule += 'vertical_line(R, C) :- grid_direction(R, C, "d").\n'
    return rule.strip()


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R + 1, E.C + 1))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="slither"))
    solver.add_program_line(fill_path(color="slither"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="slither", adj_type="loop"))
    solver.add_program_line(single_loop(color="slither"))
    solver.add_program_line(convert_direction_to_edge())
    solver.add_program_line(adjacent(_type="edge"))

    flag = False
    for (r, c), clue in E.clues.items():
        if clue == "W":
            flag = True
            solver.add_program_line(f"wolf({r}, {c}).")
        elif clue == "S":
            flag = True
            solver.add_program_line(f"sheep({r}, {c}).")
        else:
            solver.add_program_line(count_adjacent_edges(int(clue), (r, c)))

    if flag:
        solver.add_program_line(separate_item_from_loop(inside_item="sheep", outside_item="wolf"))

    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.add_program_line(display(item="vertical_line", size=2))
    solver.solve()

    return solver.solutions
