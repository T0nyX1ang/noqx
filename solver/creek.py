"""The Creek solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def creek_covering(target: int, r: int, c: int, color: str = "black") -> str:
    """Generate a constraint to check the {color} covering of cells."""
    return f":- {{ {color}({r}, {c}); {color}({r + 1}, {c}); {color}({r}, {c + 1}); {color}({r + 1}, {c + 1}) }} != {target}."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(grid_color_connected(color="not gray"))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(creek_covering(num, r, c, color="gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Creek",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVNj9owEL3zK5BPrTSHJHY+b3S77YVm24VqtYoiFFhTUIOyDaTaGvHfdzyJGhPvoT2UqlJlPHo8P48fYxvvvzVFLcH19IdH4ICLTcSCOg996k7X5ttDKZMxTJrDpqoRANyksC7KvRxleiK2fHRUcaImoN4nGXMZMI96DupTclQfEpWCmuEQgwi5aSvyEF738I7GNbpqSddBnLY4QHiPcLWtV6VcTHEUmY9JpubA9DpvaLaGbFd9l6zzob+vqt1yq4llccDfst9sH7uRffNQfW06rZufQE1au7MX7PLeroatXY3+lF358EU+veQ0zk8nrPgtel0kmbb9uYdRD2fJEWOaHBl3Qj0XdyUAzIAJuRMPGdfVDDcZf6jx+FDjUR6TEU7ns2cos5lHeJZGWHksz77lxyeNmcePhkxAfszMAa1u5gkth6GtsdYKrRpGtLq5VmRpYvJzxliVj6nOhkY4xBirC4cqZmq8YeWFtV/Cs2dRVc80w8oLbmm4pbH2XbS7/FODh9GlI3lP8R1Fj+IcTywoTvEtRYeiT3FKmmuKdxSvKAqKAWlCfeZ/8VYwHwvuAQvwN0TtFbmAt8zv/i7PWvjvcfkoY7OmXhcriX9PabNbynqcVvWuKBk+BacRe2LUM64flv+vw+VfB11957feiL9/OTMsbBCCugH22CyKxaoqGWDZNI9XZ8hf3D3eYLbe1nJd/hi/2lSHom7GS1nsXrN89Aw=",
        },
    ],
}
