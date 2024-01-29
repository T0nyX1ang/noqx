"""The Nuribou solver."""

from typing import List, Tuple

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
    adj_x = "adj_x(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."
    same_rc = "same_rc(R, C, R1, C1) :- grid(R, C), grid(R1, C1), R1 = R.\n"
    same_rc += "same_rc(R, C, R1, C1) :- grid(R, C), grid(R1, C1), C1 = C."
    count1 = f"#count {{ R2, C2: {tag}(R, C, R2, C2), same_rc(R, C, R2, C2) }} = CC1"
    count2 = f"#count {{ R2, C2: {tag}(R1, C1, R2, C2), same_rc(R1, C1, R2, C2) }} = CC2"
    constraint = f":- {color}(R, C), {color}(R1, C1), adj_x(R, C, R1, C1), {count1}, {count2}, CC1 = CC2."
    return adj_x + "\n" + same_rc + "\n" + constraint


def avoid_unknown_region(known_cells: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to avoid regions that does not derive from a source cell.

    A grid fact and a region rule should be defined first.
    """
    included = ""
    for src_r, src_c in known_cells:
        included += f"not {tag_encode('region', 'adj', adj_type, color)}({src_r}, {src_c}, R, C), "
    return f":- grid(R, C), {included.strip()} {color}(R, C)."


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

    solver.add_program_line(avoid_unknown_region(list(E.clues.keys()), color="not black"))
    solver.add_program_line(connected_parts(color="black"))
    solver.add_program_line(noribou_strip_different(color="black"))
    solver.add_program_line(all_rect(color="black"))
    solver.add_program_line(display(color="black"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
