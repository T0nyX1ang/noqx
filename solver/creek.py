"""The Creek solver."""

from typing import List

from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def creek_covering(target: int, r: int, c: int, color: str = "black") -> str:
    """Generate a constraint to check the {color} covering of cells."""
    return f":- {{ {color}({r - 1}, {c - 1}); {color}({r - 1}, {c}); {color}({r}, {c - 1}); {color}({r}, {c}) }} != {target}."


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(grid_color_connected(color="not gray"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d, Direction.TOP_LEFT)
        validate_type(pos, "normal")
        assert isinstance(num, int), f"Clue at ({r}, {c}) must be an integer."
        solver.add_program_line(creek_covering(num, r, c, color="gray"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
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
        {
            "data": "m=edit&p=7VTLbts6FNzrKwyuWoALUqSeOzdNu/FVH3YRBIIQyA5dC5WgVraKlIb/PYdHQkXT2XRxgxQoaA7GQ3LOiKK4/9GXnaLcNz8RU0Y5NJlI7CIKsLOxrapDrdIZnfeHXdsBofRDRrdlvVdebhZCK7yjTlI9p/p9mhNOKPGxF1R/So/6v1RnVC9hiNAYtMUwyQd6PdEbHDfsahA5A54NPAR6C3RTdZta3S1gFJSPaa5XlJg6b3C1oaRpfyoy5jD/N22zroywLg/wLPtd9X0c2ff37bd+nMuLE9XzIe7yibhiimvoENew/yuuuv+qHp5KmhSnE+z4Z8h6l+Ym9peJxhNdpkfALD0SwcJxbUgBwVCwxCjCUrhvFHhzkxK4ii/cVf6Fs3/hLNDZniPRx1YC6dYKIqNISwnZhYI+thJxt3qEzmcKOtu1YnS28yS4ylIkc59CMnd/JIudWpJjHnsOd/dH+uh8pqDzmYLOdvUAMzNbcXdVBu7bkQFW/63AAeF4TG4R3yH6iCs4RVQLxLeIDDFAXOCca8QbxCtEiRjinMicwz86qc8QJw/GW+usRX+fVng5WfbdttwouCWyvlmrbpa1XVPWBG7kk0ceCPZcmPv93yX9/Je02X320j6AlxYHPkmyrTq1rX/NXu3aQ9n1s7Uqm9ek8B4B",
        },
    ],
}
