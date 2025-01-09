"""The Koburin solver."""

from typing import List

from noqx.puzzle import Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent, avoid_adjacent_color, count_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="gray"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
    solver.add_program_line(fill_path(color="white"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
    solver.add_program_line(grid_color_connected(color="white", adj_type="loop"))
    solver.add_program_line(single_loop(color="white"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        solver.add_program_line(f"gray({r}, {c}).")
        if isinstance(num, int):
            solver.add_program_line(count_adjacent(target=num, src_cell=(r, c), color="black", adj_type=4))

    solver.add_program_line(display(item="black"))
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Koburin",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VRNb5tAEL3zK6I9z2GXxYTspXLTuBdKP+woihCKwN0oKDik2FTVWv7vmRlIoS6XqlIUVRXep7dvZ/CbRTPbb23eWFCKfjoCCcggmIW8lPJ5yf5ZlbvKmhOYt7u7ukEC8HGxgNu82lov7aMyb+/OjJuDe29SoQQIH5cSGbjPZu8+GJeAW+KRAIVa3AX5SC8GesXnxM47UUnkSc+RXiNdl826sjdxp3wyqVuBoP95y9lExab+bkXvg/brelOUJBT5DovZ3pWP/cm2/Vrft32syg7g5p3deMKuHuwS7ewSm7BLVfy93eqxnjJ6lh0OeOFf0OqNScn15UCjgS7NHjExe6HD5xq7ryICn4Q3gxAGJOiRcHqUoiTn4If9qSh1HKP0seL/ljXjN4+VUJIiR0rEWeP3RNEvMViY4vKuGReMPuMKqwenGd8xSsYZY8wxF4xXjOeMAWPIMad0f390wy9gJ9XYmBPP7N9VMy8Vy7a5zdcW+yAuH+xJUjebvMJd0m4K2zzvcQAdPPFD8Eo1zbP/M+nFZxJdvnxtffPa7GAni4e2Ke/zworMewI=",
        },
    ],
}
