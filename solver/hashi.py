"""The Hashi solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import direction, display, grid, shade_c
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def hashi_bridge() -> str:
    """
    Generate a rule for hashi constraints.

    A grid fact and a direction fact should be defined first.
    """
    rule = "num(1..2)."
    rule += "{ grid_direction(R, C, D, N) : direction(D), num(N) } :- grid(R, C), hashi(R, C).\n"
    rule += ":- N != -1, number(R, C, N), #sum{ N1, D: grid_direction(R, C, D, N1) } != N.\n"

    rule += "pass_by_loop(R, C) :- grid(R, C), #count { D: grid_direction(R, C, D, _) } = 2.\n"
    rule += 'pass_by_straight(R, C) :- grid(R, C), num(N), grid_direction(R, C, "l", N), grid_direction(R, C, "r", N).\n'
    rule += 'pass_by_straight(R, C) :- grid(R, C), num(N), grid_direction(R, C, "u", N), grid_direction(R, C, "d", N).\n'
    rule += ":- grid(R, C), hashi(R, C), not number(R, C, _), not pass_by_straight(R, C).\n"
    rule += ":- grid(R, C), hashi(R, C), not number(R, C, _), not pass_by_loop(R, C).\n"

    # path along the edges should be connected
    rule += ':- grid(R, C), grid_direction(R, C, "l", _), not grid_direction(R, C - 1, "r", _).\n'
    rule += ':- grid(R, C), grid_direction(R, C, "u", _), not grid_direction(R - 1, C, "d", _).\n'
    rule += ':- grid(R, C), grid_direction(R, C, "r", _), not grid_direction(R, C + 1, "l", _).\n'
    rule += ':- grid(R, C), grid_direction(R, C, "d", _), not grid_direction(R + 1, C, "u", _).\n'

    # path along the edges should have the same bridges
    rule += ':- grid(R, C), grid_direction(R, C, "l", N1), grid_direction(R, C - 1, "r", N2), N1 != N2.\n'
    rule += ':- grid(R, C), grid_direction(R, C, "u", N1), grid_direction(R - 1, C, "d", N2), N1 != N2.\n'
    rule += ':- grid(R, C), grid_direction(R, C, "r", N1), grid_direction(R, C + 1, "l", N2), N1 != N2.\n'
    rule += ':- grid(R, C), grid_direction(R, C, "d", N1), grid_direction(R + 1, C, "u", N2), N1 != N2.\n'

    # path inside the cell (not number) should have the same bridges, not sure if this is necessary
    rule += ':- grid(R, C), num(N), not number(R, C, _), grid_direction(R, C, "l", N), not grid_direction(R, C, "r", N).\n'
    rule += ':- grid(R, C), num(N), not number(R, C, _), grid_direction(R, C, "u", N), not grid_direction(R, C, "d", N).\n'

    adj = 'adj_loop(R0, C0, R, C) :- R = R0, C = C0 + 1, grid(R, C), grid(R0, C0), grid_direction(R, C, "l", _).\n'
    adj += 'adj_loop(R0, C0, R, C) :- R = R0 + 1, C = C0, grid(R, C), grid(R0, C0), grid_direction(R, C, "u", _).\n'
    adj += "adj_loop(R0, C0, R, C) :- adj_loop(R, C, R0, C0)."
    return rule + adj.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lrud"))
    solver.add_program_line(shade_c(color="hashi"))
    solver.add_program_line(hashi_bridge())
    solver.add_program_line(grid_color_connected(color="hashi", adj_type="loop"))

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(f"hashi({r}, {c}).")
        solver.add_program_line(f"number({r}, {c}, {num if isinstance(num, int) else -1}).")

    solver.add_program_line(display(item="grid_direction", size=4))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Hashiwokakero",
    "category": "loop",
    "aliases": ["bridges", "hashiwokakero"],
    "examples": [
        {
            "url": "https://puzz.link/p?hashi/19/14/2g2g3g3g2i2g3g2q2g2g1h3g2g3h2v2i3g2h1g2h1g2g3p2g23g2g2g2j2g2i2h2g3g3g33zh2h3g1h2g32h1g2g2h2j4g3h1h2l2g1j23g2h4g2g1h2h3g2o1g2h2p2g2i2k1g2g3g4j3h22g3h2",
            "test": False,
        },
        {
            "data": "m=edit&p=7VbNattAEL77KcyeWliodmclS7qlqdNL6v4kJQRhgp2ojYmNWjlui4zfPTMjh93ZpodCG3IIQsN8Oz/7zWg10vr7ZtbW2qTaGg25TrTBK0tynUOmLYz4TvbX6eJ2WZdDfbC5vW5aVLR+f3Skv8yW63pQ7b2mg21XlN2B7t6WlQKlleV7qruP5bZ7V3YT3Z2gSWmDa8eoGaUtqmOvnrGdtMN+0SSoT3o9Q/Uc1ctFe7msL477RB/KqjvVivZ5zdGkqlXzo1Z9GOPLZjVf0MJ8dovFrK8X3/aW9eaqudnsfc10p7uDnu74Abrg6ZLa0yXtf9G9niHVh5gW090OO/4JuV6UFdH+7NXcqyflFuWk3CqXUOgQiWlMgPmcxQXw0CG0HmbSmguYUjLvnMpUKaXyMCfnAEJEJB8JeyHdjTViL2MpPrSnEgOlcx47ig/sLt7fOIoIdmD+IabiA5xRRpEhkxWbjCKEx6iIV/KorkKysIm0WyPrtkbWaU28g+VOBRlA1oXveBzBhyTYI404pNRrEZFGrLk3AatRxGEU+Rfx07AF7eE9IKGTGHqAkSyBOyM9KCbIYeV5BStZAEjWAL9l5F4FezrqNs7Mexx1ClL5tCCXvQc+9AEu4jMFRfRCRjU4G72/lvx9Dc5SD0IsT7EDyhfYgfKFdsrnGeEYMTxMzlkesbQsT3HW6A5YvmGZsExZHrPPmOUZy0OWjmXGPiOaVn81zx6BTuX67+KfrvTZ+mz999bpoFLjq6/1cNK0q9kSv/6TzWpet/cY/7R2A/VL8Y0DwGj3/PP1+D9f1P3kqY2sp0YHh2jfxp/NzeymbpvhC4av5u0Cj/j6pZoO7gA=",
        },
    ],
}
