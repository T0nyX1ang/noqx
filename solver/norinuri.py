"""The Norinuri solver."""

from typing import List, Tuple

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import count_reachable_src, grid_src_color_connected
from noqx.solution import solver


def nori_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint for Norinori puzzles.

    A grid rule and an adjacent rule should be defined first.
    """
    return f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }} != 1."


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("black"))

    solver.add_program_line(adjacent())
    solver.add_program_line(nori_adjacent(color="black"))

    all_src: List[Tuple[int, int]] = []
    for (r, c, d, pos), _ in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        all_src.append((r, c))

    for (r, c, _, _), num in puzzle.text.items():
        current_excluded = [src for src in all_src if src != (r, c)]
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color="not black"))

        if isinstance(num, int):
            solver.add_program_line(count_reachable_src(num, (r, c), color="not black"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")
        else:
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Norinuri",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVRj5NAEH7nV1zmeR5YWJDui6nn1ZfKqa25XAhpKHI5IpVKu8Zs0/9+MwOKp33QmNSYXLb79ZtvB/ox7E53n23RVah8/oQJ0jcNrRKZQRLL9IexrPdNZS5wavf3bUcE8Xo2w7ui2VVeNmTl3sFNjJuie2UyUIAQ0FSQo3trDu61cSm6BS0BatLmfVJA9GqkN7LO7LIXlU88HTjRW6Jl3ZVNtZr3yhuTuSUC/84LuZopbNovFQw+OC7bzbpmYV3s6WF29/V2WNnZD+1HO+Sq/Ihu2ttdnLAbjnaZ9naZnbDLT/H3dptte8roJD8eqeDvyOrKZOz6/UiTkS7MgTA1BwgVXRrTW5Z3AjqmMPkeRiHf+Dl5HISY1wPeF32sggkJvGG+CTogQf8Q/5wQ60f3JB9K3NwKzgQDwSWZRRcKvhT0BSPBueRcCd4IXgpqwVhynvHj/mZBIPTBBFSCCIzuq3MGb1nYH7LHI/r/tNzLYGG7u6KsaGemdrOuuou07TZFA9QEjh58BZlZyD3lqS+cvS9w8f0/6g7//mxmVFc6Ie4aYWtXxapsG6A/FWRdR7/oZ3dPBxg+2a5etxZy7wE=",
        }
    ],
}
