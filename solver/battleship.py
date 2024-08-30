"""The Battleship solver."""

from typing import List

from .core.common import count, display, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.shape import OMINOES, all_shapes, count_shape, general_shape
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))

    fleet_name = ""
    for (r, c), symbol_name in puzzle.symbol.items():
        shape, style, _ = symbol_name.split("__")
        assert shape.startswith("battleship"), "Invalid battleship shape."
        assert fleet_name in ("", shape), "Multiple fleet shapes are not allowed."

        fleet_name = shape
        if style not in ("7", "8"):
            solver.add_program_line(f"{fleet_name}({r}, {c}).")
        else:
            solver.add_program_line(f"not {fleet_name}({r}, {c}).")

        if style == "1":
            solver.add_program_line(f":- grid({r + 1}, {c}), {fleet_name}({r + 1}, {c}).")
            solver.add_program_line(f":- grid({r - 1}, {c}), {fleet_name}({r - 1}, {c}).")
            solver.add_program_line(f":- grid({r}, {c + 1}), {fleet_name}({r}, {c + 1}).")
            solver.add_program_line(f":- grid({r}, {c - 1}), {fleet_name}({r}, {c - 1}).")

        if style == "2":
            assert 0 < c < puzzle.col - 1 and 0 < r < puzzle.row - 1, "Ship is outside of the board."
            solver.add_program_line(f":- #count {{ R, C: {fleet_name}(R, C), adj_4({r}, {c}, R, C) }} != 2.")

        if style == "3":
            assert c < puzzle.col - 1, "Ship is outside of the board."
            solver.add_program_line(f":- grid({r}, {c - 1}), {fleet_name}({r}, {c - 1}).")
            solver.add_program_line(f":- grid({r}, {c + 1}), not {fleet_name}({r}, {c + 1}).")

        if style == "4":
            assert r < puzzle.row - 1, "Ship is outside of the board."
            solver.add_program_line(f":- grid({r - 1}, {c}), {fleet_name}({r - 1}, {c}).")
            solver.add_program_line(f":- grid({r + 1}, {c}), not {fleet_name}({r + 1}, {c}).")

        if style == "5":
            assert c > 0, "Ship is outside of the board."
            solver.add_program_line(f":- grid({r}, {c + 1}), {fleet_name}({r}, {c + 1}).")
            solver.add_program_line(f":- grid({r}, {c - 1}), not {fleet_name}({r}, {c - 1}).")

        if style == "6":
            assert r > 0, "Ship is outside of the board."
            solver.add_program_line(f":- grid({r + 1}, {c}), {fleet_name}({r + 1}, {c}).")
            solver.add_program_line(f":- grid({r - 1}, {c}), not {fleet_name}({r - 1}, {c}).")

    solver.add_program_line(shade_c(color=fleet_name))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="x"))
    solver.add_program_line(avoid_adjacent_color(color=fleet_name, adj_type="x"))
    solver.add_program_line(general_shape("battleship", 1, OMINOES[1]["."], color=fleet_name, adj_type=4))
    solver.add_program_line(general_shape("battleship", 2, OMINOES[2]["I"], color=fleet_name, adj_type=4))
    solver.add_program_line(general_shape("battleship", 3, OMINOES[3]["I"], color=fleet_name, adj_type=4))
    solver.add_program_line(general_shape("battleship", 4, OMINOES[4]["I"], color=fleet_name, adj_type=4))
    solver.add_program_line(all_shapes("battleship", color=fleet_name))
    solver.add_program_line(count_shape(4, "battleship", 1, color=fleet_name))
    solver.add_program_line(count_shape(3, "battleship", 2, color=fleet_name))
    solver.add_program_line(count_shape(2, "battleship", 3, color=fleet_name))
    solver.add_program_line(count_shape(1, "battleship", 4, color=fleet_name))

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top number
        assert isinstance(num, int), "TOP style must be an integer."
        solver.add_program_line(count(num, color=fleet_name, _type="col", _id=c))

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left number
        assert isinstance(num, int), "LEFT style must be an integer."
        solver.add_program_line(count(num, color=fleet_name, _type="row", _id=r))

    solver.add_program_line(display(item=fleet_name))
    solver.solve()

    return solver.solutions
