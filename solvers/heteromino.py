"""The Heteromino solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, edge, grid
from .utilsx.helper import tag_encode
from .utilsx.rule import adjacent, split_by_edge
from .utilsx.shape import all_same_shape, shape_omino
from .utilsx.solution import solver


def avoid_adj_same_omino(color: str = "black") -> str:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An split by edge rule, an omino rule should be defined first.
    """
    t_be = tag_encode("belong_to_shape", "omino", 3, color)
    return f":- grid(R, C), grid(R1, C1), {t_be}(R, C, T), {t_be}(R1, C1, T), split_by_edge(R, C, R1, C1)."


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    shaded = len(E.clues)
    if (E.R * E.C - shaded) % 3 != 0:
        raise ValueError("The grid cannot be divided into 3-ominoes!")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(split_by_edge())

    if shaded == 0:
        solver.add_program_line("black(-1, -1).")

    for (r, c), _ in E.clues.items():
        solver.add_program_line(f"black({r}, {c}).")
        solver.add_program_line(f"vertical_line({r}, {c}).")
        solver.add_program_line(f"vertical_line({r}, {c + 1}).")
        solver.add_program_line(f"horizontal_line({r}, {c}).")
        solver.add_program_line(f"horizontal_line({r + 1}, {c}).")

    solver.add_program_line(shape_omino(3, color="not black", adj_type="edge", distinct_variant=True))
    solver.add_program_line(all_same_shape("omino_3", color="not black"))
    solver.add_program_line(avoid_adj_same_omino(color="not black"))
    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
