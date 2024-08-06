"""The Nuribou solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.helper import tag_encode
from .core.neighbor import adjacent
from .core.penpa import Puzzle
from .core.reachable import (
    avoid_unknown_src,
    count_reachable_src,
    grid_branch_color_connected,
    grid_src_color_connected,
)
from .core.shape import all_rect
from .core.solution import solver


def noribou_strip_different(color: str = "black") -> str:
    """Generate a rule to ensure that no two adjacent cells are shaded."""
    tag = tag_encode("reachable", "grid", "branch", "adj", 4, color)
    same_rc = "same_rc(R, C, R1, C1) :- grid(R, C), grid(R1, C1), R1 = R.\n"
    same_rc += "same_rc(R, C, R1, C1) :- grid(R, C), grid(R1, C1), C1 = C."
    count1 = f"#count {{ R2, C2: {tag}(R, C, R2, C2), same_rc(R, C, R2, C2) }} = CC1"
    count2 = f"#count {{ R2, C2: {tag}(R1, C1, R2, C2), same_rc(R1, C1, R2, C2) }} = CC2"
    constraint = f":- {color}(R, C), {color}(R1, C1), adj_x(R, C, R1, C1), {count1}, {count2}, CC1 = CC2."
    return same_rc + "\n" + constraint


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="x"))
    solver.add_program_line(adjacent(_type=8))

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
        current_excluded = [src for src in all_src if src != (r, c)]
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color="not black"))

        if clue != "?":
            solver.add_program_line(count_reachable_src(clue, (r, c), color="not black"))

    solver.add_program_line(avoid_unknown_src(color="not black"))
    solver.add_program_line(grid_branch_color_connected(color="black"))
    solver.add_program_line(noribou_strip_different(color="black"))
    solver.add_program_line(all_rect(color="black"))
    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions
