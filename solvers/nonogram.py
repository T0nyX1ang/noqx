"""The Nonogram solver."""

from typing import Dict, List, Union, Tuple

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display
from .utilsx.rule import shade_c
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def nono_row(C: int, clues: Dict[int, Tuple[Union[int, str]]], color: str = "black"):
    constraints = []
    constraints.append("row_count(R, -1, -1, 0) :- grid(R, _), R >= 0.")
    constraints.append(f"row_count(R, C, N, V) :- grid(R, C), not {color}(R, C), row_count(R, C - 1, N, _), V = 0.")
    constraints.append(
        f"row_count(R, C, N, V) :- grid(R, C), {color}(R, C), grid(R, C - 1), not {color}(R, C - 1), row_count(R, C - 1, N - 1, _), V = 1."
    )
    constraints.append(
        f"row_count(R, C, N, V) :- grid(R, C), {color}(R, C), grid(R, C - 1), {color}(R, C - 1), row_count(R, C - 1, N, V - 1)."
    )

    for i, clue in clues.items():
        if len(clue) == 1 and clue[0] == 0:
            constraints.append(f":- not row_count({i}, {C - 1}, -1, _).")
        else:
            constraints.append(f":- not row_count({i}, {C - 1}, {len(clue) - 1}, _).")
            for j, num in enumerate(clue):
                if num != "?":
                    constraints.append(
                        f":- grid({i}, C), {color}({i}, C), row_count({i}, C, {j}, V), row_count({i}, C + 1, {j}, 0), V != {num}."
                    )

    return "\n".join(constraints)


def nono_col(R: int, clues: Dict[int, Tuple[Union[int, str]]], color: str = "black"):
    constraints = []
    constraints.append("col_count(-1, C, -1, 0) :- grid(_, C), C >= 0.")
    constraints.append(f"col_count(R, C, N, V) :- grid(R, C), not {color}(R, C), col_count(R - 1, C, N, _), V = 0.")
    constraints.append(
        f"col_count(R, C, N, V) :- grid(R, C), {color}(R, C), grid(R - 1, C), not {color}(R - 1, C), col_count(R - 1, C, N - 1, _), V = 1."
    )
    constraints.append(
        f"col_count(R, C, N, V) :- grid(R, C), {color}(R, C), grid(R - 1, C), {color}(R - 1, C), col_count(R - 1, C, N, V - 1)."
    )

    for i, clue in clues.items():
        if len(clue) == 1 and clue[0] == 0:
            constraints.append(f":- not row_count({R - 1}, {i}, -1, _).")
        else:
            constraints.append(f":- not col_count({R - 1}, {i}, {len(clue) - 1}, _).")
            for j, num in enumerate(clue):
                if num != "?":
                    constraints.append(
                        f":- grid(R, {i}), {color}(R, {i}), col_count(R, {i}, {j}, V), col_count(R + 1, {i}, {j}, 0), V != {num}."
                    )

    return "\n".join(constraints)


def solve(E: Encoding) -> List:
    if len(E.top) + len(E.left) == 0:
        raise ValueError("No clues provided.")

    top_clues = {}
    for c in E.top:
        top_clues[c] = tuple(int(clue) if clue != "?" else "?" for clue in E.top[c].split())

    left_clues = {}
    for r in E.left:
        left_clues[r] = tuple(int(clue) if clue != "?" else "?" for clue in E.left[r].split())

    solver.reset()
    solver.add_program_line(f"grid(-1..{E.R}, -1..{E.C}).")
    solver.add_program_line(shade_c())
    solver.add_program_line(f"not black(-1, -1..{E.C}).")
    solver.add_program_line(f"not black(-1..{E.R}, -1).")
    solver.add_program_line(f"not black({E.R}, -1..{E.C}).")
    solver.add_program_line(f"not black(-1..{E.R}, {E.C}).")
    solver.add_program_line(nono_row(E.C, left_clues))
    solver.add_program_line(nono_col(E.R, top_clues))
    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
