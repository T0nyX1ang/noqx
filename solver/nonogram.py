"""The Nonogram solver."""

from typing import Dict, List, Tuple, Union

from .core.common import display, shade_c
from .core.penpa import Puzzle, Solution
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


def solve(puzzle: Puzzle) -> List[Solution]:
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


__metadata__ = {
    "name": "Nonogram",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7ZRBb5swFMfv+RSVzz5ASBriy9R1zS5dti6ZqgqhyEncBhXizsA6EeW7970HaWLDDjts62EivDx+fvb7Y/iTfy+lUXwERxByj/twBN6AznMPf4djnhSpEmf8oiw22kDC+efJhN/LNFe9KIAKOOPerhqL6oZXH0XEfMZZH06fxby6Ebvqk6imvJrBEOMBsOu6qA/p1TG9pXHMLmvoe5BPmxzSO0hXiVmlanFdky8iquacYZ/3NBtTlukfijU68Hqls2WCYCkLuJl8kzw1I3m51o9lU+vHe15d1HJnB7nYpZGLyhu5mNZyMeuQi3fxh+WO4/0etv0rCF6ICLV/O6bhMZ2JHcSp2LEgxKnvQEv9bFgwdsDAc4F/2JwDcKcM3SlDd8qwjwBeiFfg6hi6i47cRUMCJ4uGbpcxgZMpY2r7CmAPfNqJO4oTin2Kc9goXgUUP1D0KA4pXlPNFcVbipcUBxTPqWaEW/1bD+MvyInAxehrn4fd/3EvYrPS3MuVghdsWmZLZc6m2mQyZeBolut0kTfjggwPryCwLVVaKNX6KU22dl3ysNVGdQ4hVOuHrvqlNmtn9WeZphaoP18Wqp1mocKAjU6upTH62SKZLDYWOLGctZLaFraAQtoS5aN0umXHe9732E9GJ3wwfT74/7n8R59LfATeW/PpW5NDb682ndYH3OF+oJ0ub3jL6MBblsaGbVcD7TA2UNfbgNr2BthyOLBfmBxXdX2OqlyrY6uW27HVqeGjuPcC",
        },
        {
            "url": "https://puzz.link/p?nonogram/31/13/m513j1111i531q55k11111h5111p55k111j131q55k11k55k11k135j1l55k111j55r35k311j35r51k115j51zn3353133o11111111111k131113133m11111111111k11111111333zg3113313311l111111111111111g3331111133l111112121111j11111111111111x",
            "test": False,
        },
    ],
}
