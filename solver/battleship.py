"""The Battleship solver."""

from typing import List

from noqx.puzzle import Point, Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))

    fleet_name = "battleship_B"  # set a default battleship fleet name
    for (r, c, d, _), symbol_name in puzzle.symbol.items():
        shape, style = symbol_name.split("__")
        validate_direction(r, c, d)
        fail_false(shape.startswith("battleship"), f"Invalid battleship shape: {shape}.")
        fail_false(fleet_name in ("", shape), "Multiple fleet shapes are not allowed.")

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
            fail_false(0 < c < puzzle.col - 1 and 0 < r < puzzle.row - 1, f"Ship at ({r}, {c}) is outside of the board.")
            solver.add_program_line(f":- #count {{ R, C: {fleet_name}(R, C), adj_4({r}, {c}, R, C) }} != 2.")

        if style == "3":
            fail_false(c < puzzle.col - 1, f"Ship at ({r}, {c}) is outside of the board.")
            solver.add_program_line(f":- grid({r}, {c - 1}), {fleet_name}({r}, {c - 1}).")
            solver.add_program_line(f":- grid({r}, {c + 1}), not {fleet_name}({r}, {c + 1}).")

        if style == "4":
            fail_false(r < puzzle.row - 1, f"Ship at ({r}, {c}) is outside of the board.")
            solver.add_program_line(f":- grid({r - 1}, {c}), {fleet_name}({r - 1}, {c}).")
            solver.add_program_line(f":- grid({r + 1}, {c}), not {fleet_name}({r + 1}, {c}).")

        if style == "5":
            fail_false(c > 0, f"Ship at ({r}, {c}) is outside of the board.")
            solver.add_program_line(f":- grid({r}, {c + 1}), {fleet_name}({r}, {c + 1}).")
            solver.add_program_line(f":- grid({r}, {c - 1}), not {fleet_name}({r}, {c - 1}).")

        if style == "6":
            fail_false(r > 0, f"Ship at ({r}, {c}) is outside of the board.")
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

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")

        if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
            solver.add_program_line(count(num, color=fleet_name, _type="col", _id=c))

        if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
            solver.add_program_line(count(num, color=fleet_name, _type="row", _id=r))

    solver.add_program_line(display(item=fleet_name))
    solver.solve()

    return solver.solutions


def refine(solution: Puzzle) -> Puzzle:
    """Refine the solution."""
    for (r, c, d, pos), _ in solution.symbol.items():
        has_top_neighbor = (r - 1, c, d, pos) in solution.symbol
        has_left_neighbor = (r, c - 1, d, pos) in solution.symbol
        has_bottom_neighbor = (r + 1, c, d, pos) in solution.symbol
        has_right_neighbor = (r, c + 1, d, pos) in solution.symbol

        fleet_name = solution.symbol[Point(r, c, d, pos)].split("__")[0]

        # center part
        if {has_top_neighbor, has_bottom_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
            solution.symbol[Point(r, c, d, pos)] = f"{fleet_name}__1"

        # middle part
        elif (has_top_neighbor and has_bottom_neighbor) or (has_left_neighbor and has_right_neighbor):
            solution.symbol[Point(r, c, d, pos)] = f"{fleet_name}__2"

        # left part
        if {has_top_neighbor, has_bottom_neighbor, has_left_neighbor, not has_right_neighbor} == {False}:
            solution.symbol[Point(r, c, d, pos)] = f"{fleet_name}__3"

        # top part
        if {has_top_neighbor, has_left_neighbor, has_right_neighbor, not has_bottom_neighbor} == {False}:
            solution.symbol[Point(r, c, d, pos)] = f"{fleet_name}__4"

        # right part
        if {has_top_neighbor, has_bottom_neighbor, has_right_neighbor, not has_left_neighbor} == {False}:
            solution.symbol[Point(r, c, d, pos)] = f"{fleet_name}__5"

        # bottom part
        if {has_bottom_neighbor, has_left_neighbor, has_right_neighbor, not has_top_neighbor} == {False}:
            solution.symbol[Point(r, c, d, pos)] = f"{fleet_name}__6"

    return solution


__metadata__ = {
    "name": "Battleship",
    "category": "var",
    "examples": [
        {
            "data": "m=edit&p=7VTPb9s8DL37ryh05kH0r9i+DGnX7NK525KhCAwjcDp/SLAEzpJ4GBTkfy9Ju7XmGhh6WPcNGBwRL4+U9EhJPHyri30JiPzzItBACPwglIHoytDtN1sfN2VyAeP6uKr2BABuJxP4r9gcSidDma1z52TixIzBvEsyhQqUSwNVDuZjcjLvE5OCmZJLARJ30wS5BK87eCd+RlcNiZpw2mKCc4LL4kh6Dqv1bnHZsB+SzMxA8V6XsgJDta2+l6rVwv/vq+1yzUS3QOs51F+qr3Ubi/kZzLiRPB+Q7HWSGTaSGQ1I5kxeQXKcn89U/k8kepFkrP9zB6MOTpMT2TQ5Kc/jqW9IS3NGyvMf038kAiboDJ+IsE+MmNAWETHhW0Tcm+Lr3i4+MuFZhNufIrtYSsN+xEgirEVjibCEoZYQaw66EmNpxSYdaxkM+jth+CwmkpinBKi8KEWeU5EDjg7g+emrkGsZDnlQc828QZfLLnfQJaX3B10RH/Vo0BVz9Ul430X6J5KFK3ZGtweMJ/atWC02EHsjMddi78ReifXFhhIz4vv3ohtqF/I3ycn8SNrezx+1v7+Ny51MpfV2We4v0mq/LTbUI6arYlcqaspnR/1QMuhWUY//16f/cJ/mo9D/t7fwCzkZVZhei7kFtasXxeK+ojtG9Xsh/+pZ0SPPnQc=",
        }
    ],
}
