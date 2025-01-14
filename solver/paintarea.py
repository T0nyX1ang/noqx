"""The Paintarea solver."""

from typing import List

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_same_color, count_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(grid_color_connected(color="gray", adj_type=4, grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))
    solver.add_program_line(avoid_rect(2, 2, color="not gray"))
    solver.add_program_line(area_same_color(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, (ar, _) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        if isinstance(num, int):
            solver.add_program_line(count_adjacent(num, (r, c), color="gray"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Paintarea",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VZRb9M8FH3vr5j87IfYcRI7L2iMjpfR8dGhaYqiKusyVn0tGW2DUKr+953rXC8VmjQQMF5Qmtvjm9Pr4+Mbq5svbbWuZYYrtjKSClccGX+nEX3CdbHYLuv8SB6327tmDSDl+empvK2Wm3pUMKsc7TqXd8eye5sXQgkpNG4lStn9l++6d3k3lt0Uj4S0yJ31JA04HuClf07opE+qCHjCGPAKcL5Yz5f17KzPvM+L7kIKmue1/zVBsWq+1oJ10HjerK4XlLiutljM5m5xz0827U3zf8tcVe5ld9zLnT4hNx7kEuzlEnpCLq3iD8t15X4P2z9A8CwvSPvHAdoBTvMd4iTfCZ3gp7TTfmeEdlTpFaRxIlVIxI9DG2GoeYgSyhe68vHUR+3jBeaRXezjGx8jHxMfzzxnjOlVnEhlUpFrVETXKQMBhA3yCecN8knIO6lSiCCcZMCWMTgpcxJwMuaga1WGNXgMfsb8FBxaDOEMHMucDIuzMWPUtFwzA98x34LjmGOd1BHnXQTMdZwGZo6LgQ1jAwzPgcGVWmnGyKs+r4yBDwGnwBlj6Desn3xIgg/Qn/C8CfgJ88mT4Bv5QHvpMfY77ef1ngQP0wMPyZPgG3mSBU8OPCRPgof2wEOL+pbrk1fBT/ijXPAHHMcc+ANf2IfBQ+9PFPwZ/MT3o5/wEpj6BA116dvqxEfjY+rbLaOm/8HXQui+cAz/bf+O/HqbP6ut0NjygwvN/7tH5agQ03Z9W81rnBzjm0/10aRZr6olRpN2dV2vwxgH934kvgl/+3ff/DvL/9JZTlsQ/dSJ/gLd+oycAu7iWO/OpbhvZ9Vs3qDH4B3l0eff519cPV43cV8tPm/xb6cS5egB",
        },
        {
            "url": "https://puzz.link/p?paintarea/18/10/fesmfvrsi3vrvsntsvuttippjvnvrnvdferjbmtvtmnftnrnvrfbanmunev6vffddd8a1zj2b0t2b2a2c1o1d2b1c3zx2d2a2a3t",
            "test": False,
        },
    ],
}
