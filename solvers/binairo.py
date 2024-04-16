"""The Binario solver."""

from typing import List

from . import utilsx
from .utilsx.common import display, grid
from .utilsx.encoding import Encoding
from .utilsx.rule import count, shade_c
from .utilsx.shape import avoid_rect
from .utilsx.solution import solver


def unique_linecolor(colors: List[str], _type: str = "row") -> str:
    """
    Generates a constraint for unique row / column in a grid.
    At least one pair of cells in the same row / column should have different colors.

    A grid rule should be defined first.
    """
    if _type == "row":
        colors_row = ", ".join(
            f"#count {{ C : grid(R1, C), grid(R2, C), {color}(R1, C), not {color}(R2, C) }} = 0" for color in colors
        ).replace("not not ", "")
        return f":- grid(R1, _), grid(R2, _), R1 < R2, {colors_row}."

    if _type == "col":
        colors_col = ", ".join(
            f"#count {{ R : grid(R, C1), grid(R, C2), {color}(R, C1), not {color}(R, C2) }} = 0" for color in colors
        ).replace("not not ", "")
        return f":- grid(_, C1), grid(_, C2), C1 < C2, {colors_col}."

    raise ValueError("Invalid line type, must be one of 'row', 'col'.")


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    if not (E.R % 2 == 0 and E.C % 2 == 0):
        raise ValueError("# rows and # columns must both be even!")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(count(E.R // 2, color="black", _type="row"))
    solver.add_program_line(count(E.C // 2, color="black", _type="col"))
    solver.add_program_line(unique_linecolor(colors=["black", "not black"], _type="row"))
    solver.add_program_line(unique_linecolor(colors=["black", "not black"], _type="col"))
    solver.add_program_line(avoid_rect(1, 3, color="black"))
    solver.add_program_line(avoid_rect(1, 3, color="not black"))
    solver.add_program_line(avoid_rect(3, 1, color="black"))
    solver.add_program_line(avoid_rect(3, 1, color="not black"))

    for (r, c), num in E.clues.items():
        if num == 1:
            solver.add_program_line(f"black({r}, {c}).")
        elif num == 0:
            solver.add_program_line(f"not black({r}, {c}).")
        else:
            raise ValueError(f"Invalid clue: {num}")

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
