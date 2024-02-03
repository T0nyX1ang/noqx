"""The Nonogram solver."""
# 桶帝牛逼！

from typing import Dict, List, Union, Tuple

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display
from .utilsx.rule import shade_c
from .utilsx.solution import solver


def nono_row(C: int, clues: Dict[int, Tuple[Union[int, str]]], color: str = "black"):
    """Generates the nonogram row constraints."""
    prefix = "row_count(R, C, N, V) :- grid(R, C), row_count_value_range(R, N, V)"
    constraints = []
    constraints.append("row_count(R, -1, -1, 0) :- grid(R, _), R >= 0.")
    constraints.append(f"{prefix}, not {color}(R, C), row_count(R, C - 1, N, _), V = 0.")
    constraints.append(
        f"{prefix}, {color}(R, C), grid(R, C - 1), not {color}(R, C - 1), row_count(R, C - 1, N - 1, _), V = 1."
    )
    constraints.append(f"{prefix}, {color}(R, C), grid(R, C - 1), {color}(R, C - 1), row_count(R, C - 1, N, V - 1).")

    for i, clue in clues.items():
        constraints.append(f"row_count_value_range({i}, -1, 0).")
        if len(clue) == 1 and clue[0] == 0:
            constraints.append(f":- grid({i}, C), not row_count({i}, C, -1, 0).")
        else:
            constraints.append(f":- not row_count({i}, {C - 1}, {len(clue) - 1}, _).")
            for j, num in enumerate(clue):
                if num != "?":
                    slope = f"row_count({i}, C, {j}, V), row_count({i}, C + 1, {j}, 0)"
                    constraints.append(f"row_count_value_range({i}, {j}, 0..{num}).")
                    constraints.append(f":- grid({i}, C), {color}({i}, C), {slope} , V != {num}.")
                else:
                    constraints.append(f"row_count_value_range({i}, {j}, 0..{C+2-2*len(clue)}).")

    return "\n".join(constraints)


def nono_col(R: int, clues: Dict[int, Tuple[Union[int, str]]], color: str = "black"):
    """Generates the nonogram column constraints."""
    prefix = "col_count(R, C, N, V) :- grid(R, C), col_count_value_range(C, N, V)"
    constraints = []
    constraints.append("col_count(-1, C, -1, 0) :- grid(_, C), C >= 0.")
    constraints.append(f"{prefix}, not {color}(R, C), col_count(R - 1, C, N, _), V = 0.")
    constraints.append(
        f"{prefix}, {color}(R, C), grid(R - 1, C), not {color}(R - 1, C), col_count(R - 1, C, N - 1, _), V = 1."
    )
    constraints.append(f"{prefix}, {color}(R, C), grid(R - 1, C), {color}(R - 1, C), col_count(R - 1, C, N, V - 1).")

    for i, clue in clues.items():
        constraints.append(f"col_count_value_range({i}, -1, 0).")
        if len(clue) == 1 and clue[0] == 0:
            constraints.append(f":- grid(R, {i}), not col_count(R, {i}, -1, 0).")
        else:
            constraints.append(f":- not col_count({R}, {i}, {len(clue) - 1}, 0).")
            for j, num in enumerate(clue):
                if num != "?":
                    slope = f"col_count(R, {i}, {j}, V), col_count(R + 1, {i}, {j}, 0)"
                    constraints.append(f"col_count_value_range({i}, {j}, 0..{num}).")
                    constraints.append(f":- grid(R, {i}), {color}(R, {i}), {slope}, V != {num}.")
                else:
                    constraints.append(f"col_count_value_range({i}, {j}, 0..{R+2-2*len(clue)}).")

    return "\n".join(constraints)


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


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

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")

    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
