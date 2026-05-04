"""The Nonogram solver."""

from typing import Dict, List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, grid, shade_c


def nono_row(col: int, clues: Dict[int, Tuple[Union[int, str]]], color: str = "black"):
    """Generates the nonogram row constraints."""
    prefix = "row_count(R, C, N, V) :- grid(R, C), row_count_value_range(R, N, V)"
    constraints = []
    constraints.append("row_count(R, -1, -1, 0) :- grid(R, _).")
    constraints.append(f"{prefix}, not {color}(R, C), row_count(R, C - 1, N, _), V = 0.")
    constraints.append(f"{prefix}, {color}(R, C), not {color}(R, C - 1), row_count(R, C - 1, N - 1, _), V = 1.")
    constraints.append(f"{prefix}, {color}(R, C), {color}(R, C - 1), row_count(R, C - 1, N, V - 1).")

    for i, clue in clues.items():
        constraints.append(f"row_count_value_range({i}, -1, 0).")
        if len(clue) == 1 and clue[0] == 0:
            constraints.append(f":- grid({i}, C), not row_count({i}, C, -1, 0).")
        else:
            constraints.append(f":- not row_count({i}, {col - 1}, {len(clue) - 1}, _).")
            for j, num in enumerate(clue):
                if num != "?":
                    slope = f"row_count({i}, C, {j}, V), not {color}({i}, C + 1)"
                    constraints.append(f"row_count_value_range({i}, {j}, 0..{num}).")
                    constraints.append(f":- grid({i}, C), {color}({i}, C), {slope}, V != {num}.")
                else:
                    constraints.append(f"row_count_value_range({i}, {j}, 0..{col + 2 - 2 * len(clue)}).")

    return "\n".join(constraints)


def nono_col(row: int, clues: Dict[int, Tuple[Union[int, str]]], color: str = "black"):
    """Generates the nonogram column constraints."""
    prefix = "col_count(R, C, N, V) :- grid(R, C), col_count_value_range(C, N, V)"
    constraints = []
    constraints.append("col_count(-1, C, -1, 0) :- grid(_, C).")
    constraints.append(f"{prefix}, not {color}(R, C), col_count(R - 1, C, N, _), V = 0.")
    constraints.append(f"{prefix}, {color}(R, C), not {color}(R - 1, C), col_count(R - 1, C, N - 1, _), V = 1.")
    constraints.append(f"{prefix}, {color}(R, C), {color}(R - 1, C), col_count(R - 1, C, N, V - 1).")

    for i, clue in clues.items():
        constraints.append(f"col_count_value_range({i}, -1, 0).")
        if len(clue) == 1 and clue[0] == 0:
            constraints.append(f":- grid(R, {i}), not col_count(R, {i}, -1, 0).")
        else:
            constraints.append(f":- not col_count({row - 1}, {i}, {len(clue) - 1}, _).")
            for j, num in enumerate(clue):
                if num != "?":
                    slope = f"col_count(R, {i}, {j}, V), not {color}(R + 1, {i})"
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
            "data": "m=edit&p=7VVNT+MwEL3nV6A5zyG2kzbJZVU+updSWNoVQlFUpSGIalMF0gatXOW/M540BAwHOAAX5Pr19dljP4896ua+Tqsch9RUgC4Kasr1uA9c8+nafLUt8ugAR/X2tqyIIJ6Nx3iTFpvciRXNoJ44Ox1GeoT6dxSDAARJXUCC+k+006eRnqKe0RCgR9qknSSJnvT0kscNO2pF4RKf7jnRK6LZqsqKfDFplfMo1nMEs88hRxsK6/Ihh70P8zsr18uVEZbplg6zuV3d7Uc29XX5r4Zuiwb1qLU76+zK3q7q7aonu+ptu/Lz7YZJ01DaL8jwIoqN9789DXo6i3aN8bUDFZjQX+SlvRtQoSV4ri2ILjmdYIf4dohvh/jSCPKZYPvw7UWH9qKBay0a2LuEwgoJ5QuBciA4E1eMY0bJOKdEoVaMx4wuo8844TknjJeMR4we44DnDE2q33kZMKCzeHRGMizbm/kCb/GgLXKBwdvfiRPDrK5u0iyn1zat18u8OpiW1TotgMq7ceA/cKeaF1TFPxX/PRVvrsD9UN1//8uPKbv0/vQZwl29SBdZWQD9aSDr4mP68LX+5aelckqcRw==",
        },
        {
            "url": "https://puzz.link/p?nonogram/31/13/m513j1111i531q55k11111h5111p55k111j131q55k11k55k11k135j1l55k111j55r35k311j35r51k115j51zn3353133o11111111111k131113133m11111111111k11111111333zg3113313311l111111111111111g3331111133l111112121111j11111111111111x",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())

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

        self.add_program_line(nono_row(puzzle.col, left_clues))
        self.add_program_line(nono_col(puzzle.row, top_clues))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
