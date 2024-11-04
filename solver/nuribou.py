"""The Nuribou solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected
from noqx.rule.shape import all_rect
from noqx.solution import solver


def noribou_strip_different(color: str = "black") -> str:
    """
    Generate a rule to ensure that no two adjacent cells have the same shaded strips.

    An all_rect constraint should be defined first.
    """
    rule = "nth(R, C, 1) :- upleft(R, C).\n"
    rule += "nth(R, C, N) :- up(R, C), nth(R, C - 1, N - 1).\n"
    rule += "nth(R, C, N) :- left(R, C), nth(R - 1, C, N - 1).\n"
    rule += f":- {color}(R, C), nth(R, C, N1), nth(R, C, N2), N1 < N2.\n"

    rule += "len_strip(R, C, 1) :- upleft(R, C), not up(R, C + 1), not left(R + 1, C).\n"
    rule += f"len_strip(R, C, N) :- upleft(R, C), up(R, C + 1), {color}(R, C + N - 1), not {color}(R, C + N), nth(R, C + N - 1, N).\n"
    rule += f"len_strip(R, C, N) :- upleft(R, C), left(R + 1, C), {color}(R + N - 1, C), not {color}(R + N, C), nth(R + N - 1, C, N).\n"
    rule += f":- {color}(R, C), len_strip(R, C, L), len_strip(R, C, L1), L < L1.\n"
    rule += "len_strip(R, C, L) :- up(R, C), nth(R, C, N), len_strip(R, C - N + 1, L).\n"
    rule += "len_strip(R, C, L) :- left(R, C), nth(R, C, N), len_strip(R - N + 1, C, L).\n"
    rule += f":- {color}(R, C), {color}(R1, C1), adj_x(R, C, R1, C1), len_strip(R, C, L), len_strip(R1, C1, L1), L = L1."
    rule += ":- grid(R, C), remain(R, C).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="x"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    all_src = []
    for (r, c), clue in puzzle.text.items():
        all_src.append((r, c))
    assert len(all_src) > 0, "No clues found."

    for (r, c), clue in puzzle.text.items():
        assert isinstance(clue, int) or (isinstance(clue, str) and clue == "?"), "Clue must be an integer or '?'."
        solver.add_program_line(f"not black({r}, {c}).")

        current_excluded = [src for src in all_src if src != (r, c)]
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color="not black"))
        if clue != "?":
            solver.add_program_line(count_reachable_src(clue, (r, c), color="not black"))

    solver.add_program_line(avoid_unknown_src(color="not black", adj_type=4))
    solver.add_program_line(noribou_strip_different(color="black"))
    solver.add_program_line(all_rect(color="black"))
    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Nuribou",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VRNb5tAEL3zK6I574H9wHb2Urlp3ItLP+wqihCKsEsUVFxS7K2qtfzfMzNACRGXtlKUQ7Ts05uZ3Zm3H+z+p8vqXEhNn56JUEhskVbcpTHcw7ati0OZ2zMxd4e7qkYixMfFQtxm5T4PknZUGhz9ufVz4d/bBCQIUNglpMJ/tkf/wfpY+BWGQBj0LZtBCullT684TuyiccoQedxypNdIt0W9LfObZeP5ZBO/FkB13vJsorCrfuXQ6iB7W+02BTk22QEXs78r7tvI3n2rvrt2rExPws8buasRubqXS7SRS2xELq3i/+WW99WY0PP0dMIN/4JSb2xCqr/2dNbTlT0ixvYIeoJT6ZT5TMBIyvQGRXWO2SAeGTTxerTmZGhOKdn0jylDmowXp7OlGtpao42XqrNN+KS65PIDTxQNSkqu+SjnjHL0tuKajzMoNRSt9BObVfRLVmY6UKkiytjFcRslb+Y144JRMa5xr4XXjO8YQ8aIccljLhmvGC8YDeOEx0zptP7qPJ9BTqIn/CyMteg18i+RNEhg5erbbJvjXx273Savz+Kq3mUl4AN6CuA3cOdral7f1Gd/U2nzw5f2J740Ofg2wA9XF5vKQRo8AA==",
        },
        {"url": "https://puzz.link/p?nuribou/20/15/h5o6zs6k3i3h6zg4p4zi.pbzl7h3zz4k4l9v7zn4h.l4k4o4q7i2", "test": False},
    ],
}
