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
    shade_cc,
    rev_op_dict,
)
from .utilsx.solutions import solver


def connected_area(color: str = "black", adj_type: int = 4, area_id: int = None) -> str:
    """
    Generate a constraint to check connected areas of {color} cells.

    An adjacent rule and a grid rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    tag = f"reachable_{color_escape}" + f"_area_{area_id}" * (area_id is not None)
    _type = f"not connected_{area_id-1}(" if area_id > 0 else "grid("

    not_connected = f", {_type}R1, C1)" if area_id > 0 else ""
    initial = f"{tag}(R, C) :- (R, C) = #min{{ (R1, C1) : grid(R1, C1), {color}(R1, C1){not_connected} }}."
    propagation = f"{tag}(R, C) :- {tag}(R1, C1), adj_{adj_type}(R, C, R1, C1), {_type}R, C), {color}(R, C)."
    add_connected = f"connected_{area_id}(R, C) :- connected_{area_id-1}(R, C).\n" if area_id > 0 else ""
    add_connected += f"connected_{area_id}(R, C) :- {tag}(R, C)."
    return initial + "\n" + propagation + "\n" + add_connected, tag


def count_tag(target: int, op: str = "eq", tag: str = None) -> str:
    """
    Generates a constraint for counting the number of {tag} cells.

    A grid rule should be defined first.
    """
    op = rev_op_dict[op]

    return f":- #count {{ R, C : {tag}(R, C) }} {op} {target}."


def valid_omino(num: int = 4, tag: str = None, color: str = "black"):
    """
    Generates a rule for a valid omino.

    A grid rule or an area rule should be defined first.
    """

    count_valid = (
        f"#count {{ R, C : {tag}(R, C), {color}(R, C), omino_{num}(T, V, DR, DC), R = AR + DR, C = AC + DC }} = {num}"
    )
    return f"valid_omino_{num}(T, AR, AC) :- {tag}(AR, AC), omino_{num}(T, V, _, _), {count_valid}."


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
    
    shapeset = E.params['shapeset']
    if shapeset == 'Tetrominoes':
        omino_num, omino_count_type = 4, 1
    elif shapeset == 'Pentominoes':
        omino_num, omino_count_type = 5, 1
    elif shapeset == 'Double Tetrominoes':
        omino_num, omino_count_type = 4, 2
    else:
        raise ValueError('Shape set not supported.')
    solver.add_program_line(omino(omino_num))
    ominos = list(OMINOES[omino_num].keys())
    omino_count = len(ominos) * omino_count_type
    black_num = omino_num * omino_count
    
    solver.add_program_line(shade_cc(["black", "white"]))
    solver.add_program_line(adjacent())
    solver.add_program_line(connected(color="white"))
    solver.add_program_line(count(black_num, color="black", _type="grid"))

    for i in range(omino_count):
        program, tag = connected_area(color="black", area_id=i)
        solver.add_program_line(program)
        solver.add_program_line(count_tag(target=omino_num, tag=tag))
        solver.add_program_line(valid_omino(num=omino_num, tag=tag))
    
    for o in ominos:
        solver.add_program_line(restrict_omino_count(num=omino_num, _type=f'"{o}"', target=omino_count_type))

    for (r, c), clue in E.clues.items():
        if clue == "b":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "w":
            solver.add_program_line(f"white({r}, {c}).")

    solver.add_program_line(display(color="black"))
    solver.solve()

    return solver.solutions

def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
