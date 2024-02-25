"""The Yajilin solver."""

from typing import List, Tuple

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import single_loop, connected_loop, fill_path
from .utilsx.rule import adjacent, avoid_adjacent
from .utilsx.solution import solver


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


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
    solver.add_program_line(fill_path(color="white"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(avoid_adjacent(color="black"))
    solver.add_program_line(connected_loop(color="white"))
    solver.add_program_line(single_loop(color="white", visit_all=True))
    solver.add_program_line(adjacent(_type="loop"))

    for (r, c), clue in E.clues.items():
        if clue == "gray":
            solver.add_program_line(f"gray({r}, {c}).")
        elif clue[1] == "gray":
            num, d = clue[0]
            solver.add_program_line(f"gray({r}, {c}).")
            solver.add_program_line(yajilin_count(int(num), (r, c), d, color="black"))

    solver.add_program_line(display(item="black"))
    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
