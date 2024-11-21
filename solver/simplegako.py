"""The Simplegako solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, fill_num, grid
from noqx.solution import solver


def simplegako_fill_constraint() -> str:
    """Generate a constraint for the number filling in simplegako."""
    return (
        ":- number(R, C, N), RC = #count { R1 : number(R1, C, N) }, CC = #count { C1 : number(R, C1, N) }, N != RC + CC - 1."
    )


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(fill_num(_range=range(1, puzzle.row + puzzle.col)))
    solver.add_program_line(simplegako_fill_constraint())

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Simplegako",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VNNT4NAEL3zK5o9z4FdPtrurdbWS0Vra5qGkIZWTIkQFIoxS/jvnR1QEqMHTdQezGReHm9n2TcsUzyVYR6Bi2ENwASOIVyXkts2pdnGMj4kkezBqDzssxwJwNV0CvdhUkSG31YFRqWGUs1BXUifcQZMYHIWgJrLSl1K5YFa4BIDjtqsKRJIJx1d0bpm40bkJnKv5UjXSHdxvkuizaxRrqWvlsD0OWe0W1OWZs8Ra33o512WbmMtbMMDNlPs48d2pSjvsoeyreVBDWr0uV2rs6tpY1ezD+zqLn7Y7jCoa/zsN2h4I33t/bajg44uZIXoyYoJV2/to5fmbpglXltvBdt6Jzi2FqxOcB0t2J3Qp5e+CXgUpwPXhFNCQbhEP6AswnNCk9AhnFHNhHBFOCa0CV2q6euOvtTzL9jxhaABasL5Pg8Mn3lluo3ynpflaZgwHKvaYC+M0rewyP6ftD+aNH0F5qn9e6dmB6chMI4=",
        }
    ],
}
