"""The Tents solver."""

import itertools
from typing import List, Tuple

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.solution import solver

neighbor_offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))


def identical_adjacent_map(known_cells: List[Tuple[int, int]], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate n * (n - 1) / 2 constraints and n rules to enfroce identical adjacent cell maps.

    A grid fact and an adjacent rule should be defined first. n is the number of known source cells.
    """
    rules = "\n".join(
        f"{{ map_{r}_{c}(R, C): adj_{adj_type}(R, C, {r}, {c}), {color}(R, C) }} = 1 :- grid({r}, {c})."
        for r, c in known_cells
    )  # n rules are generated
    constraints = "\n".join(
        f":- map_{r1}_{c1}(R, C), map_{r2}_{c2}(R, C). " for (r1, c1), (r2, c2) in itertools.combinations(known_cells, 2)
    )  # n * (n - 1) / 2 constraints are generated
    return rules + "\n" + constraints


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="tents__2"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_adjacent_color(color="tents__2", adj_type=8))

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top number
        assert isinstance(num, int), "TOP clue must be an integer."
        solver.add_program_line(count(num, color="tents__2", _type="col", _id=c))

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left number
        assert isinstance(num, int), "LEFT clue must be an integer."
        solver.add_program_line(count(num, color="tents__2", _type="row", _id=r))

    all_trees: List[Tuple[int, int]] = []
    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert d == Direction.CENTER, "The symbol should be placed in the center."
        if symbol_name == "tents__1":
            all_trees.append((r, c))
            solver.add_program_line(f"not tents__2({r}, {c}).")
        if symbol_name == "tents__2":
            solver.add_program_line(f"tents__2({r}, {c}).")

    solver.add_program_line(identical_adjacent_map(all_trees, color="tents__2", adj_type=4))
    solver.add_program_line(count(len(all_trees), color="tents__2", _type="grid"))
    solver.add_program_line(display(item="tents__2"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Tents",
    "category": "var",
    "examples": [
        {
            "data": "m=edit&p=7VZNj9owEL3nV6x89iF2PpzkRrfLXijbFqoViiIUaCpQoaGQVJUR/31nJqlCYl+K1O1lZTyaeR5n3oy/OP2s82PBRYA/L+IuF9BCN6IuIrCh/2nzbbUrkjs+qqtNeQSF86fxmH/Ld6fCSXEmtMw56zjRI64fk5QJxpmELljG9afkrD8kesr1DIYY+HI9aZwkqA+d+kzjqN03oHBBn7Y6qAtQ19vjelcsJw3yMUn1nDOM845mo8r25a+CtTzQXpf71RaBVV5BMqfN9tCOnOqv5fe69RXZhetRQ3dhoet1dFFt6KJmoYtZIN2q+FGdbuLazjRpxtnlAuX+DESXSYqcv3Rq1Kmz5AxympyZL2CqhHWiFWG+BNPrTL9vhmDiojZm4PZGA/zUldn/VBD3AokAP31lx+je2TJSV9OBrCDKC6AcYhzAu/qx0DMhjNeHlDkxCgwojgxIuJjpELP4CYufxMSGGCY/wDxMeID5FowKOcAsJRGWmghliRs1i9rDYhtmxpWumZv0zLjSkpuknTfAlFk/aVk1qSxxLblJZS6vVGZuUplrKZUl32jID7bkmDamJDmH48W1R/I9SZdkQHJCPg8kn0nek/RJhuSj8ID+1RHunQ0iKP89wTRsXgZbU28jt4xkTsqm9X5VHO+m5XGf7+CCn23yQ8HgBb047DejTnei//aovvKjiqV3bz6X/+eaSKGq8G9NP3F2qJf5cl3CnnKzV2cJ10Vb3cx5AQ==",
        }
    ],
}
