"""Solve Fillomino puzzles."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import count_reachable_src, grid_src_color_connected
from noqx.solution import solver


def fillomino_constraint() -> str:
    """Generate the Fillomino constraints."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")

    # propagation of number
    constraint = f"number(R, C, N) :- number(R0, C0, N), {tag}(R0, C0, R, C).\n"

    # same number, adjacent cell, no line
    constraint += ":- number(R, C, N), number(R, C + 1, N), edge_left(R, C + 1).\n"
    constraint += ":- number(R, C, N), number(R + 1, C, N), edge_top(R + 1, C).\n"

    # different number, adjacent cell, have line
    constraint += ":- number(R, C, N1), number(R, C + 1, N2), N1 != N2, not edge_left(R, C + 1).\n"
    constraint += ":- number(R, C, N1), number(R + 1, C, N2), N1 != N2, not edge_top(R + 1, C).\n"

    # special case for 1
    mutual = ["edge_top(R, C)", "edge_top(R + 1, C)", "edge_left(R, C)", "edge_left(R, C + 1)"]
    constraint += f"{{ {'; '.join(mutual)} }} = 4 :- number(R, C, 1).\n"
    constraint += f"number(R, C, 1) :- {', '.join(mutual)}.\n"
    constraint += ":- number(R, C, 1), number(R1, C1, 1), adj_4(R, C, R1, C1).\n"

    return constraint.strip()


