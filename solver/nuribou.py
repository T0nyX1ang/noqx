"""The Nuribou solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.helper import tag_encode
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import (
    grid_branch_color_connected,
)
from .numlin import clue_bit, num_binary_range, grid_bit_color_connected
from .core.shape import all_rect
from .core.solution import solver


# def noribou_strip_different(color: str = "black") -> str:
#     """Generate a rule to ensure that no two adjacent cells are shaded."""
#     tag = tag_encode("reachable", "grid", "branch", "adj", 4, color)
#     same_rc = "same_rc(R, C, R1, C1) :- grid(R, C), grid(R1, C1), R1 = R.\n"
#     same_rc += "same_rc(R, C, R1, C1) :- grid(R, C), grid(R1, C1), C1 = C.\n"
#     count1 = f"#count {{ R2, C2: {tag}(R, C, R2, C2), same_rc(R, C, R2, C2) }} = CC1"
#     count2 = f"#count {{ R2, C2: {tag}(R1, C1, R2, C2), same_rc(R1, C1, R2, C2) }} = CC2"
#     constraint = f":- {color}(R, C), {color}(R1, C1), adj_x(R, C, R1, C1), {count1}, {count2}, CC1 = CC2.\n"
#     constraint += ":- grid(R, C), remain(R, C)."
#     return same_rc + constraint.strip()


def noribou_strip_different(color: str = "black") -> str:
    """
    Generate a rule to ensure that no two adjacent cells are shaded.
    Based on all_rect rule.
    """
    rule = "nth(R, C, 1) :- upleft(R, C).\n"
    rule += "nth(R, C, N) :- up(R, C), nth(R, C-1, N-1).\n"
    rule += "nth(R, C, N) :- left(R, C), nth(R-1, C, N-1).\n"
    rule += f":- {color}(R, C), nth(R, C, N1), nth(R, C, N2), N1 < N2.\n"

    rule += "len_strip(R, C, 1) :- upleft(R, C), not up(R, C+1), not left(R+1, C).\n"
    rule += f"len_strip(R, C, N) :- upleft(R, C), up(R, C+1), {color}(R, C+N-1), not {color}(R, C+N), nth(R, C+N-1, N).\n"
    rule += f"len_strip(R, C, N) :- upleft(R, C), left(R+1, C), {color}(R+N-1, C), not {color}(R+N, C), nth(R+N-1, C, N).\n"
    rule += f":- {color}(R, C), len_strip(R, C, L), len_strip(R, C, L1), L < L1.\n"
    rule += "len_strip(R, C, L) :- up(R, C), nth(R, C, N), len_strip(R, C-N+1, L).\n"
    rule += "len_strip(R, C, L) :- left(R, C), nth(R, C, N), len_strip(R-N+1, C, L).\n"
    rule += f":- {color}(R, C), {color}(R1, C1), adj_x(R, C, R1, C1), len_strip(R, C, L), len_strip(R1, C1, L1), L = L1."
    rule += ":- grid(R, C), remain(R, C).\n"
    return rule.strip()


def count_reachable_bit(clue, _id, nbit, color):
    tag = tag_encode("reachable", "grid", "bit", "adj", 4)
    id_str = []
    for i in range(nbit):
        bit = _id >> i & 1
        id_str.append(f"{tag}(R, C, {i}, {bit})")
    id_str = ", ".join(id_str)
    return f":- #count{{ R, C: grid(R, C), {color}(R, C), {id_str} }} != {clue}."


def connected_to_clue(color, adj_type):
    rule = "connected_to_clue(R, C) :- grid(R, C), clue(R, C).\n"
    rule += f"connected_to_clue(R, C) :- grid(R, C), {color}(R, C), connected_to_clue(R1, C1), adj_{adj_type}(R, C, R1, C1).\n"
    rule += f":- grid(R, C), {color}(R, C), not connected_to_clue(R, C).\n"
    return rule


def solve(puzzle: Puzzle) -> List[Solution]:
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

    rule, nbit = num_binary_range(len(puzzle.text.items()))
    solver.add_program_line(rule)

    for _id, ((r, c), clue) in enumerate(puzzle.text.items()):
        assert isinstance(clue, int) or (isinstance(clue, str) and clue == "?"), "Clue must be an integer or '?'."
        solver.add_program_line(f"not black({r}, {c}).")
        # current_excluded = [src for src in all_src if src != (r, c)]
        # solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color="not black"))
        # if clue != "?":
        #     solver.add_program_line(count_reachable_src(clue, (r, c), color="not black"))

        solver.add_program_line(clue_bit(r, c, _id + 1, nbit))
        if clue != "?":
            solver.add_program_line(count_reachable_bit(clue, _id + 1, nbit=nbit, color="not black"))

    # solver.add_program_line(avoid_unknown_src(color="not black"))
    solver.add_program_line(connected_to_clue(color="not black", adj_type=4))
    tag = tag_encode("reachable", "grid", "bit", "adj", 4)
    solver.add_program_line(f"nuribou_ok(R, C) :- grid(R, C), not black(R, C), bit_range(B), {tag}(R, C, B, 1).")
    solver.add_program_line(":- grid(R, C), not black(R, C), not nuribou_ok(R, C).")
    # solver.add_program_line(f":- grid(R, C), not black(R, C), not {tag}(R, C, _).")
    solver.add_program_line(grid_bit_color_connected(nbit=nbit, color="not black", adj_type=4))
    solver.add_program_line(grid_branch_color_connected(color="black"))
    solver.add_program_line(noribou_strip_different(color="black"))
    solver.add_program_line(all_rect(color="black"))
    solver.add_program_line(display(item="black"))
    # solver.add_program_line(display(item="len_strip", size=3))
    print(solver.program)
    solver.solve()

    return solver.solutions
