"""Solve Fillomino puzzles."""

from typing import List

from .core.common import display, edge, grid
from .core.penpa import Puzzle, Solution
from .core.helper import extract_initial_edges, tag_encode
from .core.neighbor import adjacent
from .core.reachable import grid_src_color_connected, count_reachable_src
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
