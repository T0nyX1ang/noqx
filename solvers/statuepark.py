"""The Statue Park solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.shapes import OMINOES
from .utilsx.rules import (
    adjacent,
    connected,
    count,
    display,
    grid,
    omino,
    shade_c,
    rev_op_dict,
)
from .utilsx.solutions import solver


def connected_area(target: int, color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to check connected areas of {color} cells.

    An adjacent rule and a grid rule should be defined first.
    """
    initial = f"reachable(R0, C0, R, C) :- grid(R0, C0), {color}(R0, C0), R = R0, C = C0."
    propagation = f"reachable(R0, C0, R, C) :- reachable(R0, C0, R1, C1), adj_{adj_type}(R, C, R1, C1), grid(R, C), {color}(R, C)."
    counter = f":- grid(R, C), {color}(R, C), #count {{ R1, C1: reachable(R, C, R1, C1) }} != {target}."
    return initial + "\n" + propagation + "\n" + counter


def valid_omino(num: int = 4, color: str = "black"):
    """
    Generates a rule for a valid omino.

    A grid rule or an area rule should be defined first.
    """

    count_valid = (
        f"#count {{ R, C : grid(R, C), {color}(R, C), omino_{num}(T, V, DR, DC), R = AR + DR, C = AC + DC }} = {num}"
    )
    return f"valid_omino_{num}(T, AR, AC) :- grid(AR, AC), omino_{num}(T, V, _, _), {count_valid}."


def restrict_omino_count(num: int = 4, _type: int = 0, target: int = 1):
    """
    Generates a rule for a valid omino.

    A grid rule or an area rule should be defined first.
    """
    op = rev_op_dict["eq"]
    return f":- #count {{ R, C : valid_omino_{num}({_type}, R, C) }} {op} {target}."


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))

    shapeset = E.params["shapeset"]
    if shapeset == "Tetrominoes":
        omino_num, omino_count_type = 4, 1
    elif shapeset == "Pentominoes":
        omino_num, omino_count_type = 5, 1
    elif shapeset == "Double Tetrominoes":
        omino_num, omino_count_type = 4, 2
    else:
        raise ValueError("Shape set not supported.")

    solver.add_program_line(omino(omino_num))
    ominos = list(OMINOES[omino_num].keys())
    omino_count = len(ominos) * omino_count_type
    black_num = omino_num * omino_count

    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(connected(color="not black"))
    solver.add_program_line(count(black_num, color="black", _type="grid"))

    solver.add_program_line(connected_area(target=omino_num, color="black"))
    solver.add_program_line(valid_omino(num=omino_num))

    for o in ominos:
        solver.add_program_line(restrict_omino_count(num=omino_num, _type=f'"{o}"', target=omino_count_type))

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
