"""The Easy As solver."""

from typing import List

from .core.common import count, display, fill_num, grid, unique_num
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.row == puzzle.col, "Doppelblock puzzles must be square."
    n = puzzle.row
    letters = puzzle.param["letters"]
    rev_letters = {v: k + 1 for k, v in enumerate(letters)}

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=range(1, len(letters) + 1), color="white"))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(count(n - len(letters), _type="row", color="white"))
    solver.add_program_line(unique_num(_type="col", color="grid"))
    solver.add_program_line(count(n - len(letters), _type="col", color="white"))

    for (r, c), letter in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top letter
        assert isinstance(letter, str) and len(letter) == 1, "TOP clue should be a letter."
        solver.add_program_line(
            f":- Rm = #min {{ R: grid(R, {c}), not white(R, {c}) }}, not number(Rm, {c}, {rev_letters[letter]})."
        )

    for (r, c), letter in filter(lambda x: x[0][0] == n and x[0][1] >= 0, puzzle.text.items()):  # filter bottom letter
        assert isinstance(letter, str) and len(letter) == 1, "BOTTOM clue should be a letter."
        solver.add_program_line(
            f":- Rm = #max {{ R: grid(R, {c}), not white(R, {c}) }}, not number(Rm, {c}, {rev_letters[letter]})."
        )

    for (r, c), letter in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left letter
        assert isinstance(letter, str) and len(letter) == 1, "LEFT clue should be a letter."
        solver.add_program_line(
            f":- Cm = #min {{ C: grid({r}, C), not white({r}, C) }}, not number({r}, Cm, {rev_letters[letter]})."
        )

    for (r, c), letter in filter(lambda x: x[0][1] == n and x[0][0] >= 0, puzzle.text.items()):  # filter right letter
        assert isinstance(letter, str) and len(letter) == 1, "RIGHT clue should be a letter."
        solver.add_program_line(
            f":- Cm = #max {{ C: grid({r}, C), not white({r}, C) }}, not number({r}, Cm, {rev_letters[letter]})."
        )

    for (r, c), letter in filter(
        lambda x: x[0][0] < n and x[0][0] >= 0 and x[0][1] < n and x[0][1] >= 0, puzzle.text.items()
    ):  # filter center number
        solver.add_program_line(f"number({r}, {c}, {rev_letters[letter]}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Easy As ABC",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7ZRPb5tAEMXvfIpoz3NggGDYG03jXFz6x7aiCKEIu1SxaosWm6pay989M7OobHAvPaT1ocL79PxjZ/3Ywbv/3lVtDYj8CRPwgRxE17EMxECG31+LzWFb6yvIusNT05IBeD+dwpdqu6+9givpKr2jSbXJwNzpQqECFdBAVYL5qI/mnTY5mDndUhARm9lJAdnbwd7LfXY3FqJPPu892Qey60273taPM0s+6MIsQPHvvJFqtmrX/KhVn4O/r5vdasNgVR3oYfZPm2/9nX33ufna9XOxPIHJRnE5Th83HOKytXHZ/SYul71y3LQ8nWjbP1HgR11w9uVgk8HO9ZE010cVRlyaURbbGxXGDJYOmIxBwmA+gMhnsHAAjoGs4YDJGCQCnBxpwOBuAOiPaxDH0TA4q7LxnYXRhnGr4jOSyLa8ILIvzlPjWWRMZGdekHScJ5XNcldOZbd+VVFjUNrzIDoVDUQX1D0woehbUV/0WnQmc25F70VvRCPRWOZMuP9/9Ib8hThFlNgjw7kml0VKr1B5t1vV7VXetLtqq+h4O3nqp5JRhHxa/j/x/tGJxy3wL+2tvrQ49D8rvWc=",
            "config": {"letters": "AUGST"},
        }
    ],
    "parameters": {"letters": {"name": "Letters", "type": "text", "default": "ABC"}},
}
