"""The Compass solver."""

from typing import Union

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


def compass_constraint(r: int, c: int, label: str, num: Union[int, str]) -> str:
    """Generate a compass constraint."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    constraint = {
        f"corner_{Direction.TOP}": f"R < {r}",
        f"corner_{Direction.LEFT}": f"C < {c}",
        f"corner_{Direction.BOTTOM}": f"R > {r}",
        f"corner_{Direction.RIGHT}": f"C > {c}",
    }
    rule = ""
    if label in constraint:
        rule = f":- #count{{ (R, C): {tag}({r}, {c}, R, C), {constraint[label]} }} != {num}."

    return rule


class CompassSolver(Solver):
    """The Compass solver."""

    name = "Compass"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VRBj9o8EL3zK5DPPsSJSZxcKrqFXrZsW6hWqyhCgc1+rAoKJaSqgvjv+2aSEAJUW3Ul9B0qk9F7Mx7z7Bk7+5HHm0T6GI6RllQYjrH4M5p+VjUmz9tlEnRlP98u0g2AlHfDoXyKl1nSCatZUWdX+EHRl8XHIBS2kPwpEcniS7ArPgXFSBZjhITU8N0CKSFtwEED7zlO6KZ0Kgt4BOwDAz4AztPVOs6y0vE5CIuJFPQ37zmZoFilPxNRrsAcKbNncsziLfaSLZ7XVSTLH9PveTVXRXtZ9Eu1g1ot/Uul1mnUEizVErqgljbxVrXJ439Jls8uSfWj/R4n/hVip0FIur810DRwHOyE0pYINMgo2MEqcvVs+ELRZV1EVZvaoG5NHBC/Ilq3Jupem7qgpibeccw1lNmrCeWh5UpCWUcTW3me1VLqWaTUrgnpPIqR0obapk19UK8iDq3q1KS1e8N7xI0oCSnVNSGl1Z8b3l9N3FLlu3oNt72k2xJqXBJKi6IeD6iHprDi0h+6RWiSf+o0lHnmJCWnTp92cepUXMxz7/kCUDbkfrHZTtBPsnDYfmBrse2xveU5A7b3bG/YarYuz/GoI/+wZ4+btTyiv5MjHA9F9w226HvSViiS86rE0EYHnwz07f/JE3VCMc43T/E8weswwDvRHaWbVbwEG+WrWbJp+HgRrxOB93nfEb8Ef9T4eIb/PdlXf7Lp9K0rX4K33skQJ3u4P7K4k2KdT+PpPEV34fgojGt2OfBK3u/DVz8D3PtD5aPOCw==",
        },
        {
            "url": "https://puzz.link/p?compass/10/10/j.222h.112i2122t1211g2212g11.1i2222m2222t2111g222.g2222h2212q1222l2221k111.2..2l1.21h",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))

        all_src = {(r, c) for (r, c, _, _) in puzzle.text}
        fail_false(len(all_src) > 0, "No clues found.")
        for r, c in all_src:
            self.add_program_line(f"not hole({r}, {c}).")
            current_excluded = [src for src in all_src if src != (r, c)]
            self.add_program_line(
                grid_src_color_connected((r, c), exclude_cells=current_excluded, color=None, adj_type="edge")
            )

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            if label and isinstance(num, int):
                self.add_program_line(compass_constraint(r, c, label, num))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

            for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
                d = Direction.LEFT if c1 != c else Direction.TOP
                self.add_program_line(f'{prefix}edge({r2}, {c2}, "{d}").')

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
