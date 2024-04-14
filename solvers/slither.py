"""The Slitherlink solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import fill_path, single_loop
from .utilsx.reachable import grid_color_connected
from .utilsx.rule import adjacent, count_adjacent_lines, shade_c
from .utilsx.solution import solver


def convert_direction_to_edge() -> str:
    """Convert grid direction fact to edge fact."""
    rule = 'horizontal_line(R, C) :- grid_direction(R, C, "r").\n'
    rule += 'vertical_line(R, C) :- grid_direction(R, C, "d").\n'
    return rule.strip()


def wolf_out_sheep_in() -> str:
    """
    Generate a constraint to make wolves outside of the loop, and make sheep inside of loop.

    A grid direction fact should be defined first.
    """
    out_loop = "out_loop(-1, C) :- grid(_, C).\n"
    out_loop += 'out_loop(R, C) :- grid(R, C), out_loop(R - 1, C), not grid_direction(R, C, "r").\n'
    out_loop += 'out_loop(R, C) :- grid(R, C), not out_loop(R - 1, C), grid_direction(R, C, "r").\n'
    constraint = ":- sheep(R, C), out_loop(R, C).\n"
    constraint += ":- wolf(R, C), not out_loop(R, C)."
    return out_loop + constraint


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R + 1, E.C + 1))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="slither"))
    solver.add_program_line(fill_path(color="slither"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="slither", adj_type="loop"))
    solver.add_program_line(single_loop(color="slither"))
    solver.add_program_line(convert_direction_to_edge())

    flag = False
    for (r, c), clue in E.clues.items():
        if clue == "W":
            flag = True
            solver.add_program_line(f"wolf({r}, {c}).")
        elif clue == "S":
            flag = True
            solver.add_program_line(f"sheep({r}, {c}).")
        else:
            solver.add_program_line(count_adjacent_lines(int(clue), (r, c)))

    if flag:
        solver.add_program_line(wolf_out_sheep_in())

    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.add_program_line(display(item="vertical_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
