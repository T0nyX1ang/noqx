"""The Nagare solver."""

from typing import List

from .core.common import direction, display, fill_path, grid, shade_c
from .core.penpa import Puzzle
from .core.loop import directed_loop
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.solution import solver


dict_dir = {"1": "l", "3": "u", "5": "r", "7": "d"}
rev_direction = {"l": "r", "r": "l", "u": "d", "d": "u"}


def nagare_wind(r: int, c: int, d: str, puzzle: Puzzle) -> str:
    if d in ("l", "r"):
        cols = range(0, c) if d == "l" else range(puzzle.col - 1, c, -1)

        c1, c2 = cols[0], cols[-1]
        for c_ in cols:
            if puzzle.symbol.get((r, c_)) or puzzle.surface.get((r, c_)):
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
            if puzzle.symbol.get((r_, c)) or puzzle.surface.get((r_, c)):
                r1 = r_ + rows.step
        if d == "d":
            r1, r2 = r2, r1
        return (
            f':- nagare(R, {c}), {r1} <= R, R <= {r2}, not grid_out(R, {c}, "{d}"), not grid_in(R, {c}, "{rev_direction[d]}").'
        )

    raise AssertionError("Invalid direction.")


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="nagare"))
    solver.add_program_line(fill_path(color="nagare", directed=True))
    solver.add_program_line(adjacent(_type="loop_directed"))
    solver.add_program_line(grid_color_connected(color="nagare", adj_type="loop_directed"))
    solver.add_program_line(directed_loop(color="nagare"))

    for (r, c), symbol_name in puzzle.symbol.items():
        shape, style, _ = symbol_name.split("__")
        d = dict_dir[style]

        if shape == "arrow_B_B":
            solver.add_program_line(f"nagare({r}, {c}).")
            solver.add_program_line(f'grid_in({r}, {c}, "{rev_direction[d]}").')
            solver.add_program_line(f'grid_out({r}, {c}, "{d}").')
        elif shape == "arrow_B_W":
            solver.add_program_line(f"not nagare({r}, {c}).")
            solver.add_program_line(nagare_wind(r, c, d, puzzle))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"not nagare({r}, {c}).")

    solver.add_program_line(display(item="grid_in", size=3))
    solver.add_program_line(display(item="grid_out", size=3))
    solver.solve()

    return solver.solutions
