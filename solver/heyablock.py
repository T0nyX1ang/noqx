"""The Heyablock solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, avoid_area_adjacent
from noqx.rule.reachable import area_color_connected, grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(avoid_area_adjacent(color="gray"))
    solver.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(area_color_connected(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))

        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="gray", _type="area", _id=i))
        else:
            solver.add_program_line(count(("gt", 0), color="gray", _type="area", _id=i))

    for r in range(puzzle.row):
        borders_in_row = [c for c in range(1, puzzle.col) if (r, c, Direction.LEFT) in puzzle.edge]
        for i in range(len(borders_in_row) - 1):
            b1, b2 = borders_in_row[i], borders_in_row[i + 1]
            solver.add_program_line(avoid_rect(1, b2 - b1 + 2, color="not gray", corner=(r, b1 - 1)))

    for c in range(puzzle.col):
        borders_in_col = [r for r in range(1, puzzle.row) if (r, c, Direction.TOP) in puzzle.edge]
        for i in range(len(borders_in_col) - 1):
            b1, b2 = borders_in_col[i], borders_in_col[i + 1]
            solver.add_program_line(avoid_rect(b2 - b1 + 2, 1, color="not gray", corner=(b1 - 1, c)))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Heyablock",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVbT9tMEH3Pr0D7vA/ei+213ygNfaGhbagQiqLIBFMiEoUvIb04yn/nzOwYg4Q+qKpSVaoSr88ej2dmz6xn1/9tqlWtTUJ/FzTu+HkT+LIh4yuR38nsdl6Xe3p/c3u1XAFofXx4qC+r+brujcRq3Ns2Rdns6+ZdOVJGaWVxGTXWzcdy27wvm75uhnikdAB3FI0sYL+Dp/yc0EEkTQI8EAx4BjidrabzenIUmQ/lqDnRiuK84bcJqsXya60kD5pPl4vzGRHn1S0Ws76a3ciT9eZieb0RWzPe6WY/pjt8Il3XpUswpkvoiXRpFb853WK820H2T0h4Uo4o988dDB0clluMg3KrXIJXHWrNlVHOYmrvp2nA1N9PMzLunmYe07SbZo+emuSxtUnIvAtlPMV6OKf3H84pePs+0jWc9BmPhzxaHk+wJt04Ht/ymPCY8njENn0s1Rqnrc1VabEVTQpcCM61dUZwAewituC98Ba8F94Z4FQwfHrx6cGnwnvwacsjViqxPHxm4jMFnwmfgs9bHrFyiZXBZy4+M/BB+Bx8ED5HrCCxcvgM4jOAL4QP4IuWz7VLJFYogMVnAd4IX4A3kYctcIwFW+DoE7baWeGhrRNtYQscY8FWO9EWtsDCQ1sn2sIWWGJBWyfawla7VHho60Rb2AJLLGjrWm1hbz02HeucdLWjutBmY2y7OlKNPDYlY9/VlOpFm5ExOt99fWk/YFMyRlf0rZ5UC/Ef4L+tEekfxH+A/7ZeVIsg/rmztjWC/yD+A3Xd1j/WVci6CqyraHUjzaN/3LtakM42+se9qwtpbqN/3Lsakf7UB1hztP+2XlQLagiMLTCtCx/TKX9SBzx6HjP+1HJqLi9sP9x4glaseexFv/6JP5vbCMujg+3xj1rYX8aNeyM13Kwuq2mNc6B/8aXeGyxXi2qO2WCzOK9X7RzH8K6nviu+uL36fyfzHzqZqQTJT53Pr/BNPJPOCOqiITbHWt1sJtVkusQeg3b/x+Mre6n9q68WTUBd1T+qb9V1rca9Ow==",
        },
    ],
}
