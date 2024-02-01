"""The Nonogram solver."""

from typing import Dict, List, Union, Tuple

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import shade_c
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s, outside_clues="1001")


def nono_row(R: int, C: int, clues: Dict[int, Tuple[Union[int, str]]], color: str = "black"):
    # Take care that start and end is left-close-right-open.
    constraints = []
    constraints.append(f"row_endgrid(0..{R - 1}, 0..{C}).")
    constraints.append("{ row_start(R, C) } :- grid(R, C).")
    constraints.append("{ row_end(R, C) } :- row_endgrid(R, C).")

    for i, clue in clues.items():
        if len(clue) == 1 and clue[0] == 0:
            constraints.append(f":- grid({i}, C), {color}({i}, C).")
            constraints.append(f":- grid({i}, C), row_start({i}, C).")
            constraints.append(f":- row_endgrid({i}, C), row_end({i}, C).")
        else:
            constraints.append(f"row_count_range({i}, 0..{len(clue)}).")
            constraints.append(f":- not row_start_count({i}, {C - 1}, {len(clue)}).")
            constraints.append(f":- not row_end_count({i}, {C}, {len(clue)}).")
            for j, num in enumerate(clue):
                if num != "?":
                    constraints.append(
                        f":- grid({i}, C), row_start({i}, C), row_start_count({i}, C, {j + 1}), not row_end({i}, C + {num})."
                    )
                    constraints.append(
                        f":- grid({i}, C), row_start({i}, C), row_start_count({i}, C, {j + 1}), not row_start_count({i}, C + {num - 1}, {j + 1})."
                    )

    constraints.append(f":- grid(R, C), not {color}(R, C), row_start_count(R, C, N + 1), row_end_count(R, C, N).")
    constraints.append(f":- grid(R, C), {color}(R, C), row_start_count(R, C, N), row_end_count(R, C, N).")

    constraints.append("row_start_count(R, -1, 0) :- grid(R, _).")
    constraints.append(
        "row_start_count(R, C, N) :- grid(R, C), row_count_range(R, N), row_start(R, C), row_start_count(R, C - 1, N - 1)."
    )
    constraints.append(
        "row_start_count(R, C, N) :- grid(R, C), row_count_range(R, N), not row_start(R, C), row_start_count(R, C - 1, N)."
    )
    constraints.append("row_end_count(R, -1, 0) :- grid(R, _).")
    constraints.append(
        "row_end_count(R, C, N) :- row_endgrid(R, C), row_count_range(R, N), row_end(R, C), row_end_count(R, C - 1, N - 1)."
    )
    constraints.append(
        "row_end_count(R, C, N) :- row_endgrid(R, C), row_count_range(R, N), not row_end(R, C), row_end_count(R, C - 1, N)."
    )
    constraints.append(":- row_start_count(R, C, N1), row_end_count(R, C, N2), N1 > N2 + 1.")
    constraints.append(":- row_start_count(R, C, N1), row_end_count(R, C, N2), N1 < N2.")
    constraints.append(":- grid(R, C), row_end(R, C), row_start(R, C).")

    return "\n".join(constraints)


def nono_col(R: int, C: int, clues: Dict[int, Tuple[Union[int, str]]], color: str = "black"):
    # Take care that start and end is left-close-right-open.
    constraints = []
    constraints.append("{ col_start(R, C) } :- grid(R, C).")
    constraints.append(f"col_endgrid(0..{R}, 0..{C - 1}).")
    constraints.append("{ col_end(R, C) } :- col_endgrid(R, C).")

    for i, clue in clues.items():
        if len(clue) == 1 and clue[0] == 0:
            constraints.append(f":- grid(R, {i}), {color}(R, {i}).")
            constraints.append(f":- grid(R, {i}), col_start(R, {i}).")
            constraints.append(f":- col_endgrid(R, {i}), col_end(R, {i}).")
        else:
            constraints.append(f":- not col_start_count({R - 1}, {i}, {len(clue)}).")
            constraints.append(f":- not col_end_count({R}, {i}, {len(clue)}).")
            constraints.append(f"col_count_range({i}, 0..{len(clue)}).")
            for j, num in enumerate(clue):
                if num != "?":
                    constraints.append(
                        f":- grid(R, {i}), col_start(R, {i}), col_start_count(R, {i}, {j + 1}), not col_end(R + {num}, {i})."
                    )
                    constraints.append(
                        f":- grid(R, {i}), col_start(R, {i}), col_start_count(R, {i}, {j + 1}), not col_start_count(R + {num - 1}, {i}, {j + 1})."
                    )

    constraints.append(f":- grid(R, C), not {color}(R, C), col_start_count(R, C, N + 1), col_end_count(R, C, N).")
    constraints.append(f":- grid(R, C), {color}(R, C), col_start_count(R, C, N), col_end_count(R, C, N).")
    constraints.append("col_start_count(-1, C, 0) :- grid(_, C).")
    constraints.append(
        "col_start_count(R, C, N) :- grid(R, C), col_count_range(C, N), col_start(R, C), col_start_count(R - 1, C, N - 1)."
    )
    constraints.append(
        "col_start_count(R, C, N) :- grid(R, C), col_count_range(C, N), not col_start(R, C), col_start_count(R - 1, C, N)."
    )
    constraints.append("col_end_count(-1, C, 0) :- grid(_, C).")
    constraints.append(
        "col_end_count(R, C, N) :- col_endgrid(R, C), col_count_range(C, N), col_end(R, C), col_end_count(R - 1, C, N - 1)."
    )
    constraints.append(
        "col_end_count(R, C, N) :- col_endgrid(R, C), col_count_range(C, N), not col_end(R, C), col_end_count(R - 1, C, N)."
    )
    constraints.append(":- col_start_count(R, C, N1), col_end_count(R, C, N2), N1 > N2 + 1.")
    constraints.append(":- col_start_count(R, C, N1), col_end_count(R, C, N2), N1 < N2.")
    constraints.append(":- grid(R, C), col_end(R, C), col_start(R, C).")

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
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(nono_row(E.R, E.C, left_clues))
    solver.add_program_line(nono_col(E.R, E.C, top_clues))
    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
