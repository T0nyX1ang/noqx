"""The Statue Park solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import adjacent, connected, count_shape, shade_c
from .utilsx.shape import all_shapes, shape_omino, OMINOES
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


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
    solver.add_program_line(connected(color="not black"))

    solver.add_program_line(shape_omino(omino_num, color="black", adj_type=4))
    solver.add_program_line(all_shapes(f"omino_{omino_num}", color="black"))

    for i in range(len(OMINOES[omino_num].keys())):
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
