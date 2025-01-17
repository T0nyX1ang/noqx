"""The Skyscrapers solver."""

from typing import List

from noqx.puzzle import Puzzle
from noqx.rule.common import display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)

    fail_false(puzzle.row == puzzle.col, "This puzzle must be square.")
    n = puzzle.row
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=range(1, n + 1)))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(unique_num(_type="col", color="grid"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")

        if r == -1 and 0 <= c < puzzle.col:
            solver.add_program_line(f"blocked_t(R, {c}) :- number(R, {c}, N), number(R1, {c}, N1), R1 < R, N1 > N.")
            solver.add_program_line(f":- #count {{ R: blocked_t(R, {c}) }} != {n - int(num)}.")

        if r == puzzle.row and 0 <= c < puzzle.col:
            solver.add_program_line(f"blocked_b(R, {c}) :- number(R, {c}, N), number(R1, {c}, N1), R1 > R, N1 > N.")
            solver.add_program_line(f":- #count {{ R: blocked_b(R, {c}) }} != {n - int(num)}.")

        if c == -1 and 0 <= r < puzzle.row:
            solver.add_program_line(f"blocked_l({r}, C) :- number({r}, C, N), number({r}, C1, N1), C1 < C, N1 > N.")
            solver.add_program_line(f":- #count {{ C: blocked_l({r}, C) }} != {n - int(num)}.")

        if c == puzzle.col and 0 <= r < puzzle.row:
            solver.add_program_line(f"blocked_r({r}, C) :- number({r}, C, N), number({r}, C1, N1), C1 > C, N1 > N.")
            solver.add_program_line(f":- #count {{ C: blocked_r({r}, C) }} != {n - int(num)}.")

        if 0 <= r < puzzle.row and 0 <= c < puzzle.col:
            solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Skyscrapers",
    "category": "num",
    "aliases": ["building"],
    "examples": [
        {
            "data": "m=edit&p=7VRNb5tAEL3zK6I5z4GFBeO9uWnci0s/4iqKEIowpQoKiBRM1K7l/56ZgQYjtYce2vpQrffpvZkB3s6ut/vaZ22BSvHPj9BFYqiDUKZSnkx3HNtyXxXmAlf9/r5piSC+W6/xS1Z1hZPwkzRS52CXxq7QvjEJKEDwaCpI0X4wB/vW2BjtNaWAatFuhiKP6NVEbyTP7HIIKpd4PHKit0Tzss2r4m4zRN6bxG4R+Duv5GmmUDdPBYw+WOdNvSs5sMv2tJjuvnwcM13/uXnox1qVHtGufm3Xn+wyHewy+4ldXsUftrtMj0dq+0cyfGcS9v5potFEr82BMDYH8DU9qmm/ZGfAD0kuJhmRDF6kdueSs7CgdYyB0KOA/yKjxexlS87SQRqlUpyOJu1x/kRrzp/UB5ynw/hDR8HMupLPTe5UtDz5PC1XyaJvBdeCnuCWeoLWF3wt6AoGghupuRK8EbwU1IKh1Cy4q7/V979gJ9Hcy/ngbpxRJHUSiPt6V7QXcdPWWQV0aRwd+AYy5Sjp//fIP7pHeAvcczvV52aH/mfQPXzv8jZ7LNoOUucZ"
        }
    ],
}
