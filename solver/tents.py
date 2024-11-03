"""The Tents solver."""

import itertools
from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
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
    solver.add_program_line(shade_c(color="tents__2__0"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_adjacent_color(color="tents__2__0", adj_type=8))

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top number
        assert isinstance(num, int), "TOP clue must be an integer."
        solver.add_program_line(count(num, color="tents__2__0", _type="col", _id=c))

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left number
        assert isinstance(num, int), "LEFT clue must be an integer."
        solver.add_program_line(count(num, color="tents__2__0", _type="row", _id=r))

    all_trees: List[Tuple[int, int]] = []
    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name == "tents__1__0":
            all_trees.append((r, c))
            solver.add_program_line(f"not tents__2__0({r}, {c}).")
        elif symbol_name == "tents__2__0":
            solver.add_program_line(f"tents__2__0({r}, {c}).")
        else:
            solver.add_program_line(f"not tents__2__0({r}, {c}).")

    solver.add_program_line(identical_adjacent_map(all_trees, color="tents__2__0", adj_type=4))
    solver.add_program_line(count(len(all_trees), color="tents__2__0", _type="grid"))
    solver.add_program_line(display(item="tents__2__0"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Tents",
    "category": "var",
    "examples": [
        {
            "data": "m=edit&p=7VXNjpswEL7zFCuffcDmx8At3W56SelPUq0ihFYkpUrUpGyBVJWjvPvODFQE7EtXarWHlfFo5vOY+WYG4+bnqahLLgJ8vIi7XMAI3YimiMCG+Wes9u2hTG747NTuqhoUzj/M5/xbcWhKJ8OdMHLnrONEz7h+l2RMMM4kTMFyrj8lZ/0+0SnXS1hi4Mv1onOSoN4N6j2to3bbgcIFPe11UNegbvf19lA+LDrkY5LpFWcY5w3tRpUdq18l63mgva2Omz0Cm6KFZJrd/rFfaU5fq++n3lfkF65nHd21ha430EW1o4uahS5mgXTb8kfbPItrv9OkGeeXC5T7MxB9SDLk/GVQo0FdJmeQaXJmvoCtEvpEHWG+BNMbTH9shmBiUzszcEerAb7qyhy/KohHgUSAr76yY3QfbBmpq+1AVhDlNVAOMQ7gQ/1Y6JkQxhtDytwYBQYURwYkXMx0iln8hMVPYmJTDJOfYB4mPMF8C0aFnGCWkghLTYSyxI26po6w2IaZcaVr5iY9M6605Cbpy5tgyqyftHRNKktcS25Sme2VysxNKrOXUlnyjab84JOc04cpSa7geHHtkXxL0iUZkFyQzx3Je5K3JH2SIfkoPKB/dYSvz8Y/opOF3T1gG+p15TkruZOx9HTclPVNWtXH4gC/8+WueCwZ3JcXh/1mNOkP6L9eof/5CsXSuy/tFL40OvBf6MuYO08=",
        }
    ],
}
