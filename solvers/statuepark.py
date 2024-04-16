"""The Statue Park solver."""

from typing import List

from . import utilsx
from .utilsx.common import display, grid, shade_c
from .utilsx.encoding import Encoding
from .utilsx.reachable import grid_color_connected
from .utilsx.rule import adjacent
from .utilsx.shape import OMINOES, all_shapes, count_shape, general_shape
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    shapeset = E.params["shapeset"]
    if shapeset == "Tetrominoes":
        omino_num, omino_count_type = 4, 1
    elif shapeset == "Pentominoes":
        omino_num, omino_count_type = 5, 1
    elif shapeset == "Double Tetrominoes":
        omino_num, omino_count_type = 4, 2
    else:
        raise ValueError("Shape set not supported.")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not black"))

    solver.add_program_line(all_shapes(f"omino_{omino_num}", color="black"))
    for i, o_shape in enumerate(OMINOES[omino_num].values()):
        solver.add_program_line(general_shape(f"omino_{omino_num}", i, o_shape, color="black", adj_type=4))
        solver.add_program_line(count_shape(omino_count_type, name=f"omino_{omino_num}", _id=i, color="black"))

    for (r, c), clue in E.clues.items():
        if clue == "b":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "w":
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
