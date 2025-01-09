"""The Geradeweg solver."""

from typing import List, Tuple

from noqx.puzzle import Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.loop import loop_segment, loop_sign, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def count_geradeweg_constraint(target: int, src_cell: Tuple[int, int]) -> str:
    """Generate a constraint to count the geradeweg clue."""
    r, c = src_cell
    rule = f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "T"), |{c} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "V"), |{r} - N1| + |{r} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "H"), |{c} - N1| + |{c} - N2| != {target}.\n'
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="clue"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="geradeweg"))
    solver.add_program_line(fill_path(color="geradeweg"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="geradeweg", adj_type="loop"))
    solver.add_program_line(single_loop(color="geradeweg"))
    solver.add_program_line(loop_sign(color="geradeweg"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        solver.add_program_line(loop_segment((r, c)))
        solver.add_program_line(f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| != |{c} - N2|.')
        if num == "?":
            solver.add_program_line(f"geradeweg({r}, {c}).")
            continue

        assert isinstance(num, int), f"Clue at ({r}, {c}) must be an integer or '?'."
        solver.add_program_line(count_geradeweg_constraint(num, (r, c)))
        if num > 0:
            solver.add_program_line(f"geradeweg({r}, {c}).")
        else:
            solver.add_program_line(f"not geradeweg({r}, {c}).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Geradeweg",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VTPb5swFL7zV1Q++2BjIMSXKeuaXhj70UxVhVBFUq9FI2MjYasc8b/nvQetoeplh1WdNIG/fN97D+fzs+zdz7ZoDJcCXxVz+IUnkDENP45oiOFZlfvK6BO+aPd3dQOE8w/LJf9aVDvjZUNV7h3sXNsFt+c6Y5Jx5sOQLOf2kz7Y99qm3F5AinEJsaQv8oGeOXpJeWSnfVAK4GnPI6BXQDdls6nMddJP9FFndsUZ/s9b+hop29a/DBt8oN7U23WJgXWxh8Xs7sofQ2bX3tTf2qFW5h23i95u8oxd5ewi7e0i+1t2q/K7uX/O6TzvOuj4Z/B6rTO0/cXR2NELfQBM9YEpAZ8qHvWbwtQcpP8ogxlI6WQ8lVjsZIhTORmhdFNF4SQ7CybZGGd2UgofVySgX4+RaPK9FGgtcFpifjSDL6d5Wugor9DPKB+gHuWDJ/NRK8b6ieMQ69mbkWNaMVMPEWi4pLZfES4JfcIV7Aq3ivAdoSAMCROqOSO8JDwlDAgjqpnhvv7Rzr+AnUz1N8j0Cf+9WO5lLIEzd5LWzbao4OSl7XZtmgcNt1znsXtGA04TXJr/L76Xv/iw++K1HYLXZgeOJbs1TXFjfptblntH",
        },
        {
            "url": "https://puzz.link/p?geradeweg/v:/17/17/0000i000i0000000i3g0g2i000000g1m3g000000j3g2j0000000g1k1g00000000000i00000000j0k0h2g0g2g1i.g.h4l1g3q2g2g2g0h2h0g2k1g00k00h3g0h000h1h000h0000000k000000000000g2g2g0000000000000i000000000000000g0000000000000000g00000000",
            "test": False,
        },
    ],
}
