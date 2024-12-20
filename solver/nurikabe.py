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
            "data": "m=edit&p=7VXBjtowEL3nK1ZznkOcOBB8qeh26YVm20K1WkURCmlWG21oaCDVyoh/35lxRFqVQ6tKVJUq48d74wl+Hsdm97XL2xKVz58wRvqmplUsPYhH0v2+Lat9XZornHb7x6Ylgng7m+FDXu9KL+2zMu9gJ8ZO0b41KShACKgryNB+MAf7ztgE7YKGADXF5i4pIHoz0DsZZ3btgsonnvSc6D3RomqLulzNXeS9Se0Sged5LU8zhU3zrYTeB+ui2awrDqzzPS1m91ht+5Fd97l56vpclR3RTp3dxRm74WCXqbPL7IxdXsWf2623zTmjk+x4pIJ/JKsrk7LrTwONB7owB8LEHEDH9GhMuyx7AiNNkjfdyXFEMjzJ2Cc5OsmJIhmdpPID0vo7PSY9HrTiuSaDDnmyYNAR/zy8oopIhBwq8XkvOBMMBJe0DLSh4BtBXzASnEvOjeCd4LWgFhxJzpgL8YulgpCMBQiaqqFd3S7gLQ3d8fuxcbn/sVjmpbDo2oe8KOmdTbrNumyvkqbd5DXQ9XD04Bmky5um/98YF78xuPj+b90bf/9splRXOiH2FmHbrfJV0dRAfzfIcR39FL+4ezrA8KVrq6d8XULmvQA=",
        },
        {
            "url": "https://puzz.link/p?nurikabe/19/12/g5zw3k2h4g4k.v.h2i2g4z3n7j3k2h4h4k3i4j3zzk2i2k2p6j2k6k",
            "test": False,
        },
    ],
}
