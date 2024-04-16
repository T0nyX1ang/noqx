"""The Battleship solver."""

from typing import List

from . import utilsx
from .utilsx.common import count, display, grid, shade_c
from .utilsx.encoding import Encoding
from .utilsx.rule import adjacent, avoid_adjacent
from .utilsx.shape import OMINOES, all_shapes, count_shape, general_shape
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="x"))
    solver.add_program_line(avoid_adjacent(adj_type="x"))
    solver.add_program_line(general_shape("battleship", 1, OMINOES[1]["."], adj_type=4))
    solver.add_program_line(general_shape("battleship", 2, OMINOES[2]["I"], adj_type=4))
    solver.add_program_line(general_shape("battleship", 3, OMINOES[3]["I"], adj_type=4))
    solver.add_program_line(general_shape("battleship", 4, OMINOES[4]["I"], adj_type=4))
    solver.add_program_line(all_shapes("battleship"))
    solver.add_program_line(count_shape(4, "battleship", 1))
    solver.add_program_line(count_shape(3, "battleship", 2))
    solver.add_program_line(count_shape(2, "battleship", 3))
    solver.add_program_line(count_shape(1, "battleship", 4))

    for c, num in E.top.items():
        solver.add_program_line(count(int(num), _type="col", _id=c))

    for r, num in E.left.items():
        solver.add_program_line(count(int(num), _type="row", _id=r))

    for (r, c), clue in E.clues.items():
        if clue in "odlrum":
            solver.add_program_line(f"black({r}, {c}).")

        if clue == "o":
            solver.add_program_line(f":- grid({r + 1}, {c}), black({r + 1}, {c}).")
            solver.add_program_line(f":- grid({r - 1}, {c}), black({r - 1}, {c}).")
            solver.add_program_line(f":- grid({r}, {c + 1}), black({r}, {c + 1}).")
            solver.add_program_line(f":- grid({r}, {c - 1}), black({r}, {c - 1}).")

        if clue == "l":
            assert c > 0, "Ship is outside of the board."
            solver.add_program_line(f":- grid({r}, {c + 1}), black({r}, {c + 1}).")
            solver.add_program_line(f":- grid({r}, {c - 1}), not black({r}, {c - 1}).")

        if clue == "r":
            assert c < E.C - 1, "Ship is outside of the board."
            solver.add_program_line(f":- grid({r}, {c - 1}), black({r}, {c - 1}).")
            solver.add_program_line(f":- grid({r}, {c + 1}), not black({r}, {c + 1}).")

        if clue == "u":
            assert r > 0, "Ship is outside of the board."
            solver.add_program_line(f":- grid({r + 1}, {c}), black({r + 1}, {c}).")
            solver.add_program_line(f":- grid({r - 1}, {c}), not black({r - 1}, {c}).")

        if clue == "d":
            assert r < E.R - 1, "Ship is outside of the board."
            solver.add_program_line(f":- grid({r - 1}, {c}), black({r - 1}, {c}).")
            solver.add_program_line(f":- grid({r + 1}, {c}), not black({r + 1}, {c}).")

        if clue == "m":
            assert 0 < c < E.C - 1 and 0 < r < E.R - 1, "Ship is outside of the board."
            solver.add_program_line(f":- #count {{ R, C: black(R, C), adj_4({r}, {c}, R, C) }} != 2.")

        if clue == "w":
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display())
    solver.solve()

    for solution in solver.solutions:
        keys = list(solution.keys())
        for rc in keys:
            r, c = map(int, rc.split(","))
            has_top_neighbor = f"{r - 2},{c}" in keys
            has_left_neighbor = f"{r},{c - 2}" in keys
            has_bottom_neighbor = f"{r + 2},{c}" in keys
            has_right_neighbor = f"{r},{c + 2}" in keys

            if {has_top_neighbor, has_bottom_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
                solution[rc] = "large_black_circle.png"
            # middle part
            elif (has_top_neighbor and has_bottom_neighbor) or (has_left_neighbor and has_right_neighbor):
                solution[rc] = "black.png"
            # top part
            elif {has_top_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
                solution[rc] = "battleship_top_end.png"
            # bottom part
            elif {has_bottom_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
                solution[rc] = "battleship_bottom_end.png"
            # left part
            elif {has_top_neighbor, has_bottom_neighbor, has_left_neighbor} == {False}:
                solution[rc] = "battleship_left_end.png"
            # right part
            elif {has_top_neighbor, has_bottom_neighbor, has_right_neighbor} == {False}:
                solution[rc] = "battleship_right_end.png"

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
