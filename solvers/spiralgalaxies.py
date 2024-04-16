"""The Spiral Galaxies solver."""

from typing import List

from . import utilsx
from .utilsx.common import display, edge, grid
from .utilsx.encoding import Encoding, tag_encode
from .utilsx.neighbor import adjacent
from .utilsx.reachable import grid_src_color_connected
from .utilsx.solution import solver


def galaxy_constraint(glxr: int, glxc: int) -> str:
    """Generate a constraint for spiral galaxies."""
    r, c = (glxr - 1) // 2, (glxc - 1) // 2
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")
    rule = f":- grid(R, C), {tag}({r}, {c}, R, C), not {tag}({r}, {c}, {glxr} - R - 1, {glxc} - C - 1)."
    rule += f":- grid(R, C), {tag}({r}, {c}, R, C), horizontal_line(R, C), not horizontal_line({glxr} - R, {glxc} - C - 1).\n"
    rule += f":- grid(R, C), {tag}({r}, {c}, R, C), vertical_line(R, C), not vertical_line({glxr} - R - 1, {glxc} - C).\n"
    return rule.strip()


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


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
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=excluded, adj_type="edge", color=None))

    tag = tag_encode("reachable", "grid", "src", "adj", "edge")
    spawn_points = ", ".join(f"not {tag}({r}, {c}, R, C)" for r, c in reachables)
    solver.add_program_line(f":- grid(R, C), {spawn_points}.")

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
