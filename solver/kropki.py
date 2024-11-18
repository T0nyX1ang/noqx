"""The Kropki solver."""

import itertools
from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import display, fill_num, grid, unique_num
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.row == puzzle.col, "Doppelblock puzzles must be square."
    n = puzzle.row

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=range(1, n + 1)))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(unique_num(_type="col", color="grid"))

    for r, c in itertools.product(range(puzzle.row), range(1, puzzle.col)):
        symbol_name = puzzle.symbol.get((r, c, Direction.LEFT))
        if symbol_name == "circle_SS__1":
            solver.add_program_line(f":- number({r}, {c - 1}, N1), number({r}, {c}, N2), |N1 - N2| != 1.")
        elif symbol_name == "circle_SS__2":
            solver.add_program_line(f":- number({r}, {c - 1}, N1), number({r}, {c}, N2), (N1 - N2 * 2) * (N1 * 2 - N2) != 0.")
        else:
            solver.add_program_line(
                f":- number({r}, {c - 1}, N1), number({r}, {c}, N2), (|N1 - N2| - 1) * (N1 - N2 * 2) * (N1 * 2 - N2) = 0."
            )

    for r, c in itertools.product(range(1, puzzle.row), range(puzzle.col)):
        symbol_name = puzzle.symbol.get((r, c, Direction.TOP))
        if symbol_name == "circle_SS__1":
            solver.add_program_line(f":- number({r - 1}, {c}, N1), number({r}, {c}, N2), |N1 - N2| != 1.")
        elif symbol_name == "circle_SS__2":
            solver.add_program_line(f":- number({r - 1}, {c}, N1), number({r}, {c}, N2), (N1 - N2 * 2) * (N1 * 2 - N2) != 0.")
        else:
            solver.add_program_line(
                f":- number({r - 1}, {c}, N1), number({r}, {c}, N2), (|N1 - N2| - 1) * (N1 - N2 * 2) * (N1 * 2 - N2) = 0."
            )

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Kropki",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VVNa9tAEL37V4Q972E/ZUk3N017SdUPOwQjhJFdFQvbyJWtUtb4v2d2JFCgs4cWklzKssPT0/PozXg/Tj+7sq14DEPHXHAJQxuFU4kEpxjGoj7vq/SGz7rztmkBcP454z/K/ama5IOomFxckroZdx/TnEnGmYIpWcHd1/TiPqVuyd0cXjEugbvvRQrg3Qgf8b1Htz0pBeBswACXADd1u9lXq/m8p76kuVtw5j/0Dn/uITs0vyo2GPHPm+awrj2xLs9QzGlbH4c3p+57s+sGrSyu3M16vxnhV49+Pez9ekT49WW8tN+kuF6h8d/A8SrNvfmHEcYjnKcXiBlGiXGZXpiWBvJI+NpoEVwzrSLgFcFPab0WNG80ncdYWm8DfiJF54l8fkofyB8F6ooCdU0DfqaB/LEM8AnNJwF94uuleLqfJqL7b7A/hH4a0GO9hD6m+2/igD6h67XCf/dPvRX0/2JFHOB9foKXdF1W0v200ucneEXXaxXdT6vodWID+8LqgB9NrytrAn4MtW5hc3/ALa4wLuAE4E5jfI9RYLQY71Fzh/ER4y1GgzFCzdSfIX91yjA8QJgFO3gHPD91XsheriK8w8ZhX/e5mOQs6w7rqr3JmvZQ7uG8nm/LY8XgarxO2G+GM9cgNv9vyze7Lf2fIP75znybzZVDe2F9P9tRnB27VbnaNLDMRPHqdmG/sV3bHHc1KyZP",
        },
        {
            "url": "https://puzz.link/p?kropki/17/17/i970j090443913a1033a299190319301330b0930004aa04163399c03i04d1d61d0d70d7d7941130i4dddddddddc003a34303d50c9cad23134900a5da411dc4014df090ad040jcc000c4900n7ddadbddc00dd90601a010630mdddd9",
            "test": False,
        },
    ],
}
