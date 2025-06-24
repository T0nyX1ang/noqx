"""The Nonogram solver."""

from typing import Dict, List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, shade_c


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


class NonogramSolver(Solver):
    """The Nonogram solver."""

    name = "Nonogram"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VU9b9swEN31K4KbbxD1YUtcCteNu7hKW7sIAkEwZFVBjMpQKltFQUP/PXcnKQ7YDM3QZCloPj8/8sjHIw8+/GzzpsQpNT9CFxU13w2kT1z+jG29O1alvsBZe7yrGyKIV4sF3ubVoXRSn2ZQz5yTibWZofmoU1CA4FFXkKH5ok/mkzYJmhUNAQakLftJHtHLM72WcWbzXlQu8WTgRG+IFrumqMrNslc+69SsEXif9xLNFPb1rxIGH/y7qPfbHQvb/EiHOdzt7oeRQ/u9/tEOc1XWoZn1dlejXbYz2PXPdpn2dpk9Y5fD/rHdOOs6SvtXMrzRKXv/dqbRma70iTDRJ/AjDn1HXvq7AT+2hMC1BTUmZxTskNAOCe2Q0GOBHsSjYPsI7UWn9qKRCE8WjexdYhGehMSy7aNAOVCSiRvBhaAnuKZEofEFPwi6gqHgUuZcCl4LzgUDwYnMmXKq//IyYEJnCeiMZNjrb+YVvKVU0lzkCqPnvzMnhVXb3OZFSa8taffbsrlI6mafV0Dl3TnwG6RTzSuq4v8V/zYVz1fgvqju3/7lp5Rden/mCuG+3eSboq6A/jRQdPUyffqn/uqnpXLKnAc=",
        },
        {
            "url": "https://puzz.link/p?nonogram/31/13/m513j1111i531q55k11111h5111p55k111j131q55k11k55k11k135j1l55k111j55r35k311j35r51k115j51zn3353133o11111111111k131113133m11111111111k11111111333zg3113313311l111111111111111g3331111133l111112121111j11111111111111x",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        top_clues = {}
        for c in range(puzzle.col):
            r1 = -1
            clue: List[Union[int, str]] = []
            while (r1, c, Direction.CENTER, "normal") in puzzle.text:
                clue.append(puzzle.text[Point(r1, c, Direction.CENTER, "normal")])
                r1 -= 1
            top_clues[c] = tuple(reversed(clue))

        left_clues = {}
        for r in range(puzzle.row):
            c1 = -1
            clue: List[Union[int, str]] = []
            while (r, c1, Direction.CENTER, "normal") in puzzle.text:
                clue.append(puzzle.text[Point(r, c1, Direction.CENTER, "normal")])
                c1 -= 1
            left_clues[r] = tuple(reversed(clue))

        self.add_program_line(f"grid(-1..{puzzle.row}, -1..{puzzle.col}).")
        self.add_program_line(shade_c())
        self.add_program_line(f"not black(-1, -1..{puzzle.col}).")
        self.add_program_line(f"not black(-1..{puzzle.row}, -1).")
        self.add_program_line(f"not black({puzzle.row}, -1..{puzzle.col}).")
        self.add_program_line(f"not black(-1..{puzzle.row}, {puzzle.col}).")
        self.add_program_line(nono_row(puzzle.col, left_clues))
        self.add_program_line(nono_col(puzzle.row, top_clues))

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"black({r}, {c}).")
            else:
                self.add_program_line(f"not black({r}, {c}).")

        self.add_program_line(display())

        return self.program
