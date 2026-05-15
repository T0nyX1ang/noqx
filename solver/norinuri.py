"""The Norinuri solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected
from noqx.rule.variety import nori_adjacent


class NorinuriSolver(Solver):
    """The Norinuri solver."""

    name = "Norinuri"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VXfj5NAEH7nrzDzPA8su1C6L6bWqy/VU1tzuRDScMjliDTUUozZhv/dmQGL9+NBjakxMct+fN/sbvh2YIfmc5vtC1Q+XzpGulMzKpYexJF0f2jr8lAV9hnO2sNdvSeCeLlY4G1WNYWXDLNS7+im1s3QvbIJKEAIqCtI0b2zR/fauhW6FQ0BKoot+0kB0YuRXsk4s3kfVD7xNwMnek00L/d5VWyWfeStTdwagZ/zQlYzhW39pYDBB+u83t6UHLjJDrSZ5q7cDSNN+7H+1ML3R3ToZg/smtGuHu3qk139tN3gj9itdvVTRqdp11HC35PVjU3Y9YeRxiNd2WPHjo6gfV76nFz0bwXCgAL8BQw6Yj09yQnL6CSn4YPlSk0oEo5aG9LxD5rHJ6M2mnQw6ogNmUGTSSVWrwUXgoHgmnaCTgu+FPQFQ8GlzLkQvBKcCxrBSOZMOBc/mS3QCmyAYGg3pk/dGbwluj+B91v478VSL4FVu7/N8oI+23m93dVNeSiAqkPnwVeQnmguNv8LxtkLBiff/6Wy8ffPZUJ51QrdJcKu3WSbvK6A/jb4O3FjHsXPvls67Kn3DQ==",
        },
        {"url": "https://puzz.link/p?norinuri/10/10/o.zt9g8lcg5zt.o", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("black"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_unknown_src("not black"))
        self.add_program_line(nori_adjacent(color="black"))

        all_src: List[Tuple[int, int]] = []
        for (r, c, d, label), _ in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            all_src.append((r, c))

        for (r, c, _, _), num in puzzle.text.items():
            current_excluded = [src for src in all_src if src != (r, c)]
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color="not black"))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num, (r, c), color="not black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
