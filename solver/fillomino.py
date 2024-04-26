"""Solve Fillomino puzzles."""

from typing import Dict, List

from .core.common import display, edge, grid
from .core.encoding import Encoding, tag_encode
from .core.helper import extract_initial_edges
from .core.neighbor import adjacent
from .core.reachable import grid_src_color_connected, count_reachable_src
from .core.solution import solver


def fillomino_constraint() -> str:
    """Generate the Fillomino constraints."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")

    # propagation of number
    constraint = f"number(R, C, N) :- number(R0, C0, N), {tag}(R0, C0, R, C).\n"

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


def fillomino_filtered(fast: bool = True) -> str:
    """Generate the Fillomino filtered connection constraints."""
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")
    initial = f"{tag}(R, C, R, C) :- grid(R, C), not number(R, C, _)."
    propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), grid(R, C), not number(R, C, _), adj_edge(R, C, R1, C1)."

    # edge between two reachable grids is forbidden.
    constraint = f":- {tag}(R, C, R, C + 1), vertical_line(R, C + 1).\n"
    constraint += f":- {tag}(R, C, R + 1, C), horizontal_line(R + 1, C).\n"
    constraint += f":- {tag}(R, C + 1, R, C), vertical_line(R, C + 1).\n"
    constraint += f":- {tag}(R + 1, C, R, C), horizontal_line(R + 1, C).\n"

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


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(extract_initial_edges(E.edges))
    solver.add_program_line(fillomino_constraint())

    for (r, c), num in E.clues.items():
        solver.add_program_line(f"number({r}, {c}, {num}).")
        solver.add_program_line(grid_src_color_connected(src_cell=(r, c), color=None, adj_type="edge"))
        solver.add_program_line(count_reachable_src(target=int(num), src_cell=(r, c), color=None, adj_type="edge"))

        if num == 1:
            solver.add_program_line(f"vertical_line({r}, {c}).")
            solver.add_program_line(f"horizontal_line({r}, {c}).")
            solver.add_program_line(f"vertical_line({r}, {c + 1}).")
            solver.add_program_line(f"horizontal_line({r + 1}, {c}).")

    solver.add_program_line(fillomino_filtered())
    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.add_program_line(display(item="number", size=3))
    solver.add_program_line(display(item="numberx", size=3))
    solver.solve()

    return solver.solutions
