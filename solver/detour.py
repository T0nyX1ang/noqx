"""The Detour solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, direction, display, fill_path, grid
from noqx.rule.helper import full_bfs
from noqx.rule.loop import loop_turning, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("detour(R, C) :- grid(R, C).")
    solver.add_program_line(fill_path(color="detour"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="detour", adj_type="loop"))
    solver.add_program_line(single_loop(color="detour"))
    solver.add_program_line(loop_turning(color="detour"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.sudoku)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))

        if rc:
            data = puzzle.sudoku[rc].get(0)
            assert isinstance(data, int), "Signpost clue should be integer."
            solver.add_program_line(f":- #count {{ R, C: area({i}, R, C), turning(R, C) }} != {data}.")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Detour",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VRda9swFH3Pryh61oMl2Zbkt6xL95JlH+0oxZiStt4alsybE4/ikP/ec6/kuoPCYIWtD8P4+ujoWjo6utL2R7dsa+nwGCcTqfCYVPOrE89vEp+z1W5dF0dy2u1umxZAyncnJ/Lzcr2tJ2XMqib73hf9VPZvilJoIflVopL9h2Lfvy36mexP0SWkAjcHUkJqwNkIz7mf0HEgVQK8ADbhtwvA61V7va4v54F5X5T9mRQ0zyv+m6DYND9rEYbg9nWzuVoRcbXcYTHb29X32LPtbpqvXcxV1UH20yB3/oRcM8olGOQSekIureLZcterb3Vz95RUXx0OsPwjxF4WJen+NEI3wtNij7jgqIq9yF2CEQyJEbnPgVPG1qXAKANgl1BOxFY/5DjngFEswN6O/3pPOTQmJrngqU44ao5nUCJ7w/E1x4RjxnHOOTNIU5mXyipRaBROjumtiRhD2yxgC95F3oJ3A58B24AdeB95B94PvAX2AfsMNR55b6neI0btq6AB/cCB5zOhI68UcNCAfqlN5DV4E3ltgIMG9EudRt6ATwceGtKgAf1SZ5FPwWcDDw1Z1OZo7bCasR59oPXS9jHGlgye0Nodtolx/sgf+EBbydgBD2skT0I+vg/+sA9JyMf3wSv2RKFU2Idk9I38UUEnvsCDJ+RVzDfIH3wjf0zMN8gfPCSvTFgXvo/8hE4TdRroNKQTRXTOpXTMMeWYc4lZOgp/cFieU82/lVNq7MgvD3brb7arSSnmuF+OFk27Wa5xycxuvjxqLbrNVd0Obdzvh4m4E/zSWZfp/yv/H1z5ZH/y0mr5pcnB6RI39a7pWlFN7gE=",
        }
    ],
}
