"""The Spiral Galaxies solver."""

import json
from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import grid, edge, display
from .utilsx.helper import tag_encode
from .utilsx.rule import adjacent, reachable_source_edge
from .utilsx.solution import solver


def galaxy_constraint(glxr: int, glxc: int) -> str:
    """Generate a constraint for spiral galaxies."""
    r, c = (glxr - 1) // 2, (glxc - 1) // 2
    tag = tag_encode("reachable", "adj", "edge")
    rule = f":- grid(R, C), {tag}({r}, {c}, R, C), not {tag}({r}, {c}, {glxr} - R - 1, {glxc} - C - 1)."
    rule += f":- grid(R, C), {tag}({r}, {c}, R, C), horizontal_line(R, C), not horizontal_line({glxr} - R, {glxc} - C - 1).\n"
    rule += f":- grid(R, C), {tag}({r}, {c}, R, C), vertical_line(R, C), not vertical_line({glxr} - R - 1, {glxc} - C).\n"
    return rule.strip()


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
        excluded = [(r1, c1) for r1, c1 in reachables if (r1, c1) != (r, c)]
        solver.add_program_line(reachable_source_edge((r, c), excluded))

    tag = tag_encode("reachable", "adj", "edge")
    spawn_points = ", ".join(f"not {tag}({r}, {c}, R, C)" for r, c in reachables)
    solver.add_program_line(f":- grid(R, C), {spawn_points}.")

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
