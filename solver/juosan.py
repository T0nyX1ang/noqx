"""The Juosan solver."""

from typing import List

from .core.helper import full_bfs
from .core.common import area, display, grid, shade_c
from .core.penpa import Puzzle
from .core.solution import solver


def jousan_constraint():
    """Constrain consecutive lines."""
    # black for horizontal, not black for vertical
    rule = ":- grid(R, C), grid(R + 2, C), black(R, C), black(R + 1, C), black(R + 2, C).\n"
    rule += ":- grid(R, C), grid(R, C + 2), not black(R, C), not black(R, C + 1), not black(R, C + 2).\n"
    rule += 'content(R, C, "——") :- grid(R, C), black(R, C).\n'
    rule += 'content(R, C, "|") :- grid(R, C), not black(R, C).'
    return rule


def count_lines(area_id: int, num1: int, num2: int = 0):
    """Limit the number of horizontal or vertical lines."""
    rule = f"count_area({area_id}, N) :- #count{{ R, C: area({area_id}, R, C), black(R, C) }} = N.\n"
    rule += f":- not count_area({area_id}, {num1}), not count_area({area_id}, {num2})."
    return rule


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(jousan_constraint())

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.sudoku)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.sudoku[rc][0]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count_lines(i, data, len(ar) - data))

    solver.add_program_line(display(item="content", size=3))
    solver.solve()

    return solver.solutions
