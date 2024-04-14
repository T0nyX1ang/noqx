"""The Nuribou solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding, tag_encode
from .utilsx.fact import display, grid
from .utilsx.reachable import avoid_unknown_src, grid_src_color_connected, grid_branch_color_connected
from .utilsx.rule import adjacent, count_region, shade_c
from .utilsx.shape import all_rect
from .utilsx.solution import solver


def noribou_strip_different(color: str = "black") -> str:
    """Generate a rule to ensure that no two adjacent cells are shaded."""
    tag = tag_encode("reachable", "grid", "branch", "adj", 4, color)
    same_rc = "same_rc(R, C, R1, C1) :- grid(R, C), grid(R1, C1), R1 = R.\n"
    same_rc += "same_rc(R, C, R1, C1) :- grid(R, C), grid(R1, C1), C1 = C."
    count1 = f"#count {{ R2, C2: {tag}(R, C, R2, C2), same_rc(R, C, R2, C2) }} = CC1"
    count2 = f"#count {{ R2, C2: {tag}(R1, C1, R2, C2), same_rc(R1, C1, R2, C2) }} = CC2"
    constraint = f":- {color}(R, C), {color}(R1, C1), adj_x(R, C, R1, C1), {count1}, {count2}, CC1 = CC2."
    return same_rc + "\n" + constraint


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    all_src = []
    for (r, c), clue in E.clues.items():
        if isinstance(clue, int) or clue == "yellow":
            all_src.append((r, c))

    if not all_src:
        raise ValueError("No clues found.")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="x"))
    solver.add_program_line(adjacent(_type=8))

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        else:
            current_excluded = [src for src in all_src if src != (r, c)]
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color="not black"))

            if clue != "yellow":
                num = int(clue)
                solver.add_program_line(count_region(num, (r, c), color="not black"))

    solver.add_program_line(avoid_unknown_src(color="not black"))
    solver.add_program_line(grid_branch_color_connected(color="black"))
    solver.add_program_line(noribou_strip_different(color="black"))
    solver.add_program_line(all_rect(color="black"))
    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
