"""The Nuribou solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.helper import tag_encode
from .utilsx.rule import adjacent, connected_parts, count_region, region, shade_c
from .utilsx.shape import all_rect
from .utilsx.solution import solver


def noribou_strip_different(color: str = "black") -> str:
    """Generate a rule to ensure that no two adjacent cells are shaded."""
    tag = tag_encode("reachable", "adj", 4, color)
    same_rc, constraint = "", ""
    for dir in ["lu", "rd", "ld", "ru"]:
        op1 = "<=" if dir[0] == "l" else ">="
        op2 = "<" if dir[1] == "u" else ">"
        same_rc += f"{dir}_rule(R, C, R2, C2) :- grid(R, C), grid(R2, C2), R2 = R, C2 {op1} C.\n"
        same_rc += f"{dir}_rule(R, C, R2, C2) :- grid(R, C), grid(R2, C2), C2 = C, R2 {op2} R.\n"
    count1 = f"#count {{ R2, C2: {tag}(R, C, R2, C2), lu_rule(R, C, R2, C2) }} = CC1"
    count2 = f"#count {{ R2, C2: {tag}(R+1, C+1, R2, C2), rd_rule(R+1, C+1, R2, C2) }} = CC2"
    constraint = f":- {color}(R, C), {color}(R+1, C+1), {count1}, {count2}, CC1 = CC2.\n"
    count1 = f"#count {{ R2, C2: {tag}(R, C, R2, C2), ld_rule(R, C, R2, C2) }} = CC1"
    count2 = f"#count {{ R2, C2: {tag}(R-1, C+1, R2, C2), ru_rule(R-1, C+1, R2, C2) }} = CC2"
    constraint += f":- {color}(R, C), {color}(R-1, C+1), {count1}, {count2}, CC1 = CC2."
    return same_rc + constraint


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
    solver.add_program_line(adjacent(_type=8))

    for (r, c), clue in E.clues.items():
        if clue == "black":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not black({r}, {c}).")
        else:
            current_excluded = [src for src in all_src if src != (r, c)]
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(region((r, c), current_excluded, color="not black", avoid_unknown=True))

            if clue != "yellow":
                num = int(clue)
                solver.add_program_line(count_region(num, (r, c), color="not black"))

    solver.add_program_line(connected_parts(color="black"))
    solver.add_program_line(noribou_strip_different(color="black"))
    solver.add_program_line(all_rect(color="black"))
    solver.add_program_line(display(color="black"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
