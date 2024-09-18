"""The Yin-Yang solver."""

from typing import List, Tuple

from .core.common import display, grid, shade_c
from .core.helper import extract_two_symbols, tag_encode
from .core.penpa import Puzzle, Solution
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def exclude_border_color_changes(rows: int, cols: int, symbol_1: str, symbol_2: str) -> str:
    """Exclude border color changes more than twice."""
    rule = ""
    tag = tag_encode("changed", symbol_1, symbol_2)

    for r in range(rows - 1):
        rev_r = rows - 1 - r
        rule += f"{tag}({r}, 0) :- {symbol_1}({r}, 0), {symbol_2}({r + 1}, 0).\n"
        rule += f"{tag}({rev_r}, {cols - 1}) :- {symbol_1}({rev_r}, {cols - 1}), {symbol_2}({rev_r - 1}, {cols - 1}).\n"

    for c in range(cols - 1):
        rev_c = cols - 1 - c
        rule += f"{tag}(0, {c}) :- {symbol_1}(0, {c}), {symbol_2}(0, {c + 1}).\n"
        rule += f"{tag}({rows - 1}, {rev_c}) :- {symbol_1}({rows - 1}, {rev_c}), {symbol_2}({rows - 1}, {rev_c - 1}).\n"

    rule += f":- {{ {tag}(R, C) }} > 2.\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    symbol_set = set(puzzle.symbol.values())
    symbol_1, symbol_2 = extract_two_symbols(symbol_set)

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color=symbol_1))
    solver.add_program_line(f"{symbol_2}(R, C) :- grid(R, C), not {symbol_1}(R, C).")
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_rect(2, 2, color=symbol_1))
    solver.add_program_line(avoid_rect(2, 2, color=f"not {symbol_1}"))

    # exclude checkerboard shape
    solver.add_program_line(f":- {symbol_1}(R, C), {symbol_2}(R, C + 1), {symbol_2}(R + 1, C), {symbol_1}(R + 1, C + 1).")
    solver.add_program_line(f":- {symbol_2}(R, C), {symbol_1}(R, C + 1), {symbol_1}(R + 1, C), {symbol_2}(R + 1, C + 1).")

    # exclude border color changes more than twice
    solver.add_program_line(exclude_border_color_changes(puzzle.row, puzzle.col, symbol_1, symbol_2))
    solver.add_program_line(exclude_border_color_changes(puzzle.row, puzzle.col, symbol_2, symbol_1))

    symbol_1_initial: List[Tuple[int, int]] = []
    symbol_2_initial: List[Tuple[int, int]] = []
    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name == symbol_1:
            solver.add_program_line(f"{symbol_1}({r}, {c}).")
            symbol_1_initial.append((r, c))
        else:
            solver.add_program_line(f"not {symbol_1}({r}, {c}).")
            symbol_2_initial.append((r, c))

    solver.add_program_line(grid_color_connected(color=symbol_1, grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(grid_color_connected(color=f"not {symbol_1}", grid_size=(puzzle.row, puzzle.col)))

    solver.add_program_line(display(item=symbol_1))
    solver.add_program_line(display(item=symbol_2))
    solver.solve()

    return solver.solutions
