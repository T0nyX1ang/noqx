"""Akari (Light up) solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid
from noqx.rule.helper import tag_encode
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.solution import solver


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
            "data": "m=edit&p=7VTfa9s8FH33XxH0rAfLchxHb1m/Zi9Zus0ZJQhjHM8lpnGd2fEYCvnfe++VVrswRims44Oh6OjcI0U6vvrRfevztuTCx5+MObRQQhFTDeKIqu/KpjodSjXhi/60b1ognN8sl/wuP3Slp92o1DubuTILbt4rzQTjLIAqWMrNJ3U2H5RJuEmgi/EQtJUdFAC9Hugt9SO7sqLwga8tnwHdAi2qtjiU2Qp6QfmotNlwhuu8o38jZXXzvWTOB8ZFU+8qFHb5CT6m21dH19P1X5v73o0V6YWbhbW7/WkX7Ti7crCL1NpF9hu7Xf+Q1U3z8Cq7+X3eVr9yOk8vF8j4Z/CaKY22vww0HmiizkwGTIWcTQU1kY1mkprYinMrCt+qQoS2DZwunR46PcIYpl+76XXAZ3a3aRktnkJcTrMJ5MMJuPCoHw2M/o1GRiEZGsdobByjwdFsZHQco+Fny5P1pxngE4Q6A24Jl4QB4QYSyI0k/I/QJ5wSrmjMNeEt4RVhSBjRmBluwQs3yeZybIdJzIzEfR8O0B/yqKV9AZ6X6f9PSz3Nkr69y4sSbs26r3dlO1k3bZ0fIE72+bFk8FJdPPaDUYUEw8P37/F6+8cLs++/+nb8ncuqIbFScHPD2bHP8qxo4FhB2jScjzB6sf7mXwU33O1G6j0C",
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
