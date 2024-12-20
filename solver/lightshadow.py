"""The Light and Shadow solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(avoid_unknown_src(color="black"))
    solver.add_program_line(avoid_unknown_src(color="not black"))

    all_src = []
    for (r, c), clue in puzzle.text.items():
        all_src.append((r, c))
    assert len(all_src) > 0, "No clues found."

    for (r, c), clue in puzzle.text.items():
        assert isinstance(clue, int) or (isinstance(clue, str) and clue == "?"), "Clue must be an integer or '?'."
        current_excluded = [src for src in all_src if src != (r, c)]
        color = "black" if puzzle.surface.get((r, c)) == 4 else "not black"
        solver.add_program_line(f"{color}({r}, {c}).")
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color=color))

        if clue != "?":
            solver.add_program_line(count_reachable_src(clue, (r, c), color=color))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Light and Shadow",
    "category": "shade",
    "aliases": ["lightandshadow"],
    "examples": [
        {
            "data": "m=edit&p=7VZdT9tcDL7vr0C+9kXOR/N1MzEGu2Fle8uE0FFVpV0QFe3CUjJNqfrfsX0CJ2WgFzSpV6iK7Tx5Yj92zkm6/tUUdYlKobJoUoyQIrTDGIdJhHGcyBF1v/PF3bLMD/CwubuuagoQz05O8KpYrsuB61iTwabN8vYQ28+5AwUImg4FE2y/5Zv2S96OsB3TJUBL2KknaQqPQ3gh1zk68qCKKB75mG+7pHC+qOfLcnpKVwn5mrv2HIHrfJS7OYRV9buETgefz6vVbMHArLijZtbXi9vuyrr5Ud00HVdNttgeernjZ+SaIJdDL5ejZ+RyF/8ud3lbPSc0m2y3NPD/SOo0d6z6ewjTEI7zDZgUcosQD8UlyrtMXOrPlNLea+O97XD7cJ54n0Sdt95nHS/z6XTki2jD+aj+iOvTvQ4y6t+vBxHkn2gHxJTNgQkM1kqMKFC4sIM0ULgPB8MeQ7L2knCLDj4ERio5CHhgcPc7OZQSJA4UmYwD2+NoQWh1P3J4ag6SHsdKqX4enuiOGmUlT0+OTFvuCpy4Uxg4Ms2+5lj67DUuT2m3ViKZ+7X4Ce7Wyp6OR57ubu+ZDJmQwHk6ZR1J5l4eWRU7ebR5mPwjh1eMTNVzaO2ofEP2UuyJWC32nJY2tkbsJ7GR2KHYU+Eci70QeyTWio2Fk/DmePX28VvDUufar+g9aHNGyyv56W/4jr6MTgYOxk19VcxLemeOmtWsrA9GVb0qlkCfp+0A/oAczvDX7v2LtfcvFg8/euXG29te+x85juZqEmzPEG6baTGdV0ugvzv4Mn75Rpzy6Bdw8zbcpn/he58mvbzgZ1MvbopZCZPBPQ==",
        },
    ],
}
