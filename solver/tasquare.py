"""The Tasquare solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import (
    count_reachable_src,
    grid_color_connected,
    grid_src_color_connected,
)
from noqx.rule.shape import all_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(all_rect(color="black", square=True))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(f"not black({r}, {c}).")
        if isinstance(num, int):
            solver.add_program_line(grid_src_color_connected((r, c), color="black"))
            solver.add_program_line(count_reachable_src(num + 1, (r, c), color="black"))
        else:
            solver.add_program_line(count_adjacent(("gt", 0), (r, c), color="black"))

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Tasquare",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVNj9owEL3nVyCf5xDngw2+0e3SC822DdUKRREKNCtQQaGBVJUR/31nxumabqxWVbWrqqqCR2+e7fHLy4QcvrRlU4GU9AsT8AERRPGQh5QBD7+7ZpvjtlIDGLfHdd0gALidTOC+3B4qL+9WFd5Jj5Qeg36jciEFiACHFAXo9+qk3yqdgs5wSkCE3NQsChDeWHjH84SuDSl9xGmHEc4RGvGLqWHeqVzPQNA5r3g3QbGrv1ai00H5qt4tN0QsyyPezGG92Xczh/ZT/bnt1sriDHps5GYOuaGVS9DIJeSQS3fx53K3+9oldFScz2j4B5S6UDmp/mhhYmGmThhTdRJhQlsHqMI8FREFT4ghEbFNh5hiM3TplY9p9JiOIkxDm1J1u1f6VMuulgHl2FWPORW322VI1S/ymMrbw2VM9S/mWetF/eTpzciETrAMuiDZi/l3L5D/4dEYQ3osn9RnqXqPZY96LFvVZ50ajHF9mv1z0E4Zxs0+zaY6aLcS940bpx20Qwm6PWHPA44zbEnQIcfXHH2OMccpr7nheMfxmmPEcchrrqipf6vtLx/7M8nJQ+rr/kVvwz/KFl4usra5L1cV/jml7W5ZNYO0bnblFvNsXe4rgd+Dsye+CR786kb/PxEv/okg8/2/7Y35hZxczyGMQd+C2LeLcrGqsavQtZ/x0ejZ+Bd3B/9SxLE0PSEK7wE=",
        },
        {
            "url": "https://puzz.link/p?tasquare/21/15/g.k..k4k.x.h.i8j2q.u4i2l2jar.2l.h.zhak8i8h9j2.x1m.n2g.h.l.j2h3g1k2g4r.o1i3h.i.j.l1zj2g4i..g.i.h./",
        },
    ],
}
