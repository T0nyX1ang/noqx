"""The Nagare solver."""

from typing import List

from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import direction, display, fill_path, grid, shade_c
from noqx.rule.helper import validate_direction
from noqx.rule.loop import directed_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver

dict_dir = {"1": "l", "3": "u", "5": "r", "7": "d"}
rev_direction = {"l": "r", "r": "l", "u": "d", "d": "u"}


def nagare_wind(r: int, c: int, d: str, puzzle: Puzzle) -> str:
    if d in ("l", "r"):
        cols = range(0, c) if d == "l" else range(puzzle.col - 1, c, -1)

        c1, c2 = cols[0], cols[-1]
        for c_ in cols:
            if puzzle.symbol.get(Point(r, c_, Direction.CENTER)) or puzzle.surface.get(Point(r, c_)):
                c1 = c_ + cols.step
        if d == "r":
            c1, c2 = c2, c1
        return (
            f':- nagare({r}, C), {c1} <= C, C <= {c2}, not grid_out({r}, C, "{d}"), not grid_in({r}, C, "{rev_direction[d]}").'
        )

    if d in ("u", "d"):
        rows = range(0, r) if d == "u" else range(puzzle.row - 1, r, -1)

        r1, r2 = rows[0], rows[-1]
        for r_ in rows:
            if puzzle.symbol.get(Point(r_, c, Direction.CENTER)) or puzzle.surface.get(Point(r_, c)):
                r1 = r_ + rows.step
        if d == "d":
            r1, r2 = r2, r1
        return (
            f':- nagare(R, {c}), {r1} <= R, R <= {r2}, not grid_out(R, {c}, "{d}"), not grid_in(R, {c}, "{rev_direction[d]}").'
        )

    raise AssertionError("Invalid direction.")


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="nagare"))
    solver.add_program_line(fill_path(color="nagare", directed=True))
    solver.add_program_line(adjacent(_type="loop_directed"))
    solver.add_program_line(grid_color_connected(color="nagare", adj_type="loop_directed"))
    solver.add_program_line(directed_loop(color="nagare"))

    for (r, c, d, _), symbol_name in puzzle.symbol.items():
        validate_direction(r, c, d)
        shape, style = symbol_name.split("__")
        _d = dict_dir[style]

        if shape == "arrow_B_B":
            solver.add_program_line(f"nagare({r}, {c}).")
            solver.add_program_line(f'grid_in({r}, {c}, "{rev_direction[_d]}").')
            solver.add_program_line(f'grid_out({r}, {c}, "{_d}").')
        if shape == "arrow_B_W":
            solver.add_program_line(f"not nagare({r}, {c}).")
            solver.add_program_line(nagare_wind(r, c, _d, puzzle))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"not nagare({r}, {c}).")

    solver.add_program_line(display(item="grid_in", size=3))
    solver.add_program_line(display(item="grid_out", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Nagareru-Loop",
    "category": "loop",
    "aliases": ["nagareru"],
    "examples": [
        {
            "data": "m=edit&p=7VfLbutGDN37KwKtZ6F56bVLbpNu3PThFEEgGIbjKI1Rp7614zaQ4X/PkDyOjZpF20WLCzSwNcMhOZwzR0NKWv+6ma4643L6+8rkxqZfWVd8VdHyleN3M39ZdM2ZOd+8PC1XSTDm26sr8zhdrLtBC6/xYNvXTX9u+q+bNnOZwTU2/ffNtv+m6e9MP0qmzISkGybJZsYl8fIg3rKdpE+itHmSryEn8S6J09Vq+fvkYnIhnt81bX9jMlrogqeTmD0vf+symcfj2fL5fk6K++lL2s36af4ZlvXmYfnzBr52vDP9ueAd7vHSwsDrD3hJFLwkKXgJHOGdzVezRTcZSqB/CLd7+Kl71ZDW490uUf5DwjppWoL940GsDuKo2WaxzJpgssJyV8qoitLJqM6lq7izubjaXJxsXktvvfTOoZfZ1sHuJYz1sHv4e8Tx8A/wC4X0QGhLzCsxr4S9BK4S61SwV9BX0NeyjsvF7oDbWVnPOdmXc/ADfuckjgNOFzA/BOmj4HIlxsDlwKUDLlfBD+R64PC5zPPg01uM7X4scbyVON4JXg+8Hnx7h3ge+rDvMT9iHvD6AusUgteDJ1/DXsNew16LPeRiD+AtWFkn4P4H4A5WeAvAF8BnAJ/BIx5whohxgbgF5hWYV0Jfwh/nIIDngGMaahlH4ItW8EfgieAxMl8pC66bbWott3cpIyhea817LbnldM3oNrbxoJYSw8mheBOJmjcF8Sdqzqm2PInCOaTqKY6ipzOqoOHc0vwp1zR/uifH/nuclJPH29r705nX4lNuHu93r68o/ik9nIuKP+ekEp9zVNNTrVF4dpQbyr4c1aJjHt71f4i/19OZ1PwL2q+ip9qg4fwT3jjnFR64Bmh6qgmqnvar6el4anri+ZQ3rinKfecao+mptijnyleE85RPTzmr6LnWKDi5tijxudYoeLimKDyHQs9Hri1aHHqmKOeWa4+Gk545ynmIuX5+uCadxEl16Yqrk+P2Jj28Te+5/YrbnNvI7ZB9Lrm95fYTt4Hbgn1Kevz/zReE0wL5L8Fpo7xp/vUvfvh9+P3//MaDNhttVo/TWZde+ofzX7qz6+XqebpIo9HT9HOXpe+s3SB7zfhKZcSmz6mPT6///tOL6M+/tPr6pcFJFX88eAM=",
        }
    ],
}
