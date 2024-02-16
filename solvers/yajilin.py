"""The Yajilin solver."""

from typing import List, Tuple

from . import utilsx
from .utilsx.encoding import Encoding

from .utilsx.fact import grid, display
from .utilsx.rule import adjacent, avoid_adjacent
from .utilsx.solution import solver, rc_to_grid
from .utilsx.loops import NON_DIRECTED


def shade_custom() -> str:
    """
    Custom shading. A grid fact should be defined first.
    """
    return "{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C)."


def yajilin_count(target: int, src_cell: Tuple[int, int], direction: str, color: str = "black") -> str:
    """
    Generates a constraint for counting the number of {color} cells in a row / col.

    A grid fact should be defined first.
    """
    src_r, src_c = src_cell
    op = "<" if direction in "lu" else ">"

    if direction in "lr":
        return f":- #count {{ C1 : {color}({src_r}, C1), C1 {op} {src_c} }} != {target}."

    if direction in "ud":
        return f":- #count {{ R1 : {color}(R1, {src_c}), R1 {op} {src_r} }} != {target}."

    raise ValueError("Invalid direction, must be one of 'l', 'r', 'u', 'd'.")


def hamilton_loop(color: str = "white"):
    # NON_DIRECTED = ["J", "7", "L", "r", "-", "1"]
    dirs = ["lu", "ld", "ru", "rd", "lr", "ud"]
    fact = 'direction("l"; "u"; "r"; "d").\n'
    fact += f"{{ grid_direction(R, C, D) }} :- {color}(R, C), direction(D).\n"
    for sign, direction in zip(NON_DIRECTED, dirs):
        d1, d2 = direction
        fact += (
            f'loop_sign(R, C, "{sign}") :- {color}(R, C), grid_direction(R, C, "{d1}"), grid_direction(R, C, "{d2}").\n'
        )

    constraint = f":- {color}(R, C), #count{{ D: grid_direction(R, C, D) }} != 2.\n"
    constraint += f':- {color}(R, C), grid_direction(R, C, "l"), not grid_direction(R, C-1, "r").\n'
    constraint += f':- {color}(R, C), grid_direction(R, C, "u"), not grid_direction(R-1, C, "d").\n'
    constraint += f':- {color}(R, C), grid_direction(R, C, "r"), not grid_direction(R, C+1, "l").\n'
    constraint += f':- {color}(R, C), grid_direction(R, C, "d"), not grid_direction(R+1, C, "u").\n'
    return fact + constraint


def connected_loop(color: str = "white") -> str:
    """
    Define adjacent loops and constrain the connectivity.
    A grid fact and a loop/path fact should be defined first.
    """
    initial = f"reachable_loop(R, C) :- (R, C) = #min{{ (R1, C1) : {color}(R1, C1) }}.\n"
    propagation = f"reachable_loop(R, C) :- {color}(R, C), reachable_loop(R1, C1), adj_loop(R1, C1, R, C).\n"
    constraint = f":- {color}(R, C), not reachable_loop(R, C)."
    return initial + propagation + constraint


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_custom())
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent(color="black"))
    # solver.add_program_line(connected(color="white"))
    solver.add_program_line(hamilton_loop(color="white"))
    solver.add_program_line(adjacent("loop"))
    solver.add_program_line(connected_loop(color="white"))

    for (r, c), clue in E.clues.items():
        if clue == "gray":
            solver.add_program_line(f"gray({r}, {c}).")
        elif clue[1] == "gray":
            num, direction = clue[0]
            solver.add_program_line(f"gray({r}, {c}).")
            solver.add_program_line(yajilin_count(int(num), (r, c), direction, color="black"))

    solver.add_program_line(display(item="black"))
    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
