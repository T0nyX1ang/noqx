"""The Spiral Galaxies solver."""

import json
from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import grid, edge, display
from .utilsx.rule import adjacent, reachable_edge
from .utilsx.solution import solver


def galaxy_constraint(glxr: int, glxc: int) -> str:
    """Generate a constraint for spiral galaxies."""
    r, c = (glxr - 1) // 2, (glxc - 1) // 2
    rule = f":- grid(R, C), reachable_edge(R, C, {r}, {c}), not reachable_edge({glxr} - R - 1, {glxc} - C - 1, {r}, {c})."
    return rule


def encode(string: str) -> Encoding:
    json_obj = json.loads(string)
    json_grid = json_obj["grid"]
    json_params = json_obj["param_values"]

    rows, cols = int(json_params["r"]), int(json_params["c"])
    clues = {}

    for i in range(2 * (rows + 1)):
        for j in range(2 * (cols + 1)):
            if f"{i},{j}" in json_grid:
                clues[(i, j)] = "*"  # galaxy variation

    return Encoding(rows, cols, clues)


def solve(E: Encoding) -> List:
    assert len(E.clues) > 0, "No clues provided!"

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(reachable_edge())

    reachables = []
    for (r, c), _ in E.clues.items():
        reachables.append(((r - 1) // 2, (c - 1) // 2))
        solver.add_program_line(galaxy_constraint(r, c))

        if r % 2 == 0 and c % 2 == 1:
            solver.add_program_line(f"not horizontal_line({r // 2}, {(c - 1) // 2}).")

        if r % 2 == 1 and c % 2 == 0:
            solver.add_program_line(f"not vertical_line({(r - 1) // 2}, {c // 2}).")

        if r % 2 == 0 and c % 2 == 0:
            solver.add_program_line(f"not horizontal_line({r // 2}, {(c - 1) // 2}).")
            solver.add_program_line(f"not horizontal_line({r // 2}, {(c - 1) // 2 + 1}).")
            solver.add_program_line(f"not vertical_line({(r - 1) // 2}, {c // 2}).")
            solver.add_program_line(f"not vertical_line({(r - 1) // 2 + 1}, {c // 2}).")

    for r, c in reachables:
        for r1, c1 in reachables:
            if (r, c) < (r1, c1):
                solver.add_program_line(f"not reachable_edge({r}, {c}, {r1}, {c1}).")

    spawn_points = ", ".join(f"not reachable_edge(R, C, {r}, {c})" for r, c in reachables)
    solver.add_program_line(f":- grid(R, C), {spawn_points}.")

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
