"""The Meandering Numbers solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, avoid_num_adjacent
from noqx.solution import solver


def meander_constraint(_id: int, area_size: int) -> str:
    """Generate a constraint for the meandering numbers."""
    if area_size == 1:
        return f":- area({_id}, R, C), not number(R, C, 1)."

    mutual = f"area({_id}, R, C), area({_id}, R1, C1), number(R1, C1, N1), adj_4(R, C, R1, C1)"
    rule = f"meander({_id}, R, C) :- number(R, C, N), #count {{ R1, C1 : {mutual}, |N - N1| = 1 }} != 2."
    rule += f":- area({_id}, R, C), number(R, C, 1), #count {{ R1, C1 : {mutual}, N1 = 2 }} != 1."
    rule += f":- area({_id}, R, C), number(R, C, {area_size}), #count {{ R1, C1 : {mutual}, N1 = {area_size - 1} }} != 1."
    rule += f":- area({_id}, R, C), meander({_id}, R, C), not number(R, C, 1), not number(R, C, {area_size})."
    return rule


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.row == puzzle.col, "This puzzle must be square."
    n = puzzle.row

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(n, n))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_num_adjacent(adj_type=8))
    solver.add_program_line(unique_num(_type="area", color="grid"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, (ar, _) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i))
        solver.add_program_line(meander_constraint(_id=i, area_size=len(ar)))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Meandering Numbers",
    "category": "num",
    "aliases": ["meanderingnumbers"],
    "examples": [
        {
            "data": "m=edit&p=7VbRaiM3FH33VwQ960EazUijecumTl+ybrfJEoIxwUlmE1M7bu24LGP87zlXOsKwBMpSloZS7JGPNVfnXN17Rvb2z91802tr5e1abTSQrhufLmurdBm+rhYvy7470ae7l6f1BkDrX87P9Zf5ctuPpoyajfZD7IZTPfzcTZVVWlW4rJrp4VO3Hz52w1gPl7iltMXcRQ6qAMdHeJ3uCzrLk9YAT4gBbwDvF5v7ZX97kWd+7abDlVai8yGtFqhW6796xTzk+/16dbeQibv5CzazfVr8wTvb3cP69x1j7eygh9Oc7uSNdN0xXYE5XUFvpCu7+MHpxtnhgLL/hoRvu6nk/vkI2yO87PYYJ91e2brBWodmS2swadOtmzSep7FK4xVW6sGl8ac0mjQ2abxIMWMQVrXTVdOqrkLD60ZX3hAH4Io4AtcZN62ugsvYG2AklHAFHIhr4EgMzpacAVottQLmY5mHVqRWgFakVttqZ6gVDTC1YgVMrVgDZy3EamczP2K1qzI/YoEzP2KBMz9itXOZH7HAmR+xwJkfscDkd+Cvye/A35Dfgb8hvwN/Q/4a/J78Dfg9+Rvwe/I34Pfkx7Prgs0Y9XSsJ9bhIaeWB2dLTg+tlloB/C35gxwKnhi5sbbgAGZMi71E7qVFDpE5oJ51qWfEeWKZT2yBs25tDHDpO3rNfVXQrULpo/iBvZO+B/Y0iDdKPDwQcp74PPpH/BCKT8Rv9JJ4o9TBYI+m9FT8wJqIBwxrYsQb3K/4wbAmBnWmf5I3TPGM+K14CbW11LKoW6mDHLi29BrYFSyeYQ7iE8ccnPiHOYhnHHNwyKF4TPzjiq/Ek8UPWNsUz4jfuNZDl89m8knxmIcun1N8Hv0m/vFlLXSL9zx0PXXFV8WH4qvAvbfiPa6N0C1ekmcwUjeKl6gbER9LfISXhAeHzXU6cs7SWKfRp6MoyBH3XYfgPz/1/jadKbopv6jfvpr/7uxsNFXjh8f+ZLLerOZL/FxNdqu7flO+4//BYaS+qnSlX6D6/78M/9JfBmmBeW/PzHtLB0+xWvXz54d+s3h+PHlObt6q2egV",
        },
        {
            "url": "https://puzz.link/p?meander/15/15/4i894gi914i2944i894gi914i2944i894gi914i294000000vvv000000vvv000000vvv000000vvv000000i7j1j2g8j2j3l1j6j9l6j5j9g5j6j8l3j1j4g9j9j4l2j3j4l2j7j9g8j7j3l8j4j9g5j3j6l1j6j7l1j2j4g6j9j9i",
            "test": False,
        },
    ],
}
