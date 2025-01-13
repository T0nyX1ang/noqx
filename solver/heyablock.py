"""The Heyablock solver."""

from typing import List

from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import area_color_connected, grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(area_color_connected(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        flag = True
        if rc:
            num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
            if isinstance(num, int):
                flag = False
                solver.add_program_line(count(num, color="gray", _type="area", _id=i))

        if flag:
            solver.add_program_line(count(("gt", 0), color="gray", _type="area", _id=i))

    for r in range(puzzle.row):
        borders_in_row = [c for c in range(1, puzzle.col) if Point(r, c, Direction.LEFT) in puzzle.edge]
        for i in range(len(borders_in_row) - 1):
            b1, b2 = borders_in_row[i], borders_in_row[i + 1]
            solver.add_program_line(avoid_rect(1, b2 - b1 + 2, color="not gray", corner=(r, b1 - 1)))

    for c in range(puzzle.col):
        borders_in_col = [r for r in range(1, puzzle.row) if Point(r, c, Direction.TOP) in puzzle.edge]
        for i in range(len(borders_in_col) - 1):
            b1, b2 = borders_in_col[i], borders_in_col[i + 1]
            solver.add_program_line(avoid_rect(b2 - b1 + 2, 1, color="not gray", corner=(b1 - 1, c)))

    for (r, c, d, _), draw in puzzle.edge.items():
        if d == Direction.TOP and r > 0 and draw:
            solver.add_program_line(f":- gray({r}, {c}), gray({r - 1}, {c}).")

        if d == Direction.LEFT and c > 0 and draw:
            solver.add_program_line(f":- gray({r}, {c}), gray({r}, {c - 1}).")

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Heyablock",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVdT9tKEH3Pr0D7vA/eD9trv1SUhr7Q0DZUCEVRZIIpEYnCTUg/HOW/c2Z2jEFCheqqXFW6Srw+ezyemT2znl3/s6lWtTYJ/V3QuOPnTeDLhoyvRH4ns9t5Xe7p/c3t1XIFoPXx4aG+rObrujcSq3Fv2xRls6+b9+VIGaWVxWXUWDefym3zoWz6uhnikdIB3FE0soD9Dp7yc0IHkTQJ8EAw4BngdLaazuvJUWQ+lqPmRCuK85bfJqgWy2+1kjxoPl0uzmdEnFe3WMz6anYjT9abi+X1RmzNeKeb/Zju8Il0XZcuwZguoSfSpVX84XSL8W4H2T8j4Uk5oty/dDB0cFhuMQ7KrXIJXnWoNVdGOYup7aaBHL9BpkKkRPj7aUZvd+aZxzTtptmjpyZ5bG0SMu9iG0/BH87p/YdzCt6+j/wNr+KMx0MeLY8nWKRuHI/veEx4THk8Yps+1m6N09bmqrTYmyYFLgTn2jojuAB2EVvwXngL3gvvDHAqGD69+PTgU+E9+LTlESuVWB4+M/GZgs+ET8HnLY9YucTK4DMXnxn4IHwOPgifI1aQWDl8BvEZwBfCB/BFy+faJRIrFMDiswBvhC/Am8jDFjjGgi1w9Alb7azw0NaJtrAFjrFgq51oC1tg4aGtE21hCyyxoK0TbWGrXSo8tHWiLWyBJRa0da22sLcem451TrraUV1oszG2XR2pRh6bkrHvakr1os3IGK3wvr60H7ApGaNN+lZPqoX4D/Df1oj0D+I/wH9bL6pFEP/catsawX8Q/4HacOsf6ypkXQXWVbS6kebRP+5dLUhnG/3j3tWFNLfRP+5djUh/agysOc6Dtl5UC+oQjC0wrQsf0yl/Ugc8eh4z/tRy6jYv7EfciYJWrHlsTv/+E382txGWRyfd4x+1sL+MG/dGarhZXVbTGgdD/+JrvTdYrhbVHLPBZnFer9o5zuVdT/1QfHF79f8f1f/RUU0lSH7rwH6Fb+KZdEZQFw2xOdbqZjOpJtMl9hi0+xWPr+yl9q++WjQBdVX/rL5X17Ua9+4A",
        },
        {"url": "https://puzz.link/p?heyablock/10/10/498g17buntfqsh12247obovv003o00vv3o3o726h22j2h4g6g2", "test": False},
        {
            "url": "https://puzz.link/p?heyablock/15/10/4i894gi914i2944i894gi914i294000vvv000vvv000vvv000vvv0001122222024024311331235234",
            "test": False,
        },
    ],
}
