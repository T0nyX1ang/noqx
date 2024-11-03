"""The Country Road solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.loop import pass_area_once, single_loop
from noqx.rule.neighbor import adjacent, avoid_area_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
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
        solver.add_program_line(pass_area_once(ar))
        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="country_road", _type="area", _id=i))

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
            "data": "m=edit&p=7ZZPbxs3FMTv/hTGnnnYXfKRXN3cxO7Fdf/ERRAIQuA/amPUjlrZKlIZ/u75PfJRClADRREUzSEQRA2pWb5Zcma5939sLtZLN4xuiM5n17uBT5iCiyG6kMB8e/uc3zzcLmeH7mjz8G61Bjj3/cmJ++Xi9n55MDfW4uBxO822R2777WzeDZ3rRr5Dt3DbH2eP2+9m22O3fcVfnRsYO62kEXi8h6/L/4pe1MGhB58ZBr4BXt2sr26Xb0/ryA+z+fbcdVrnm3K1wu5u9eeyMx3av1rdXd7owOXFAzdz/+7md/vnfnO9+m1j3GHx5LZHVe7pM3L9Xq7CKlfRM3L1Lj5b7u3N++Xqw3NSp8XTE0v+E2Lfzuaq++c9zHv4avZIezZ77GLi0hTY6LIt3ThGBvwn/Ym+7Pve01djtL7Qj9Zn0qFM/aa0J6UdS3tOZbf1pX1Z2r60UtrTwjlGkMd5XkI3G13nwwBGYcEjOBv2YIQVHJyPveEERqBiEefTYBhDp9EwnNQ41EpWSyYwN6M49mAWomA0JNMQ0ZBMQ6RutroJfjZ+gpONk6g1Wa0MZzJOJk+96ZnIVW/zTyPYrp3gDJUDF1zHGXNhbHhyQTdA8ZhcCLVW8MEFqdoC6xNsfRgDVw2MkeeGqZWtVhIyX9eN/8E2nj24rnnIk5Pe6k492OZBv5j+MGUnQ11b6eEMlSN9cDJWPcwBrrW4Dmz8gXFv49yj2D1yHdjmGT246oHrJNQ1FI+GUDWIhxMah7q2JswHtvl9BNd7FJ/AdQ0FH4r5UAJ1xeryLJRofPwm5jdqgo0v6NFkFYyeaHoEPdH0CHqS6cGrYl6lDtjmj/CT8fGbmN8kws/GZ+/E9o6aYNMT0ZNNT2QNs60hXhXzKnXApg1/ivlTcnKxbxnB52K50By1PGpGouVLc9Fyh2aysc9FyyBnxy6DCU7LHX7bZU3z0vKVyWa2jOM3P1nW8BuZ2eWl5YsM7bJDVsiLeVVz0fKiuWh54RlCNvYZCTau/m+5yGTN1lM9j9d3nt9lRDPbNEzUmpr/NSPN5+yd5YWsgM0baG55IStkxDjq/5YXDmMZjD/At+cAv2DzxojfRvPAyJ6O5gHNSMvUqDlq/tccNf/D14d6y0jLmmakZU0z4lu+qLvLHXMGmzOAW77Uw+aT4lV75gj7K7a//O69rd5rfmbNdx7mmbPzcFb/m7as/m9eVf9bLXxb/cxh8rocKS9KG0oby1GT9Aj8V4fk559q/yhnzsrrofr3jx69X8f/8/HFwbw75b3q8Gy1vru45eXq+PrXT3pnm7vL5br1ea99Oug+dOVb3pbC11fd/+FVV5e//9Ky/KXJ4enCgm7eP6z/OlyvLq67xcFH",
        },
        {
            "url": "https://puzz.link/p?country/17/17/4si5d6t8fa2heg0ch42pfar88vioeikf7s4665a6g69g2bo2rc2qk0g5jrmll2p6kk62qsfhflvrakghu0pq13l87qg5huhgj407o09p0557vg4g4j-19o-362k2q1g",
            "test": False,
        },
    ],
}