def fillomino_filtered(fast: bool = True) -> str:
    """Generate the Fillomino filtered connection constraints."""
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")
    initial = f"{tag}(R, C, R, C) :- grid(R, C), not number(R, C, _)."
    propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), grid(R, C), not number(R, C, _), adj_edge(R, C, R1, C1)."

    # edge between two reachable grids is forbidden.
    constraint = f":- {tag}(R, C, R, C + 1), edge_left(R, C + 1).\n"
    constraint += f":- {tag}(R, C, R + 1, C), edge_top(R + 1, C).\n"
    constraint += f":- {tag}(R, C + 1, R, C), edge_left(R, C + 1).\n"
    constraint += f":- {tag}(R + 1, C, R, C), edge_top(R + 1, C).\n"

    if fast:
        constraint += "{ numberx(R, C, 1..5) } = 1 :- grid(R, C), not number(R, C, _).\n"
        constraint += f":- numberx(R, C, N), #count{{ R1, C1: {tag}(R, C, R1, C1) }} != N.\n"
    else:
        constraint += (
            f"{{ numberx(R, C, N) }} = 1 :- grid(R, C), not number(R, C, _), #count{{ R1, C1: {tag}(R, C, R1, C1) }} = N.\n"
        )
    constraint += f":- numberx(R, C, N), numberx(R1, C1, N), not {tag}(R, C, R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- number(R, C, N), numberx(R1, C1, N), adj_4(R, C, R1, C1)."

    return initial + "\n" + propagation + "\n" + constraint


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(fillomino_constraint())

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be an integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")
        solver.add_program_line(grid_src_color_connected(src_cell=(r, c), color=None, adj_type="edge"))
        solver.add_program_line(count_reachable_src(target=int(num), src_cell=(r, c), color=None, adj_type="edge"))

        if num == 1:
            solver.add_program_line(f":- not edge_left({r}, {c}).")
            solver.add_program_line(f":- not edge_top({r}, {c}).")
            solver.add_program_line(f":- not edge_left({r}, {c + 1}).")
            solver.add_program_line(f":- not edge_top({r + 1}, {c}).")

    for r, c, d in puzzle.edge:
        solver.add_program_line(f":- not edge_{d.value}({r}, {c}).")

    for r, c, d in puzzle.helper_x:
        solver.add_program_line(f":- edge_{d.value}({r}, {c}).")

    solver.add_program_line(fillomino_filtered(fast=puzzle.param["fast_mode"]))
    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.add_program_line(display(item="number", size=3))
    solver.add_program_line(display(item="numberx", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Fillomino",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VNNj9MwEL3nV1Q+zyF2vrq+laXlUsLHFlWrKKrSNstGJASSBiFH+e87M0kxleAAEtADsvz0nj2jeeOP9nOXNTmEOLw5uCBxqDDkKX2fpzuNTXEqcz2DRXd6rBskAK9WK3jIyjZ3kikqdXpzo80CzAudCCWApxQpmDe6Ny+1icHc4ZYAiWtrZFKAQrq0dMv7xG7HRekijyeO9B7poWgOZb5bjyuvdWI2IKjOM84mKqr6Sy7GNNaHutoXtLDPTthM+1h8mnba7lh/6KZYmQ5gFj+361m7REe7xH5gl7r4w3Zv0mHAY3+Lhnc6Ie/vLJ1beqd7xFj3QilMpbvmmxHKR6msDC92PQ/l3MoAZfRN+pRrg/3oQgaXhQLKtTKkXM9KqmtlRHVtcES51mT0fSFsS3Jz94wrRsW4wd7BeIzPGV3GgHHNMUvGLeMto88YckxEp/dL5/sX7CSKjuI8gt/nqZOI5fF9PovrpspKfF9xV+3z5qzxQw+O+Cp48u34///4P/rjdAXutb3Ea7ODf0M8FGVZV8XHWqTOEw==",
            "config": {"fast_mode": False},
        },
        {
            "data": "m=edit&p=7VRNb9swDL3nVxQ68yDJXx+3rEt26dJtzVAUhhEkqbsac+YuqYdBQf57SVqtoyJG0XXrdhicEE96pEyT1Nt8b+brAhJ8vBgkKHy8WPI/9ukn7TMtb6siPYJhc3tdrxEAnI7HcDWvNsUgs175YGuS1AzBvEszoQXwX4kczMd0a96nZgLmDCkBCvdOECkBGuGog+fMEzpuN5VEPLEY4QXCZbleVsXspN35kGZmCoLe84ajCYpV/aMQbRivl/VqUdLGYn6LH7O5Lm8ss2ku66+N9VX5DsywP12vS5dgmy6hA+nSV/zhdJN8t8Oyf8KEZ2lGuX/uYNzBs3SLdpJuhY4x1MNOc2eETnDpPyw97S49dxk4sT4d1bEhxXZsGLlL1zmSDhu5sZH73sh9b+KyCbF7y9B1dr9XSffFSionWkk3XGny3+MflUQ9qonyKH6fdwus/P3zsCeKO3PBdsxWs51i48B4bN+ylWwDtifsM2J7zvaYrc82ZJ+IWv+s4Xh5OsKn+iYxDkeAhScQUAUIhD6WhoBCZVEJjoeH86c90FQzwqECTVNEOCDsWxwixlPYPwbtY88Ya8D4FieoXdL6SzyT8ZPVyfA4kr39J/i3dvJBJkaXX4qjSb1ezStUgUmzWhTr+zXK7m4gfgr+8yT6/5X4LykxtUC+8pV7qQJkZtRdSTCnIG6a2Xy2rHHUsIRM39/SPtpe3D7a3uVeur3eh2nUkR5CysMECs5hAgWo9/taVemL088kHuSoj7YK9Yv0E4dbWfzNqb362KI6i6uyqupV+a0W+eAO",
        },
        {
            "url": "https://puzz.link/p?fillomino/15/15/h1o5i8g2m6g3g7i3h4h1i1g6g4h2g3h4g2i5h2i4h3l4h1h5m4h2g2h6k7h3i3h7k7h2g2h3m2h1h5l3h4i3h3i-10g4h4g1h3g7g1i8h4h3i2g2g2m8g6i1o1h",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?fillomino/9/9/rb-134k-13i-13i7k5h-13k-13h8k6i-13i-13k9-13am2j",
            "test": False,
        },
    ],
    "parameters": {"fast_mode": {"name": "Fast Mode", "type": "checkbox", "default": True}},
}
