"""The Heteromino solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, edge, grid
from .utilsx.helper import tag_encode
from .utilsx.rule import adjacent, split_by_edge
from .utilsx.solution import solver


def valid_omino_3(color: str = "black") -> str:
    delta = (("-1", "+0"), ("+0", "-1"), ("+1", "+0"), ("+0", "+1"))
    idx = 0
    constraint = ""
    t_va = tag_encode("valid_omino", 3, color)
    t_be = tag_encode("belong_to_omino", 3, color)
    for i in range(4):
        dx1, dy1 = delta[i]
        for j in range(i + 1, 4):
            dx2, dy2 = delta[j]
            idx += 1
            remain = [delta[k] for k in range(4) if k not in [i, j]]
            (dx3, dy3), (dx4, dy4) = remain
            adj = f"adj_edge(R, C, R{dx1}, C{dy1}), adj_edge(R, C, R{dx2}, C{dy2}), not adj_edge(R, C, R{dx3}, C{dy3}), not adj_edge(R, C, R{dx4}, C{dy4})"
            nadj = f"#count {{ R1, C1: adj_edge(R{dx1}, C{dy1}, R1, C1) }} = 1, #count {{ R1, C1: adj_edge(R{dx2}, C{dy2}, R1, C1) }} = 1"
            constraint += f"{t_va}(R, C, {idx}) :- grid(R, C), {color}(R, C), {adj}, {nadj}.\n"
    constraint += f"{t_be}(R, C, T) :- grid(R, C), {t_va}(R, C, T).\n"
    constraint += f"{t_be}(R, C, T) :- grid(R, C), adj_edge(R, C, R1, C1), {t_va}(R1, C1, T).\n"
    constraint += f":- grid(R, C), {color}(R, C), {{ {t_be}(R, C, T) }} < 1."
    return constraint


def avoid_adj_omino_3(color: str = "black") -> str:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An split by edge rule, an omino rule should be defined first.
    """
    t_be = tag_encode("belong_to_omino", 3, color)
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

    solver.add_program_line(valid_omino_3(color="not black"))
    solver.add_program_line(avoid_adj_omino_3(color="not black"))
    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
