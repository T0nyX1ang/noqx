"""The Mochikoro solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import (
    count_reachable_src,
    grid_color_connected,
    grid_src_color_connected,
)
from noqx.rule.shape import all_rect, avoid_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(grid_color_connected(color="not black", adj_type=8, grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="black"))
    solver.add_program_line(all_rect(color="not black"))

    all_src = []
    for (r, c), _ in puzzle.text.items():
        all_src.append((r, c))
    assert len(all_src) > 0, "No clues found."

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(f"not black({r}, {c}).")
        current_excluded = [src for src in all_src if src != (r, c)]
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color="not black"))
        if isinstance(num, int):
            solver.add_program_line(count_reachable_src(num, (r, c), color="not black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Mochikoro",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVRi5tAEH73VxzzPA+uu5rcvpT0eulL6rVNSjhEgrEekTNsamIpG/Lfb3aUmhYPehykUIrZj2++Hcdvx3Wz/9ZkdYFCuJ8co4/EUIURDyECHn53LcpDVegrnDSHjamJIN5Np/iQVfvCS7qs1Dvaa20naN/rBAQgBDQEpGg/6aP9oG2Mdk5TgIq0WZsUEL3t6ZLnHbtpReETjztO9J5oXtZ5VaxmrfJRJ3aB4J7zlu92FLbmewGdDxfnZrsunbDODrSY/abcdTP75qt5bLpckZ7QTlq78wG7srfraGvXsQG7bhWvt1vtzJDR6/R0ooZ/JqsrnTjXX3o67ulcHwljfYTQp1vp3bbvBEL5axi5woo8dkLEwpteGI1JUD9D4QuKZR8HruBZrH6vKCJXoX+kGLkK47NYncXkWrD3e8YpY8C4oKWhlYzvGH3GkHHGObeMS8YbRsUYcc7INecP2wcyAK0QJK0vaHt5AW+JpE9w4Ar/XTX1Epg39UOWF7Tj42a7Luqr2NTbrAI6XE4e/AAevMvU//Pm4ueNa77/olPn73/FCfWVviV7h7BrVtkqNxXQnxWyLp/Rn8t/aZ3X1794N+nood2Rb8pHUxtIvSc=",
        },
        {
            "url": "https://puzz.link/p?mochikoro/22/13/4l2k4m3w4p5h1n2x2v4i2h4k2h5p2k4m5j4q2t2u3n4g4l3o4o2n2j2zk2g1n1o",
            "test": False,
        },
    ],
}
