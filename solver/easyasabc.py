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
