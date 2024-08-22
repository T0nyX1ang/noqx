"""The Nonogram solver."""

from typing import Dict, List, Tuple, Union

from .core.common import display, shade_c
from .core.penpa import Puzzle
from .core.solution import solver


def nono_row(col: int, clues: Dict[int, Tuple[Union[int, str]]], color: str = "black"):
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
            constraints.append(f":- not row_count({i}, {col - 1}, {len(clue) - 1}, _).")
            for j, num in enumerate(clue):
                if num != "?":
                    slope = f"row_count({i}, C, {j}, V), row_count({i}, C + 1, {j}, 0)"
                    constraints.append(f"row_count_value_range({i}, {j}, 0..{num}).")
                    constraints.append(f":- grid({i}, C), {color}({i}, C), {slope} , V != {num}.")
                else:
                    constraints.append(f"row_count_value_range({i}, {j}, 0..{col + 2 - 2 * len(clue)}).")

    return "\n".join(constraints)


def nono_col(row: int, clues: Dict[int, Tuple[Union[int, str]]], color: str = "black"):
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
            constraints.append(f":- not col_count({row}, {i}, {len(clue) - 1}, 0).")
            for j, num in enumerate(clue):
                if num != "?":
                    slope = f"col_count(R, {i}, {j}, V), col_count(R + 1, {i}, {j}, 0)"
                    constraints.append(f"col_count_value_range({i}, {j}, 0..{num}).")
                    constraints.append(f":- grid(R, {i}), {color}(R, {i}), {slope}, V != {num}.")
                else:
                    constraints.append(f"col_count_value_range({i}, {j}, 0..{row + 2 - 2 * len(clue)}).")

    return "\n".join(constraints)


def solve(puzzle: Puzzle) -> List[str]:
    top_clues = {}
    for c in range(puzzle.col):
        top_clues[c] = tuple(clue for (r1, c1), clue in puzzle.text.items() if r1 <= -1 and c1 == c)

    left_clues = {}
    for r in range(puzzle.row):
        left_clues[r] = tuple(clue for (r1, c1), clue in puzzle.text.items() if r1 == r and c1 <= -1)

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(f"grid(-1..{puzzle.row}, -1..{puzzle.col}).")
    solver.add_program_line(shade_c())
    solver.add_program_line(f"not black(-1, -1..{puzzle.col}).")
    solver.add_program_line(f"not black(-1..{puzzle.row}, -1).")
    solver.add_program_line(f"not black({puzzle.row}, -1..{puzzle.col}).")
    solver.add_program_line(f"not black(-1..{puzzle.row}, {puzzle.col}).")
    solver.add_program_line(nono_row(puzzle.col, left_clues))
    solver.add_program_line(nono_col(puzzle.row, top_clues))
    solver.add_program_line(display())

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    solver.solve()

    return solver.solutions
