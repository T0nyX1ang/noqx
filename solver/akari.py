"""Akari (Light up) solver."""

from typing import List

from .core.common import display, grid
from .core.helper import tag_encode
from .core.neighbor import adjacent, count_adjacent
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def lightup(color: str = "black") -> str:
    """
    A lit rule specially designed for akari.

    A grid fact and an adjacent rule should be defined first.
    """
    tag = tag_encode("reachable", "sun_moon__3__0", "branch", "adj", 4, color)
    initial = f"{tag}(R0, C0, R, C) :- grid(R, C), sun_moon__3__0(R, C), R0 = R, C0 = C."
    propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), {color}(R, C), adj_4(R, C, R1, C1), (R - R0) * (C - C0) = 0."
    constraint1 = f":- sun_moon__3__0(R0, C0), sun_moon__3__0(R, C), |R0 - R| + |C0 - C| != 0, {tag}(R0, C0, R, C)."
    constraint2 = f":- grid(R, C), not black(R, C), not sun_moon__3__0(R, C), {{ {tag}(R0, C0, R, C) }} = 0."

    return initial + "\n" + propagation + "\n" + constraint1 + "\n" + constraint2


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line("{ sun_moon__3__0(R, C) } :- grid(R, C), not black(R, C).")
    solver.add_program_line(adjacent())
    solver.add_program_line(lightup(color="not black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")

    for (r, c), clue in puzzle.text.items():
        if isinstance(clue, int):
            solver.add_program_line(count_adjacent(clue, (r, c), color="sun_moon__3__0"))

    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name == "sun_moon__3__0":
            solver.add_program_line(f"sun_moon__3__0({r}, {c}).")

    solver.add_program_line(display(item="sun_moon__3__0"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Akari",
    "category": "var",
    "aliases": ["lightup"],
    "examples": [
        {
            "data": "m=edit&p=7VTfa9swEH73XxH0fA+W5SSO3rKu2UuW/XBGCcIEJ3OJaVx3djyGQv733p1E7UIZYw+lg6Ho03ffydKXE1L7o8ubAmRIP5UAjthimXCPkgn30Ld1eToWegTz7nSoGyQAnxYLuM2PbREYPysLznam7RzsB22EFCAi7FJkYL/os/2obQo2xZSAGLWlmxQhve7pDeeJXTlRhshXjk+RbpDuy2Z/LLZLzKLyWRu7BkH7vOOviYqq/lkI74PifV3tShJ2+Qn/THsoH3ym7b7Xd52fK7ML2Lmzu3nBrurtEnV2if3Gbtvdb6u6vv8ru/ld3pQvOZ1llwtW/Ct63WpDtr/1NOlpqs9CRULHIMaSh4mLpoqHxIkzJ8rQqVLGboy8rrwee31CMS6/8subCKbutHkbI59C2s6IEdbDC7TxIE8GBl+TkUHIhoYxGRvGZHCwGhsdxmT42fZs/WkF/AtSnxE3jAvGiHGNBQSrGN8zhoxjxiXPuWa8YbxijBknPGdKR/CHh+Rq+Qp2jHKX/Xkb/3taFhiRds1tvi/wgqy6alc0o1XdVPkR4/SQPxQCH6VLIH4J7kbRG/f/nXr9d4qqH761i/DW7ODV9GXMgkc=",
        },
        {
            "url": "https://puzz.link/p?akari/17/17/g666.g6.g6.x6.x6.x6.obl6.gbi6cv.gblcmbl7cv6bi66blam6.x.gbv.gcv66.g666.g.g",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?akari/20/20/................................h............h1...h............i...i...........i1.bg........t.....i6cn...hbibi1b..kbl1b0.g6bgc..l..k.j1.l..hciam...i6.q...v0...bs....b.b..h2..h....i..h..i..h....i..h..b..h....h1..h...h..h....................../",
            "test": False,
        },
    ],
}
