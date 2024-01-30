"""The Nonogram solver."""

from typing import List, Union

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import shade_c
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s, outside_clues="1001")


def nono(tag: str, R: int, C: int, clues: list[list[Union[int, str]]], color: str = "black"):
    # Take care that start and end is left-close-right-open.
    assert tag in ["row", "col"]
    init = f"{{ {tag}_start(R, C) }} :- grid(R, C).\n"
    init += f"{{ {tag}_end(R, C) }} :- 0 <= R, R < {R + (tag=='col')}, 0 <= C, C < {C + (tag=='row')}."
    constraints = [init]
    for i, clue in clues.items():
        cell_str = f"{i}, C" if tag == "row" else f"R, {i}"
        end_cond = f"0 <= C, C < {C+1}" if tag == "row" else f"0 <= R, R < {R+1}"
        if len(clue) == 1 and clue[0] == 0:
            constraint_i = f":- grid({cell_str}), {color}({cell_str}).\n"
            constraint_i += f":- grid({cell_str}), {tag}_start({cell_str}).\n"
            constraint_i += f":- {end_cond}, {tag}_end({cell_str})."
        else:
            cell_var = "C" if tag == "row" else "R"
            constraint_i = f":- #count{{ {cell_var}: {tag}_start({cell_str}), grid({cell_str}) }} != {len(clue)}."
            constraint_i += f"\n:- #count{{ {cell_var}: {tag}_end({cell_str}), {end_cond} }} != {len(clue)}."
            for j, num in enumerate(clue):
                if num != "?":
                    cell_end = f"{i}, C+{num}" if tag == "row" else f"R+{num}, {i}"
                    cell_end_2 = f"{i}, C+{num-1}" if tag == "row" else f"R+{num-1}, {i}"
                    constraint_i += f"\n:- grid({cell_str}), {tag}_start({cell_str}), {tag}_start_count({cell_str}, {j+1}), not {tag}_end({cell_end})."
                    constraint_i += f"\n:- grid({cell_str}), {tag}_start({cell_str}), {tag}_start_count({cell_str}, {j+1}), not {tag}_start_count({cell_end_2}, {j+1})."
            constraint_i += f"\n:- not {color}({cell_str}), 0<=N, N<={len(clue)}, {tag}_start_count({cell_str}, N + 1), {tag}_end_count({cell_str}, N)."
            constraint_i += f"\n:- {color}({cell_str}), 0<=N, N<={len(clue)}, {tag}_start_count({cell_str}, N), {tag}_end_count({cell_str}, N)."
        constraints.append(constraint_i)

    if tag == "row":
        constraint = f"{tag}_start_count(R, C, N) :- grid(R, C), #count{{ C1: {tag}_start(R, C1), grid(R, C1), C1 <= C }} = N.\n"
        constraint += f"{tag}_end_count(R, C, N) :- grid(R, C), #count{{ C1: {tag}_end(R, C1), grid(R, C1), C1 <= C }} = N.\n"
    else:
        constraint = f"{tag}_start_count(R, C, N) :- grid(R, C), #count{{ R1: {tag}_start(R1, C), grid(R1, C), R1 <= R }} = N.\n"
        constraint += f"{tag}_end_count(R, C, N) :- grid(R, C), #count{{ R1: {tag}_end(R1, C), grid(R1, C), R1 <= R }} = N.\n"
    constraint += f":- {tag}_start_count(R, C, N1), {tag}_end_count(R, C, N2), N1 > N2 + 1.\n"
    constraint += f":- {tag}_start_count(R, C, N1), {tag}_end_count(R, C, N2), N1 < N2.\n"
    constraint += f":- grid(R, C), {tag}_end(R, C), {tag}_start(R, C)."
    constraints.append(constraint)
    
    return "\n".join(constraints)


def solve(E: Encoding) -> List:
    if len(E.top) + len(E.left) == 0:
        raise ValueError("No clues provided.")

    top_clues = {}
    for c in E.top:
        top_clues[c] = [int(clue) if clue != "?" else "?" for clue in E.top[c].split()]

    left_clues = {}
    for r in E.left:
        left_clues[r] = [int(clue) if clue != "?" else "?" for clue in E.left[r].split()]

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())

    solver.add_program_line(nono("row", E.R, E.C, left_clues))
    solver.add_program_line(nono("col", E.R, E.C, top_clues))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
