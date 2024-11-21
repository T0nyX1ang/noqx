"""The Sukoro solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, fill_num, grid, invert_c
from noqx.rule.neighbor import adjacent, avoid_num_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def num_count_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """Generate a constraint for counting the number of adjacent black cells."""
    return f":- number(R, C, N), N != #count {{ R1, C1 : adj_{adj_type}(R, C, R1, C1), {color}(R1, C1) }}."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(fill_num(_range=range(0, 5), color="white"))
    solver.add_program_line(invert_c(color="white", invert="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(num_count_adjacent(color="black"))
    solver.add_program_line(avoid_num_adjacent())

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"not white({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"white({r}, {c}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Sukoro",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VXfb9owEH7PX1Hdsx/i2ITgN9aVvbB0G0xVFUUoZKmKGuQukGky4n/v3SVb8ESl7WGtJk3BH9/9sPP5Dpvd17ZoKiFD+qhE4Dc+WiY8oiTmEfbPcrOvK3Mhpu3+3jZIhLiezcRdUe+qIOuz8uDgJsZNhXtnMpAgIMIhIRfuozm498alwi0wBEKib94lRUivBnrDcWKXnVOGyNOeI71FWm6asq5W887zwWRuKYDe84ZnE4Wt/VZBr4Ps0m7XG3Ksiz1uZne/eewju/aLfWj7XJkfhZt2chc/5OpBrhrkEu3kEjsjl3bxl+VO8uMRy/4JBa9MRto/DzQZ6MIcEFNzACVxqsJec2dAKTSp9b058UxNZvTTHNHcIRqH3lJx5EXHNHeIyjDx1pKRv5hUtNqpTcpO5quxH9exv97oV9vfioz1SRyLIbkkt4wzxohxiRUTTjG+ZQwZR4xzzrlivGG8ZNSMMeeMqea/2RWgbWusNKqLuha9gLZMdefdf0b/ni8PMli0zV1RVng80na7rpqL1Dbboga8j44BfAce/EvS/6+oV7qiqAXhH11Ur39CM6wunhN3LeCxXRWr0taA/3KC/Fqf9z+Xf8b/4rvFY4+debCNhTx4Ag==",
        },
        {"url": "https://puzz.link/p?sukoro/11/11/p2324d14e3b2b3g3b1h31c13h2b3g1b2b1e23d1434p", "test": False},
    ],
}
