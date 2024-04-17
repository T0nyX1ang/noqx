"""Solve Fillomino puzzles."""

from typing import List

from .utilsx.common import display, edge, fill_num, grid
from .utilsx.encoding import Encoding, tag_encode
from .utilsx.neighbor import adjacent
from .utilsx.reachable import grid_branch_color_connected
from .utilsx.solution import solver


def fillomino_constraint():
    """Generate the Fillomino constraints."""
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")

    # propagation of number
    constraint = f"number(R, C, N) :- number(R0, C0, N), {tag}(R0, C0, R, C).\n"
    constraint += f":- number(R0, C0, N), #count {{ R, C: {tag}(R0, C0, R, C) }} != N.\n"

    # same number, adjacent cell, no line
    constraint += ":- number(R, C, N), number(R, C + 1, N), vertical_line(R, C + 1).\n"
    constraint += ":- number(R, C, N), number(R + 1, C, N), horizontal_line(R + 1, C).\n"

    # different number, adjacent cell, have line
    constraint += ":- number(R, C, N1), number(R, C + 1, N2), N1 != N2, not vertical_line(R, C + 1).\n"
    constraint += ":- number(R, C, N1), number(R + 1, C, N2), N1 != N2, not horizontal_line(R + 1, C).\n"

    # special case for 1
    mutual = ["horizontal_line(R, C)", "horizontal_line(R + 1, C)", "vertical_line(R, C)", "vertical_line(R, C + 1)"]
    constraint += f"{{ {'; '.join(mutual)} }} = 4 :- number(R, C, 1).\n"
    constraint += f"number(R, C, 1) :- {', '.join(mutual)}.\n"
    constraint += ":- number(R, C, 1), number(R1, C1, 1), adj_4(R, C, R1, C1).\n"

    return constraint.strip()


def fillomino_slow() -> str:
    """Generate the Fillomino rules for precise solving."""
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")

    count_edge = f"#count{{ R1, C1: {tag}(R, C, R1, C1) }} = N"
    slow = f":- adj_4(R, C, R0, C0), not {tag}(R, C, R0, C0), number(R0, C0, N), {count_edge}.\n"
    slow += f"{{ numberx(R, C, N) }} = 1 :- grid(R, C), not number(R, C, _), {count_edge}.\n"
    slow += f":- numberx(R, C, N), numberx(R1, C1, N), not {tag}(R, C, R1, C1), adj_4(R, C, R1, C1).\n"
    return slow.strip()


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(grid_branch_color_connected(color=None, adj_type="edge"))
    solver.add_program_line(fillomino_constraint())

    occurances = {1, 2, 3, 4, 5}
    for (r, c), num in E.clues.items():
        occurances.add(num)
        solver.add_program_line(f"number({r}, {c}, {num}).")

        if num == 1:
            solver.add_program_line(f"vertical_line({r}, {c}).")
            solver.add_program_line(f"horizontal_line({r}, {c}).")
            solver.add_program_line(f"vertical_line({r}, {c + 1}).")
            solver.add_program_line(f"horizontal_line({r + 1}, {c}).")

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.add_program_line(display(item="number", size=3))

    if E.params["fast"]:
        solver.add_program_line(fill_num(_range=occurances))
    else:
        solver.add_program_line(fillomino_slow())
        solver.add_program_line(display(item="numberx", size=3))

    solver.solve()

    return solver.solutions
