"""The Nurikabe solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import (
    avoid_unknown_src,
    count_reachable_src,
    grid_color_connected,
    grid_src_color_connected,
)
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="black"))

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
    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Nurikabe",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VRNb5wwEL3zK6I5+4D5+vCl2qbZXra06W4VRQhFQB0FBUoKS1UZ8d8zM6CllfZSVYpSqTJ++954WD+PjfvvQ95pIW163EjgLzZPRtydKOBuL+1QHWutLsRmOD60HRIhPm634j6ve22lS1ZmjSZWZiPMe5WCBAEOdgmZMNdqNB+USYTZ4xAID2O7OclBerXSGx4ndjkHpY08WTjSW6Rl1ZW1vtvNkU8qNQcBNM9bfpsoNO0PDYsP0mXbFBUFivyIi+kfqqdlpB++to/DkiuzSZjNbHd/xq672iU62yV2xi6t4u/t1k/tOaNxNk1Y8M9o9U6l5PrLSqOV7tWImKgRvAhfjXCXeU8g8FDSps8y9FG6JxnZKIOTjCVK/ySl7aD2ftEh6nDVkuaKV+3SZM6qffp7eIMV4Qg6lOzzlnHL6DAecBnCuIzvGG1Gn3HHOVeMN4yXjB5jwDkhFeKPSvUCdlJ3/uJ+b1ThfyyWWSnsh+4+LzUe02RoCt1dJG3X5DXgjTBZ8BO48+Hy/l8SL35JUPHt13b+X5sd/CLh29BVj3mhIbOeAQ==",
        },
        {
            "url": "https://puzz.link/p?nurikabe/19/12/g5zw3k2h4g4k.v.h2i2g4z3n7j3k2h4h4k3i4j3zzk2i2k2p6j2k6k",
            "test": False,
        },
    ],
}
