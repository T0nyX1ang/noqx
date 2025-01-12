"""The Regional Yajilin solver."""

from typing import List

from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, direction, display, fill_path, grid, shade_cc
from noqx.rule.helper import full_bfs
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_cc(colors=["black", "white"]))
    solver.add_program_line(fill_path(color="white"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
    solver.add_program_line(grid_color_connected(color="white", adj_type="loop"))
    solver.add_program_line(single_loop(color="white"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))

        if rc:
            num = puzzle.text[Point(*rc, Direction.CENTER, "sudoku_0")]
            if isinstance(num, int):
                solver.add_program_line(count(num, color="black", _type="area", _id=i))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Regional Yajilin",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7ZZBj9tEGIbv+RUrn+dgz4w9Y1/QUrpcQkrZRVUVRatscGkg25TsBhVH+9/7zPgNKdKKAhWVkFDiyRPHT753HH/j3P2yX+56U5Xp6aLhlYevYt5sbPJW6nG1vt/03Zk539+/3u4AY55dXJhXy81dP5nrqMXkMLTdcG6Gr7t5URWmsGxVsTDD8+4wfNMNMzNc8lFhPPum40EWfHrCF/nzRE/GnVUJz2AHgy/B1Xq32vTX03HPt918uDJFqvNlthMWt9tf+0I50vvV9vZmnXbcLO+ZzN3r9Vt9crf/YfvzXsdWiwcznI9xp4/Edae4Cce4iR6Jm2bxyXE36zf9u8eStouHB874d2S97uYp9vcnjCe87A6MszxW3aFoS883+JQFjunbvsjJirayvHPi5sS2hK042cf9yea6Sew+cF1ydbxPbjqG8i9ziIs82jxekdEMLo9f5bHMY53HaT7mKaFtZY21fK3lqqocHMQeJkbmGm7FXMCO0pkDXIm5uFPUzC3sRrYlzNQy46bYmXG9XIvr5VpcL9fhermugmsxmb0yOzJ7ZXZk9srscWu5HreW63FruR63lutx66PLfGvN15O5UWZP5kaZPZkbZa5xG7k1biO3xg1ya9wgt8YNR5f5Bs23IXNQ5obMQZkbMgdlbtIiIrfBjXIDbpQbcKPcgBvlBuYbNd9A5qjMgcxRmQOZW2WOuK3ciNvKjbit3IjbymVhc+XRDbDmGyOszLGFlbllhUxNkxm3ktviVnJb3NQ+mXGr0aUOPLrUgcf5UgceM1MHHjNTBx4zU8e41G6Zca1cesGpF6gDy6UXnHqBOvA4X+oYp16gDjxmpg48ZqYOLNfiOrn0glMvUAeWSy849QJ1YM2XXnDqBerAykwvOPUCdYyr5TrcWi694NQL1IHl0gtOvUAdWPOlF5x6gTqwMtML7tgL/L6/Xz/8jrZN+VlUXuSl5UkefR6bvOSEtGj+xWWVX6vo/IeL66escR8NNefcppv0Hx/1f2/fYjIvLve7V8tVz41tyg3ubLbd3S43vJvtb2/63fE9fykeJsW7Im/p7sKt+P9/GZ/9X0Y6++U/+K/xr7bDR+LMh0tWbTM8M8Xb/fXyerXl8uK0/dl+FpS/tf+R7/nsZ4F1odj1P663b5abs9+WP635KYvF5D0=",
        },
        {
            "url": "https://puzz.link/p?yajilin-regions/11/18/c6c69alhlhg1lhhh4h91gdict8jomt4aemu3001i3tk00uuff1g3vovve81oiu2k1sfvmrto68g2g22g222g222111111111g11g11111h",
            "test": False,
        },
    ],
}
