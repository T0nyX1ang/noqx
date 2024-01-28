"""The Statue Park solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid, omino, OMINOES
from .utilsx.rule import (
    adjacent,
    connected,
    connected_parts,
    count,
    count_connected_parts,
    count_valid_omino,
    shade_c,
)
from .utilsx.shape import valid_omino
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

    ominos = list(OMINOES[omino_num].keys())
    omino_count = len(ominos) * omino_count_type
    black_num = omino_num * omino_count

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(omino(omino_num))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(count(black_num, color="black"))
    solver.add_program_line(connected(color="not black"))
    solver.add_program_line(connected_parts(color="black"))
    solver.add_program_line(count_connected_parts(target=omino_num, color="black"))
    solver.add_program_line(valid_omino(num=omino_num, color="black"))

    for o_type in ominos:
        solver.add_program_line(count_valid_omino(omino_count_type, f'"{o_type}"', num=omino_num, color="black"))

    for (r, c), clue in E.clues.items():
        if clue == "b":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "w":
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(color="black"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
