"""The Coral solver."""

from collections import Counter
from typing import Dict, List, Tuple, Union

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import border_color_connected, grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def len_segment(color: str = "black") -> str:
    """
    Generate a rule to get the length of segments.
    """
    rule = f"nth_horizontal(R, C, 1) :- {color}(R, C), not {color}(R, C - 1).\n"
    rule += f"nth_horizontal(R, C, N) :- {color}(R, C), nth_horizontal(R, C - 1, N - 1).\n"
    rule += f"nth_vertical(R, C, 1) :- {color}(R, C), not {color}(R - 1, C).\n"
    rule += f"nth_vertical(R, C, N) :- {color}(R, C), nth_vertical(R - 1, C, N - 1).\n"

    rule += f"len_horizontal(R, C, N) :- nth_horizontal(R, C, 1), nth_horizontal(R, C + N - 1, N), not {color}(R, C + N).\n"
    rule += f"len_vertical(R, C, N) :- nth_vertical(R, C, 1), nth_vertical(R + N - 1, C, N), not {color}(R + N, C).\n"

    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    top_clues = {}
    for c in range(puzzle.col):
        top_clues[c] = tuple(clue for (r1, c1), clue in puzzle.text.items() if r1 <= -1 and c1 == c)

    left_clues = {}
    for r in range(puzzle.row):
        left_clues[r] = tuple(clue for (r1, c1), clue in puzzle.text.items() if r1 == r and c1 <= -1)

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(display())
    solver.add_program_line(len_segment())
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black"))
    solver.add_program_line(border_color_connected(rows=puzzle.row, cols=puzzle.col, color="not black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))

    for r, clue in left_clues.items():
        for num, count in Counter(clue).items():
            solver.add_program_line(f":- #count{{ C: grid({r}, C), len_horizontal({r}, C, {num}) }} != {count}.")
        forbidden_len = ",".join([f"N != {x}" for x in Counter(clue).keys()])
        solver.add_program_line(f":- grid({r}, C), len_horizontal({r}, C, N), {forbidden_len}.")

    for c, clue in top_clues.items():
        for num, count in Counter(clue).items():
            solver.add_program_line(f":- #count{{ R: grid(R, {c}), len_vertical(R, {c}, {num}) }} != {count}.")
        forbidden_len = ",".join([f"N != {x}" for x in Counter(clue).keys()])
        solver.add_program_line(f":- grid(R, {c}), len_vertical(R, {c}, N), {forbidden_len}.")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    # solver.add_program_line(display(item="len_horizontal", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Coral",
    "category": "shade",
    "examples": [
        {
            "url": "https://puzz.link/p?nonogram/8/8/31h31h22h4i31h321g111g2i32h41h311g11h4i31h21h21h",
            "test": False,
        },
    ],
}
