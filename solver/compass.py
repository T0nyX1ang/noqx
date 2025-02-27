"""The Compass solver."""

from typing import Union

from noqx.puzzle import Color, Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected
from noqx.solution import solver


def compass_constraint(r: int, c: int, pos: str, num: Union[int, str]) -> str:
    """Generate a compass constraint."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    constraint = {"sudoku_4": f"R < {r}", "sudoku_6": f"C < {c}", "sudoku_7": f"R > {r}", "sudoku_5": f"C > {c}"}
    rule = f":- #count{{ (R, C): {tag}({r}, {c}, R, C), {constraint[pos]} }} != {num}."

    return rule.strip()


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(defined(item="hole"))
    solver.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))

    all_src = set((r, c) for (r, c, _, _) in puzzle.text)
    fail_false(len(all_src) > 0, "No clues found.")
    for r, c in all_src:
        solver.add_program_line(f"not hole({r}, {c}).")
        current_excluded = [src for src in all_src if src != (r, c)]
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color=None, adj_type="edge"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, ("sudoku_4", "sudoku_5", "sudoku_6", "sudoku_7"))
        if pos and isinstance(num, int):
            solver.add_program_line(compass_constraint(r, c, pos, num))

    for (r, c, _, _), color in puzzle.surface.items():
        fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
        solver.add_program_line(f"hole({r}, {c}).")

        for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
            prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
            direc = "left" if c1 != c else "top"
            solver.add_program_line(f"{prefix}edge_{direc}({r2}, {c2}).")

    for (r, c, d, _), draw in puzzle.edge.items():
        solver.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))

    return solver.program


__metadata__ = {
    "name": "Compass",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VRBj9o8EL3zK5DPPsSJSZxcKrqFXrZsW6hWqyhCgc1+rAoKJaSqgvjv+2aSEAJUW3Ul9B0qk9F7Mx7z7Bk7+5HHm0T6GI6RllQYjrH4M5p+VjUmz9tlEnRlP98u0g2AlHfDoXyKl1nSCatZUWdX+EHRl8XHIBS2kPwpEcniS7ArPgXFSBZjhITU8N0CKSFtwEED7zlO6KZ0Kgt4BOwDAz4AztPVOs6y0vE5CIuJFPQ37zmZoFilPxNRrsAcKbNncsziLfaSLZ7XVSTLH9PveTVXRXtZ9Eu1g1ot/Uul1mnUEizVErqgljbxVrXJ439Jls8uSfWj/R4n/hVip0FIur810DRwHOyE0pYINMgo2MEqcvVs+ELRZV1EVZvaoG5NHBC/Ilq3Jupem7qgpibeccw1lNmrCeWh5UpCWUcTW3me1VLqWaTUrgnpPIqR0obapk19UK8iDq3q1KS1e8N7xI0oCSnVNSGl1Z8b3l9N3FLlu3oNt72k2xJqXBJKi6IeD6iHprDi0h+6RWiSf+o0lHnmJCWnTp92cepUXMxz7/kCUDbkfrHZTtBPsnDYfmBrse2xveU5A7b3bG/YarYuz/GoI/+wZ4+btTyiv5MjHA9F9w226HvSViiS86rE0EYHnwz07f/JE3VCMc43T/E8weswwDvRHaWbVbwEG+WrWbJp+HgRrxOB93nfEb8Ef9T4eIb/PdlXf7Lp9K0rX4K33skQJ3u4P7K4k2KdT+PpPEV34fgojGt2OfBK3u/DVz8D3PtD5aPOCw==",
        },
        {
            "url": "https://puzz.link/p?compass/10/10/j.222h.112i2122t1211g2212g11.1i2222m2222t2111g222.g2222h2212q1222l2221k111.2..2l1.21h",
            "test": False,
        },
    ],
}
