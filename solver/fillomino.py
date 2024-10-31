"""Solve Fillomino puzzles."""

from typing import List

from .core.common import display, edge, grid
from .core.helper import extract_initial_edges, tag_encode
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import count_reachable_src, grid_src_color_connected
from .core.solution import solver


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
    solver.add_program_line(extract_initial_edges(puzzle.edge, puzzle.helper_x))
    solver.add_program_line(fillomino_constraint())

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be an integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")
        solver.add_program_line(grid_src_color_connected(src_cell=(r, c), color=None, adj_type="edge"))
        solver.add_program_line(count_reachable_src(target=int(num), src_cell=(r, c), color=None, adj_type="edge"))

        if num == 1:
            solver.add_program_line(f"edge_left({r}, {c}).")
            solver.add_program_line(f"edge_top({r}, {c}).")
            solver.add_program_line(f"edge_left({r}, {c + 1}).")
            solver.add_program_line(f"edge_top({r + 1}, {c}).")

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
            "data": "m=edit&p=7VXPj5s8EL3zV6x89oGx+RVu6TbpJaVfm1SrFUIrkiVdVCj9SKgqR/nfdzxQRR5tD63Udg8r4qc3fjNm8rDh8P9Q9pUEbX86kb4EvEKtaEAQ0PCna1Mfmyq9kvPh+ND1SKR8t1zKfdkcKi+fsgrvZGapmUvzJs2FEpIGiEKa9+nJvE1NJs0aJSEB51bIQEiFdHGhN6Rbdj1Ogo88mzjSW6S7ut811d1qnPkvzc1GCnufV1RtqWi7b5UYyyjede22thPb8oh/5vBQf52Uw3DffR6mXCjO0sx/3q6+tGvp2K5lT7Rr/8UfbndWnM9o+wds+C7Nbe8fLzS50HV6QszSk9AzLMWnPj4ZEQROGLIwxtBujCl0ayNw1MitjVno1iZuOHOTZ64KviuDHzp3Bt/tE3xWD8rVga0HbD3FdGYaHg03P2A6swJi7eYzbyCOmM7WS1ynIWHrJWw95i4we4H5q5hfivmjmB9KuX4rxeq126/SrJ7tOuX4hxsVaLveEi4JFeEGd7M0mvA1oU8YEq4oZ0F4Q3hNGBBGlBPb8/BLJ+YvtJPriF6/T13hi/I7SuHlYj30+3JX4Xtzcf+pusq6vi0bjLKh3Vb9jxg/W2dPfBc0aBMGL1+yf/Qls4/Af26n87m1g+8Lsa+bpmvrL50ovEc=",
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
