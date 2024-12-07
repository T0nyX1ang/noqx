"""The Rail Pool solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, direction, display, fill_path, grid
from noqx.rule.helper import full_bfs
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def len_segment_area(color: str = "grid") -> str:
    """
    Generate a rule to get the length of segments.
    """
    rule = 'nth_horizontal(R, C, 0) :- grid_direction(R, C, "r"), not grid_direction(R, C, "l").\n'
    rule += 'nth_horizontal(R, C, N) :- grid_direction(R, C, "l"), nth_horizontal(R, C - 1, N - 1).\n'
    rule += 'nth_vertical(R, C, 0) :- grid_direction(R, C, "d"), not grid_direction(R, C, "u").\n'
    rule += 'nth_vertical(R, C, N) :- grid_direction(R, C, "u"), nth_vertical(R - 1, C, N - 1).\n'

    rule += f'len_horizontal(R, C, N) :- nth_horizontal(R, C, 0), {color}(R, C + N), nth_horizontal(R, C + N, N), not grid_direction(R, C + N, "r").\n'
    rule += f'len_vertical(R, C, N) :- nth_vertical(R, C, 0), {color}(R + N, C), nth_vertical(R + N, C, N), not grid_direction(R + N, C, "d").\n'
    rule += f"len_horizontal(R, C, L) :- {color}(R, C), nth_horizontal(R, C, N), len_horizontal(R, C - N, L).\n"
    rule += f"len_vertical(R, C, L) :- {color}(R, C), nth_vertical(R, C, N), len_vertical(R - N, C, L).\n"

    rule += f"area_len(A, L) :- {color}(R, C), area(A, R, C), len_horizontal(R, C, L).\n"
    rule += f"area_len(A, L) :- {color}(R, C), area(A, R, C), len_vertical(R, C, L).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("railpool(R, C) :- grid(R, C).")
    solver.add_program_line(fill_path(color="railpool"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="railpool", adj_type="loop"))
    solver.add_program_line(single_loop(color="railpool"))
    solver.add_program_line(len_segment_area(color="railpool"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, list), "Please set all NUMBER to tapa sub."
            for num in data:
                if num != "?":
                    solver.add_program_line(f":- not area_len({i}, {num}).")
            solver.add_program_line(f":- #count{{ N: area_len({i}, N) }} != {len(data)}.")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Rail Pool",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7ZRNaxsxEIbv/hVBZx1WI3m/LsFNnV5c9yMuISxLsJ1NY2rHrZ0tZY3/e94Zyd1tMJQSCDmUZWcfjWdGr8aStj/q6abSKR6b6kgbPNaRvBRl8kbhmSwellV+ogf1w916A9D6w/m5vp0ut1WvCFFlb9dkeTPQzbu8UEZpRXiNKnXzKd817/NmqJsL/KR0Ct/IBxFw2OKl/M505p0mAo/BDgy8As4Xm/myuh55z8e8aCZa8TxvJJtRrdY/KxV08Hi+Xs0W7LivV7fL4NzWN+tvdQgz5V43A690dESpPaaUnU+VhoBnK51NH9D27d3i+zG5Wbnfo+OfIfg6L1j7lxbTFi/yHew43ymKOdVCi0Y3Uc9acZyeti5n2NVxxE7m62Rl6ZMQE0mSoU6QMQn7Whc0GFFyJfZcLImdQKhurNi3YiOxfbEjiRlCv4kzbZJI5YT6/bTlhLRJoZM5deB+4D4Yi5YY9h/YIjfEc26CPjDHiEkOMTHisVKpg7nSzHPGJ8PPi68mQ56N6TD70ROJT8FBZ5ZojAOjfoYeCUNnFuYFU+T9+CLXz0uG6wSOYrCvI9yNjw5+xFPQSdBDXg++4KCTcNLxD/3WH1jWGPQTgW2oY1HHhVy+Jfq+h2TBLrBzYN9/fMF+XWTZf2CLmp1c3ocSD81xmIvZhZ7H6E/Ca8RGuJTtcCbWiY1lmyS82//pPDx/R/5VTkH4l/94sJKXHJe9Qo0W99XJeL1ZTfnaG9587YzG9WpWbQ5j3OD7nvql5C1wSLT7f6m//KXO3Y9e21Z+bXJwuMreIw==",
        },
    ],
}
