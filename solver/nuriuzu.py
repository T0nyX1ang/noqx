"""The Nuri-uzu solver."""

from typing import List, Tuple

from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false, tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_src_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def nuriuzu_constraint(glxr: int, glxc: int, adj_type: int = 4, color: str = "black") -> str:
    """Generate a constraint for spiral galaxies."""
    r, c = (glxr - 1) // 2, (glxc - 1) // 2
    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    rule = f":- grid(R, C), {tag}({r}, {c}, R, C), not {tag}({r}, {c}, {glxr} - R - 1, {glxc} - C - 1).\n"
    return rule.strip()


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_rect(2, 2, color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="not black"))

    reachables: List[Tuple[int, int]] = []
    for (r, c, d, _), symbol_name in puzzle.symbol.items():
        fail_false(symbol_name.startswith("circle_SS"), "Invalid symbol type.")

        # there are no category = 1 for nuriuzu, because it is conflicting with the no 2x2 white rule.
        if d == Direction.CENTER:
            reachables.append((r, c))
            solver.add_program_line(nuriuzu_constraint(r * 2 + 1, c * 2 + 1, color="not black"))
            solver.add_program_line(f"not black({r}, {c}).")

        if d == Direction.TOP:
            reachables.append((r - 1, c))
            solver.add_program_line(nuriuzu_constraint(r * 2, c * 2 + 1, color="not black"))
            solver.add_program_line(f"not black({r - 1}, {c}).")
            solver.add_program_line(f"not black({r}, {c}).")

        if d == Direction.LEFT:
            reachables.append((r, c - 1))
            solver.add_program_line(nuriuzu_constraint(r * 2 + 1, c * 2, color="not black"))
            solver.add_program_line(f"not black({r}, {c - 1}).")
            solver.add_program_line(f"not black({r}, {c}).")

    fail_false(len(reachables) > 0, "Please provide at least one clue.")
    for r, c in reachables:
        excluded = [(r1, c1) for r1, c1 in reachables if (r1, c1) != (r, c)]
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=excluded, adj_type=4, color="not black"))

    tag = tag_encode("reachable", "grid", "src", "adj", 4, "not black")
    spawn_points = ", ".join(f"not {tag}({r}, {c}, R, C)" for r, c in reachables)
    solver.add_program_line(f":- grid(R, C), not black(R, C), {spawn_points}.")

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")
        else:
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display())

    return solver.program


__metadata__ = {
    "name": "Nuri-uzu",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VZRb5swEH7Pr5ju+R4wmAR4y7quL126jUxVhVDkULdBoyKDMFWO8t97PpiQViNNm7buoXL86eO7s/mwrXPab51qNIrQ/oIIPRTU5l7EXUT0TP1HW5eHSidvcNkddnVDBPFqhXeqavUsG5Ly2dHEiVmiuUgy8AG5C8jRfEqO5kNiUjQphQAlaZfEBKBP9Hyk1xy37KwXhUd8NXCiN0SLsikqvUnTXvqYZGaNYF/0lodbCg/1dw39OH4u6odtaYWtOtDHtLtyP0Ta7rb+2g25Ij+hWf7k1/oZ/AajX0t7v5Y5/Nphf+5X397rttu6zMb56USr/pnsbpLMOv8y0mikaXIkXDEKxpvkCKGkaQS9abRHjiEK3fLCKQsxd+uRN6G75/E9t5vAi536IhJum96E/ditx4H7vfHE/PHEPMIPoomAnAqE7k8Tge9aO9q197x3PuOathZNwPiO0WMMGS8555zxmvGMUTLOOWdhD8cvHh+QZEkiSFoV//lZ+kveMtmXpalGxes1+n9H81kGadfcqUJTBUt3aq+BborTDB6BexZQmny9PF7m8rA74P32FfIyJSmjtaXCYK4Q9t1GbYq6Avr7gayLZ/o/d091C9p92ajqXlXqsdQt5LMn",
        },
        {"url": "https://puzz.link/p?nuriuzu/10/10/iaaeztepexewezwepexewezzseezzj", "test": False},
    ],
}
