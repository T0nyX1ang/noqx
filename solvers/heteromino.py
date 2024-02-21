"""The Heteromino solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, edge, grid, omino
from .utilsx.helper import tag_encode
from .utilsx.rule import adjacent, count_reachable_edge, reachable_edge
from .utilsx.shape import valid_omino
from .utilsx.solution import solver


def avoid_adjacent_same_shape(num: int = 3, color: str = "black") -> None:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An area adjacent rule, an omino rule should be defined first.
    """
    t_va = tag_encode("valid_omino", num, color)
    t_be = tag_encode("belong_to_omino", num, color)
    constraint = f"{t_be}(T, V, AR + DR, AC + DC) :- grid(AR, AC), omino_{num}(T, V, DR, DC), {t_va}(T, V, AR, AC).\n"
    constraint += f":- {t_be}(T, V, R, C), {t_be}(T, V, R1, C1), not adj_edge(R, C, R1, C1), adj_4(R, C, R1, C1)."
    return constraint


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    shaded = len(E.clues)
    if (E.R * E.C - shaded) % 3 != 0:
        raise ValueError("The grid cannot be divided into 3-ominoes!")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(omino(3))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(reachable_edge())
    solver.add_program_line(count_reachable_edge(3, color="not black"))

    if shaded == 0:
        solver.add_program_line("black(-1, -1).")

    for (r, c), _ in E.clues.items():
        solver.add_program_line(f"black({r}, {c}).")
        solver.add_program_line(f"vertical_line({r}, {c}).")
        solver.add_program_line(f"vertical_line({r}, {c + 1}).")
        solver.add_program_line(f"horizontal_line({r}, {c}).")
        solver.add_program_line(f"horizontal_line({r + 1}, {c}).")

    solver.add_program_line(valid_omino(3, color="not black", _type="edge", distinct_variant=True))
    solver.add_program_line(avoid_adjacent_same_shape(3, color="not black"))
    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
