"""The Tentaisho (Spiral Galaxies) solver."""

from typing import List

from .core.common import display, edge, grid
from .core.penpa import Puzzle
from .core.helper import extract_initial_edges, tag_encode
from .core.neighbor import adjacent
from .core.reachable import grid_src_color_connected
from .core.solution import solver


def galaxy_constraint(glxr: int, glxc: int) -> str:
    """Generate a constraint for spiral galaxies."""
    r, c = (glxr - 1) // 2, (glxc - 1) // 2
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")
    rule = f":- grid(R, C), {tag}({r}, {c}, R, C), not {tag}({r}, {c}, {glxr} - R - 1, {glxc} - C - 1)."
    rule += f":- grid(R, C), {tag}({r}, {c}, R, C), horizontal_line(R, C), not horizontal_line({glxr} - R, {glxc} - C - 1).\n"
    rule += f":- grid(R, C), {tag}({r}, {c}, R, C), vertical_line(R, C), not vertical_line({glxr} - R - 1, {glxc} - C).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(extract_initial_edges(puzzle.edge, puzzle.helper_x))

    reachables = []
    for (r, c), symbol_name in puzzle.symbol.items():
        reachables.append((r, c))
        _, _, category = symbol_name.split("__")

        if category == "0":
            solver.add_program_line(galaxy_constraint(r * 2 + 1, c * 2 + 1))

        if category == "1":
            solver.add_program_line(galaxy_constraint(r * 2 + 2, c * 2 + 2))
            solver.add_program_line(f"not horizontal_line({r + 1}, {c}).")
            solver.add_program_line(f"not horizontal_line({r + 1}, {c + 1}).")
            solver.add_program_line(f"not vertical_line({r}, {c + 1}).")
            solver.add_program_line(f"not vertical_line({r + 1}, {c + 1}).")

        if category == "2":
            solver.add_program_line(galaxy_constraint(r * 2 + 2, c * 2 + 1))
            solver.add_program_line(f"not horizontal_line({r + 1}, {c}).")

        if category == "3":
            solver.add_program_line(galaxy_constraint(r * 2 + 1, c * 2 + 2))
            solver.add_program_line(f"not vertical_line({r}, {c + 1}).")

    assert len(reachables) > 0, "Please provide at least one clue."

    for r, c in reachables:
        excluded = [(r1, c1) for r1, c1 in reachables if (r1, c1) != (r, c)]
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=excluded, adj_type="edge", color=None))

    for (r, c), _ in puzzle.surface.items():
        solver.add_program_line(f"black({r}, {c}).")
        solver.add_program_line(f"vertical_line({r}, {c}).")
        solver.add_program_line(f"vertical_line({r}, {c + 1}).")
        solver.add_program_line(f"horizontal_line({r}, {c}).")
        solver.add_program_line(f"horizontal_line({r + 1}, {c}).")

    tag = tag_encode("reachable", "grid", "src", "adj", "edge")
    spawn_points = ", ".join(f"not {tag}({r}, {c}, R, C)" for r, c in reachables)
    solver.add_program_line(f":- grid(R, C), not black(R, C), {spawn_points}.")

    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions
