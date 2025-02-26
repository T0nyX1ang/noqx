"""The Simplegako solver."""

from noqx.puzzle import Puzzle
from noqx.rule.common import display, fill_num, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.solution import solver


def simplegako_fill_constraint() -> str:
    """Generate a constraint for the number filling in simplegako."""
    return (
        ":- number(R, C, N), RC = #count { R1 : number(R1, C, N) }, CC = #count { C1 : number(R, C1, N) }, N != RC + CC - 1."
    )


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(fill_num(_range=range(1, puzzle.row + puzzle.col)))
    solver.add_program_line(simplegako_fill_constraint())

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))

    return solver.program


__metadata__ = {
    "name": "Simplegako",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VNNb6MwEL3zKyKf54BtIIlv2TTpJaUfSRVFCEUkpQoqiC2EqjLiv2c80CJV28NW2m0O1WieHs9j/AYz5XMVFTF4GHIENnAM4XmU3HEo7S5WyTGN1QAm1fGQF0gArudzeIzSMraCriq0aj1WegL6UgWMM2ACk7MQ9K2q9ZXSPuglLjHgqC3aIoF01tM1rRs2bUVuI/c7jnSDdJ8U+zTeLlrlRgV6Bcyc84t2G8qy/CVmnQ/zvM+zXWKEXXTEZspD8rtbKauH/KnqannYgJ58blf2dg1t7Rr2B7umi39sdxw2DX72OzS8VYHxft/TUU+Xqkb0Vc2EZ7YO0Ut7N0yKt9Y7wZEfBNcxguwFzzWC0wtDeum7gEdxOnBDOCcUhCv0A1oSXhDahC7hgmpmhGvCKaFD6FHN0HT0Vz3/BzuBEDRAbbhf56EVML/KdnEx8PMii1KGY9VY7JVRBhKLnJ9J+6ZJM1dgn9u/d252cBpC6wQ=",
        }
    ],
}
