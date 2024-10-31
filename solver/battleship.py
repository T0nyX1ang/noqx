"""The Battleship solver."""

from typing import List

from .core.common import count, display, grid, shade_c
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.penpa import Puzzle, Solution
from .core.shape import OMINOES, all_shapes, count_shape, general_shape
from .core.solution import solver


def battleship_refine(solution: Solution) -> Solution:
    """Refine the battleship solution."""
    for (r, c), _ in solution.symbol.items():
        has_top_neighbor = (r - 1, c) in solution.symbol
        has_left_neighbor = (r, c - 1) in solution.symbol
        has_bottom_neighbor = (r + 1, c) in solution.symbol
        has_right_neighbor = (r, c + 1) in solution.symbol

        fleet_name = solution.symbol[(r, c)].split("__")[0]

        # center part
        if {has_top_neighbor, has_bottom_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
            solution.symbol[(r, c)] = f"{fleet_name}__1__0"

        # middle part
        elif (has_top_neighbor and has_bottom_neighbor) or (has_left_neighbor and has_right_neighbor):
            solution.symbol[(r, c)] = f"{fleet_name}__2__0"

        # left part
        elif {has_top_neighbor, has_bottom_neighbor, has_left_neighbor} == {False}:
            solution.symbol[(r, c)] = f"{fleet_name}__3__0"

        # top part
        elif {has_top_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
            solution.symbol[(r, c)] = f"{fleet_name}__4__0"

        # right part
        elif {has_top_neighbor, has_bottom_neighbor, has_right_neighbor} == {False}:
            solution.symbol[(r, c)] = f"{fleet_name}__5__0"

        # bottom part
        elif {has_bottom_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
            solution.symbol[(r, c)] = f"{fleet_name}__6__0"

    return solution


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))

    fleet_name = "battleship_B"  # set a default battleship fleet name
    for (r, c), symbol_name in puzzle.symbol.items():
        shape, style, _ = symbol_name.split("__")
        assert shape.startswith("battleship"), f"Invalid battleship shape: {shape}."
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

    for solution in solver.solutions:
        battleship_refine(solution)

    return solver.solutions


__metadata__ = {
    "name": "Battleship",
    "category": "var",
    "examples": [
        {
            "data": "m=edit&p=7VRLb9NAEL77V1R7nsOOX7H3lpaGSzGPBFWRZVUOGCUikUsSI7RR/ntnxm69uL5wAIqEnB19+eax384+Dt+acl8BIv+CBDQQgjCKZSD6MnT3LTbHbWUuYNoc1/WeAMDb2Qy+lNtD5eUo2brwTjY1dgr2tckVKlA+DVQF2PfmZN8Ym4Gdk0sBEnfTBvkEr3t4K35GVy2JmnDWYYJLgqvySHoO68393WXLvjO5XYDiuS6lAkO1q79XqtPC/z/Vu9WGib5A5zk0n+uvTReLxRnstJW8HJEc9JIZtpIZjUjmlfwByWlxPlP7P5DoO5Oz/o89THo4NyeymTmpIODUgLS0e6SC8HH5j0TEBO3hExEPiQkT2iESJkKHSAcpoR7MEuJAR+gPU2QWp2g8jJhIhFM0lQhHGGoJcXLQlxinLLbLccpgNJwJ42cxicQ8LYDai9LkJTU55o7F8Hz3VcLtH/Wg5p4Foy7Jmoy6Uu7jiIuUzESPL3ZB5wBsIPaVWC02EnsjMddib8VeiQ3FxhIz4ZP0S2fNbclvkpOHiTxgP3/0kP1rXOHlKmt2q2p/kdX7Xbml2z5fl/eVouf17KkfSgadD3qt/7+4f/nF5a3QL+0uvDQ5dDsL7wE=",
        }
    ],
}
