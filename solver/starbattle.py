"""The Star Battle solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.param["stars"].isdigit(), "Invalid star count."
    num_stars = int(puzzle.param["stars"])

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="star__2__0"))

    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_adjacent_color(color="star__2__0", adj_type=8))

    solver.add_program_line(count(num_stars, color="star__2__0", _type="row"))
    solver.add_program_line(count(num_stars, color="star__2__0", _type="col"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count(num_stars, color="star__2__0", _type="area", _id=i))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"star__2__0({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not star__2__0({r}, {c}).")

    solver.add_program_line(display(item="star__2__0"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Star Battle",
    "category": "var",
    "examples": [
        {
            "data": "m=edit&p=7VXNbts8ELz7KQKeeeCfREm3NHV6SZO2SREEgmAojtoYdeDUP0Uhw++e2eWq/oqmCJpD8BUoZFFjkjsc7nCl1ddNu+y0dfTzhTba4gpl4NvHjG8j18VsPe+qA324Wd8ulgBanx0f60/tfNWNaorE1Yy2fVn1h7p/U9XKKc23VY3u31fb/m3Vj3V/jiGFubo/AbJKO8DxHl7yOKGj1GkN8KlgwCvA6Ww5nXeTk9Tzrqr7C61onVccTVDdLb51KoXx/+ni7npGHdftGptZ3c7uZWS1uVl82chc2+x0f5jkXj0i1+/lEkxyCT0il3ZBclfrdvksqSnwV5Fls9sh2R8gc1LVpPjjHhZ7eF5t0Z5WWxU8hcIPy46g1/LYFY0FjDkswas5GjzmQcftBbh077l9za3hNuP2hOeMQeNKnBlrVQUqb6L2DmsSthY4CsYcL3OcBy4FYz5pZFwAQxNhj9ggsb7UPssSDojNJDbgvOZGMHhy4cnoDMtaGWKjxOaIjRIbwV8If6RCKASDsxROqoVSeCJ4SuEpog5G1ioKYNFcGuBcMGrKCD/yEyQ/iANOGhCng0trIQ7YCQa/5BBxwIkHcTr4pAHjwMKDHAbJYUBFh0z0kBdG9mWQWyN7N9iLlT1as/eO/LJJA57Ag4/ImxVOi/xYyQP55QYfwemF04Nz8DoHzgcM/lz4c/APfpEXUfrJizj0k1+yLvky+MjvKMlzzIEHH7HfOPgIbT+8hrZCtBWYL74j98it+OIoz5J/D7984scTWOZ75Nknfs7zkH+czxDExwDOIJwBnEE4gxOPUDSXXDpH3AZucy6pSMX7R+X933J+XvU+KafO5C3/0xX/vr5mVKvxzefu4HSxvGvneL2e37b3ncLXazdS3xXftaeP4b8P2ot+0Cjx5v927p+QUyOnqIz+TKv7zaSdTBc4UcjYb/pfXD0Kl5OezohqRg8=",
        },
        {
            "url": "https://puzz.link/p?starbattle/15/15/3/31g94h1gk30glmiuum28c52kl8mh0i10o51gh4i1go2h84a4802gt5hah8la6046hc9aign1ga18424a42h8",
            "config": {"stars": 3},
            "test": False,
        },
    ],
    "parameters": {"stars": {"name": "Stars", "type": "number", "default": 2}},
}
