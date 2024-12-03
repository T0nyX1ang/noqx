"""The Sukoro solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
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

    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert d == Direction.CENTER, "The symbol should be placed in the center."
        if symbol_name == "ox_E__1":
            solver.add_program_line(f"not white({r}, {c}).")
        if symbol_name in ("ox_E__4", "ox_E__7"):
            solver.add_program_line(f"white({r}, {c}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Sukoro",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VRNb9pAEL37V0Rz3oPXuxjjG02hF+q0hSpClmUZ6goUkKnBVbSI/56ZsdVlIzikahpVqux9vPnY4Xn2Y/+jKepSSJ9eFQn8xUfLiEcQhTz87pmtD5syvhHD5rCqaiRC3I3H4nux2Zde2mVl3tEMYjMU5kOcggQBAQ4JmTCf46P5GJtEmCmGQEj0TdqkAOnI0nuOE7ttndJHnnQc6Rzpcl0vN2U+aT2f4tTMBND/vOPZRGFb/Syh00H2stou1uRYFAf8mP1qvesi++Zb9dB0uTI7CTN8JldbucrKJdrKJXZBLn0Fya0e89ErSB1kpxO2/AuKzeOUdH+1NLJ0Gh8Rk/gISuJUhevMqwJKoUnL3pkDx9RkBr/MHs210dB3SoWBE+3TXBuVfuTUkoFbTCqqdm6TsrP5qu/GdejW6z233U+RoT6LYzMkt2TOOGYMGGfYMWEU43tGn7HHOOGcEeM94y2jZgw5p089f9GqnMuBrhF2y4Am6dp6XklxqtobwH16/54v81JImu2irG+Sqt4WGzw601WxKwHvp5MHj8CDd5f+f2W9wZVF7fd/+4i8zYlNzVTgCTF3AnZNXuTLCvcV9o38Wl/2X8t/qf9a/cv++ZU686v5f8D/11cLLyzcWQ9VXUHmPQE=",
        },
        {"url": "https://puzz.link/p?sukoro/11/11/p2324d14e3b2b3g3b1h31c13h2b3g1b2b1e23d1434p", "test": False},
    ],
}