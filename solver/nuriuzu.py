"""The Nuri-uzu solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.helper import tag_encode
from .core.neighbor import adjacent
from .core.reachable import grid_src_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def nuriuzu_constraint(glxr: int, glxc: int, adj_type: int = 4, color: str = "black") -> str:
    """Generate a constraint for spiral galaxies."""
    r, c = (glxr - 1) // 2, (glxc - 1) // 2
    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    rule = f":- grid(R, C), {tag}({r}, {c}, R, C), not {tag}({r}, {c}, {glxr} - R - 1, {glxc} - C - 1).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_rect(2, 2, color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="not black"))

    reachables = []
    for (r, c), symbol_name in puzzle.symbol.items():
        reachables.append((r, c))
        _, _, category = symbol_name.split("__")

        if category == "0":
            solver.add_program_line(nuriuzu_constraint(r * 2 + 1, c * 2 + 1, color="not black"))
            solver.add_program_line(f"not black({r}, {c}).")

        if category == "1":
            solver.add_program_line(nuriuzu_constraint(r * 2 + 2, c * 2 + 2, color="not black"))
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(f"not black({r + 1}, {c}).")
            solver.add_program_line(f"not black({r}, {c + 1}).")
            solver.add_program_line(f"not black({r + 1}, {c + 1}).")

        if category == "2":
            solver.add_program_line(nuriuzu_constraint(r * 2 + 2, c * 2 + 1, color="not black"))
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(f"not black({r + 1}, {c}).")

        if category == "3":
            solver.add_program_line(nuriuzu_constraint(r * 2 + 1, c * 2 + 2, color="not black"))
            solver.add_program_line(f"not black({r}, {c}).")
            solver.add_program_line(f"not black({r}, {c + 1}).")

    assert len(reachables) > 0, "Please provide at least one clue."

    for r, c in reachables:
        excluded = [(r1, c1) for r1, c1 in reachables if (r1, c1) != (r, c)]
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=excluded, adj_type=4, color="not black"))

    tag = tag_encode("reachable", "grid", "src", "adj", 4, "not black")
    spawn_points = ", ".join(f"not {tag}({r}, {c}, R, C)" for r, c in reachables)
    solver.add_program_line(f":- grid(R, C), not black(R, C), {spawn_points}.")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions
