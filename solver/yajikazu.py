"""The Yajilin-Kazusan solver."""

from typing import List, Tuple

from .core.common import display, grid, shade_c
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.solution import solver


def yajikazu_count(target: int, src_cell: Tuple[int, int], arrow_direction: int, color: str = "black") -> str:
    """
    Generates a constraint for counting the number of {color} cells in a row / col.

    A grid fact should be defined first.
    """
    src_r, src_c = src_cell
    op = "<" if arrow_direction in [0, 1] else ">"

    if arrow_direction in [1, 2]:  # left, right
        return f":- not {color}({src_r}, {src_c}), #count {{ C1 : {color}({src_r}, C1), C1 {op} {src_c} }} != {target}."

    if arrow_direction in [0, 3]:  # up, down
        return f":- not {color}({src_r}, {src_c}), #count {{ R1 : {color}(R1, {src_c}), R1 {op} {src_r} }} != {target}."

    raise AssertionError("Invalid direction.")


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="gray"))
    solver.add_program_line(grid_color_connected(color="not gray"))

    # avoid all cells are unshaded
    solver.add_program_line(":- { gray(R, C) } = 0.")

    for (r, c), clue in puzzle.text.items():
        assert isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows."
        num, direction = clue.split("_")
        assert num.isdigit() and direction.isdigit(), "Invalid arrow or number clue."
        solver.add_program_line(yajikazu_count(int(num), (r, c), int(direction), color="gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Yajisan-Kazusan",
    "category": "shade",
    "aliases": ["yk", "yajisan-kazusan"],
    "examples": [
        {
            "data": "m=edit&p=7VRNj9MwEL3nV1Q+gTRIdpzvW1m2XEr4aNFqFUVRWrLasC2BZIPAVf/7jidGdWguHIAVQlFen59nxs/O1N2XvmwrEB7EICPgIPDxQ44DDpGI6OXmWdf3uyqZwby/v21aJACvFwu4KXdd5WQmKncOKk7UHNTLJGMuA3oFy0G9TQ7qVaJSUCucYhChtkQmGLhIL0/0iuY1uxhEwZGnQ0GB9Brptm63u6pYDsqbJFNrYHqd55StKds3Xys2lKDxttlvai1synvcTHdbfzYzXf+huetNrMiPoOaD3dWEXXmyq+lgV7MJu3oXv9lunB+PeOzv0HCRZNr7+xONTnSVHBDT5MA8V6d6hUQ3+gthRc/XklvoE/4hxbRAoXdkJJ9ridtRgXeWGFAtaZcPwyHKqhVSec9OjORZYkyJY8n4shIFF2fGBKdqrp0qBMW5Bbe1YCLOLGvXc6PzOJe8jDVJhyTG2oQXObGunFjDo3o/aWYfI41yRwcqAnPu9n5D48WOi6gjxnER7c06A+weQT10TbggdAnX2GKgJOELQk7oEy4p5pLwivCC0CMMKCbUTfpLbfwH7GR4K+o7cfrx/+253MnYqm9vym2F107a7zdVO0ubdl/uGN7zR4d9Y/RmEsO9/1f/X7r69Sfgj+2f89js4H+ZfS8/1nel6mdPNOvKT8/0CH+fstx5AA==",
        },
        {
            "url": "https://puzz.link/p?yajikazu/9/9/301040104010103040201030101030103040301030101020304010203030401040404040301010304010401030402030402020203040203040302020204040304020402040201010402020102020402040",
            "test": False,
        },
    ],
}
