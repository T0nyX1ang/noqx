"""The Nonogram solver."""

from typing import Dict, Tuple, Union

from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, shade_c
from noqx.solution import solver


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


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    top_clues = {}
    for c in range(puzzle.col):
        top_clues[c] = tuple(
            clue
            for (r1, c1, d1, pos1), clue in puzzle.text.items()
            if r1 <= -1 and c1 == c and d1 == Direction.CENTER and pos1 == "normal"
        )

    left_clues = {}
    for r in range(puzzle.row):
        left_clues[r] = tuple(
            clue
            for (r1, c1, d1, pos1), clue in puzzle.text.items()
            if r1 == r and c1 <= -1 and d1 == Direction.CENTER and pos1 == "normal"
        )

    solver.add_program_line(f"grid(-1..{puzzle.row}, -1..{puzzle.col}).")
    solver.add_program_line(shade_c())
    solver.add_program_line(f"not black(-1, -1..{puzzle.col}).")
    solver.add_program_line(f"not black(-1..{puzzle.row}, -1).")
    solver.add_program_line(f"not black({puzzle.row}, -1..{puzzle.col}).")
    solver.add_program_line(f"not black(-1..{puzzle.row}, {puzzle.col}).")
    solver.add_program_line(nono_row(puzzle.col, left_clues))
    solver.add_program_line(nono_col(puzzle.row, top_clues))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")
        else:
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display())

    return solver.program


__metadata__ = {
    "name": "Nonogram",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VU9b9swEN31K4KbbxD1YUtcCteNu7hKW7sIAkEwZFVBjMpQKltFQUP/PXcnKQ7YDM3QZCloPj8/8sjHIw8+/GzzpsQpNT9CFxU13w2kT1z+jG29O1alvsBZe7yrGyKIV4sF3ubVoXRSn2ZQz5yTibWZofmoU1CA4FFXkKH5ok/mkzYJmhUNAQakLftJHtHLM72WcWbzXlQu8WTgRG+IFrumqMrNslc+69SsEXif9xLNFPb1rxIGH/y7qPfbHQvb/EiHOdzt7oeRQ/u9/tEOc1XWoZn1dlejXbYz2PXPdpn2dpk9Y5fD/rHdOOs6SvtXMrzRKXv/dqbRma70iTDRJ/AjDn1HXvq7AT+2hMC1BTUmZxTskNAOCe2Q0GOBHsSjYPsI7UWn9qKRCE8WjexdYhGehMSy7aNAOVCSiRvBhaAnuKZEofEFPwi6gqHgUuZcCl4LzgUDwYnMmXKq//IyYEJnCeiMZNjrb+YVvKVU0lzkCqPnvzMnhVXb3OZFSa8taffbsrlI6mafV0Dl3TnwG6RTzSuq4v8V/zYVz1fgvqju3/7lp5Rden/mCuG+3eSboq6A/jRQdPUyffqn/uqnpXLKnAc=",
        },
        {
            "url": "https://puzz.link/p?nonogram/31/13/m513j1111i531q55k11111h5111p55k111j131q55k11k55k11k135j1l55k111j55r35k311j35r51k115j51zn3353133o11111111111k131113133m11111111111k11111111333zg3113313311l111111111111111g3331111133l111112121111j11111111111111x",
            "test": False,
        },
    ],
}
