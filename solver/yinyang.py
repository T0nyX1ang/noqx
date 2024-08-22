"""The Yin-Yang solver."""

from typing import List, Tuple

from .core.common import display, grid, shade_c
from .core.helper import extract_two_symbols
from .core.penpa import Puzzle
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[str]:
    symbol_set = set(puzzle.symbol.values())
    symbol_1, symbol_2 = extract_two_symbols(symbol_set)

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color=symbol_1))
    solver.add_program_line(f"{symbol_2}(R, C) :- grid(R, C), not {symbol_1}(R, C).")
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_rect(rect_r=2, rect_c=2, color=symbol_1))
    solver.add_program_line(avoid_rect(rect_r=2, rect_c=2, color=f"not {symbol_1}"))

    symbol_1_initial: List[Tuple[int, int]] = []
    symbol_2_initial: List[Tuple[int, int]] = []
    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name == symbol_1:
            solver.add_program_line(f"{symbol_1}({r}, {c}).")
            symbol_1_initial.append((r, c))
        else:
            solver.add_program_line(f"not {symbol_1}({r}, {c}).")
            symbol_2_initial.append((r, c))

    solver.add_program_line(grid_color_connected(color=symbol_1, initial_cell=symbol_1_initial[0]))
    solver.add_program_line(grid_color_connected(color=f"not {symbol_1}", initial_cell=symbol_2_initial[0]))

    solver.add_program_line(display(item=symbol_1))
    solver.add_program_line(display(item=symbol_2))
    solver.solve()

    return solver.solutions
