"""The Context solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="x"))
    solver.add_program_line(avoid_adjacent_color(color="gray", adj_type=4))
    solver.add_program_line(grid_color_connected(color="not gray", adj_type=4, grid_size=(puzzle.row, puzzle.col)))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(f":- not gray({r}, {c}), #count {{ R, C: adj_4({r}, {c}, R, C), gray(R, C) }} != {num}.")
        solver.add_program_line(f":- gray({r}, {c}), #count {{ R, C: adj_x({r}, {c}, R, C), gray(R, C) }} != {num}.")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Context",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VXfj5pAEH73r7js8zyw/JCVN3s9+2K9tthcCCEGKZcjh8WiNM0a//ebGUhxrU1Kmnhp0uCO3zc7DN/O4Lj71qR1DtKij6MAv/FypeJlqzEvq7uWxb7MgxuYNvunqkYAcD+bwWNa7vJR3EUlo4OeBHoK+l0QCylA2LikSEB/DA76faAXoEPcEqDQN2+DbIR3PXzgfUK3rVNaiBcdRhghzIo6K/PVvPV8CGK9BEHPecN3ExSb6nsuOh3Es2qzLsixTvd4mN1Tse12ds2X6rnpYmVyBD1t5YYX5Dq9XIKtXEIX5NIp/l5uua0uCZ0kxyMW/BNKXQUxqf7cQ9XDMDigXQQH4bh4K3WZeyKcMVL7J3U9k5q7nm1Q3zGpmdn3kTo9VQZV0ghWFNynUhTc0wkF9/dOSEZPpTUxcklpCpE2ZTvhjnXG6Rwn+bhEp9ysgnRNsdI11UrvLL939nzvVC+2RXJzIrYztjbbJfYOtMP2LVuLrcd2zjF3bB/Y3rJ12Y45xqfu/+H7IagsCnuOp7fbl+UK2mKnnTnm5f17vmQUi7CpH9Msxx/qotms8/pmUdWbtBQ4E48j8UPw4jfL/T8mrz4mqfjWoGH5+r/NGOs6tkHfg9g2q3SVVaXA/1j4vT8a6A/B94f4o4H+EFw1xB8N9IeAE+RyfvcX/9W7iwNOfG3q4jld5yIZvQA=",
        },
        {
            "url": "https://puzz.link/p?context/16/12/g1k12g2010k3q2h323i2p3i222i3h21l2i333l2m3j3m0l333i1l11h3i121i3p1i323h0q3k2121g20k1g",
            "test": False,
        },
    ],
}