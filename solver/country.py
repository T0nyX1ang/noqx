"""The Country Road solver."""

from typing import List

from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, count, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.loop import count_area_pass, single_loop
from noqx.rule.neighbor import adjacent, avoid_area_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="country_road"))
    solver.add_program_line(fill_path(color="country_road"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="country_road", adj_type="loop"))
    solver.add_program_line(single_loop(color="country_road"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count_area_pass(1, ar))
        if rc:
            num = puzzle.text[Point(*rc, Direction.CENTER, "normal")]
            if isinstance(num, int):
                solver.add_program_line(count(num, color="country_road", _type="area", _id=i))

    solver.add_program_line(avoid_area_adjacent(color="not country_road", adj_type=4))
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Country Road",
    "category": "loop",
    "aliases": ["countryroad"],
    "examples": [
        {
            "data": "m=edit&p=7ZZNb9tGF4X3+hUG17MgOZ/UpvCb2t2o7kdcBIEgBLKtNkLtqK9sFSkN//c8d+YOFbQGiiIomkUgaHRmdMh7eHkOh/f/P6z3G9P1pgvGJtOajo8bnAkuGBfBfFv9XG4fbjfzE3N6eHi72wOM+e783Py8vr3fzJbKWs0ex2E+nprxm/my6RrT9Hy7ZmXGH+aP47fz8cyML/mrMR1ri0LqgWdH+Cr/L+hFWexa8IVi4Gvg9XZ/fbt5sygr38+X46VppM7/8tECm7vd75tGdcj8end3tZWFq/UDF3P/dvub/nN/uNn9elBut3oy42mRu3hGrj3KFVjkCnpGrlzFJ8u93b7b7N4/J3VYPT3R8h8R+2a+FN0/HWE6wpfzR8aL+WPjnRz6FTrKfWl8+NNCiCxEN837Xhj2o/nA3B/n1jIX69S5Zx50TtkuF3+dx/M89nm8RJsZbR6/zmObR5/HReacIdniTSu6e9NY14FRmHEPTootGGEZO2NDqziCESjYe2NjpxjLx14xnFg51Ipayw9gLkZwaME0ImM0RNUQ0BBVQ6Bu0roRflJ+hJOUE6k1aK0EZ1BOInGt6hlIXqvnH3qwHjvA6QoHLriss2ZcX/FgnNwAwX00zpVazjrjfNHm6I/T/rAGLhpYI/EVUytpreh5KpS+8T9Y15MFl567NBjfat2hBet50O9VvxuS8V3prW/hdIXjW2d8X/RwDnCpxXFg5XesW13nGr1eI8eB9Ty9BRc9cI13pYfeosEVDd7CcZVDXe0J5wPr+W0Al2v0NoJLDz0+9OpD76gr0ckYflA+fvPqN2qCle/RI8nKGD1B9Xj0BNXj0RNVD1716lXqgPX8AX5UPn7z6jcf4Cflc++83jtqglVPQE9SPYEeJu0hXvXqVeqAVRv+9OpPn6IJbc0IPveaC8lRzaNkJGi+JBc1d2gmG8dc1Ayyu0wZjHBq7vDblDXJS81XIptJM47f7KBZw29kZspLzRcZmrJDVsiLelVyUfMiuah54RlCNo4Zcbou/q+5SGRN+ymex+uT56eMSGarhoFaQ/W/ZKT6nHuneSErYPUGmmteyAoZUY74v+aF7dp3yu/g63OAX7B6o8dvvXqg55726gHJSM1ULzmq/pccVf/Dl4d6zUjNmmSkZk0yYmu+qDvljnM6PacD13yJh9Un2av6zPHcX6/3l9+jt8V71c/0fPIwz5zJw0n8r9qS+L96VfyvtfBt8TObyau8pbzIo8tjyFtNlE3yH22jn76r/a2cJZ2XTfWvH9l6v6z/6+ur2bJZ8OZ1crHb361vef06u/nlo9nF4e5qs69z3nyfZs37Jn/z25L78jL8H7wMS/vbzy3Ln5scni409PDuYf/HyX63vmlWsw8=",
        },
        {
            "url": "https://puzz.link/p?country/17/17/4si5d6t8fa2heg0ch42pfar88vioeikf7s4665a6g69g2bo2rc2qk0g5jrmll2p6kk62qsfhflvrakghu0pq13l87qg5huhgj407o09p0557vg4g4j-19o-362k2q1g",
            "test": False,
        },
    ],
}
