"""The Easy As solver."""

from typing import Dict, List

from .core.common import count, display, fill_num, grid, unique_num
from .core.encoding import Encoding
from .core.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    assert E.R == E.C, "Easy as puzzles must be square."
    n = E.R
    letters = E.params["letters"]
    rev_letters = {v: k + 1 for k, v in enumerate(letters)}

    solver.reset()
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=range(1, len(letters) + 1), color="white"))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(count(n - len(letters), _type="row", color="white"))
    solver.add_program_line(unique_num(_type="col", color="grid"))
    solver.add_program_line(count(n - len(letters), _type="col", color="white"))

    for c, letter in E.top.items():
        solver.add_program_line(
            f":- Rm = #min {{ R: grid(R, {c}), not white(R, {c}) }}, not number(Rm, {c}, {rev_letters[letter]})."
        )

    for c, letter in E.bottom.items():
        solver.add_program_line(
            f":- Rm = #max {{ R: grid(R, {c}), not white(R, {c}) }}, not number(Rm, {c}, {rev_letters[letter]})."
        )

    for r, letter in E.left.items():
        solver.add_program_line(
            f":- Cm = #min {{ C: grid({r}, C), not white({r}, C) }}, not number({r}, Cm, {rev_letters[letter]})."
        )

    for r, letter in E.right.items():
        solver.add_program_line(
            f":- Cm = #max {{ C: grid({r}, C), not white({r}, C) }}, not number({r}, Cm, {rev_letters[letter]})."
        )

    for (r, c), letter in E.clues.items():
        solver.add_program_line(f"number({r}, {c}, {rev_letters[letter]}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    for solution in solver.solutions:
        for rc, num in solution.items():
            solution[rc] = letters[int(num) - 1]

    return solver.solutions
