"""The Detour solver."""

from typing import List

from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, direction, display, fill_path, grid
from noqx.rule.helper import full_bfs
from noqx.rule.loop import loop_turning, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
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

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))

        if rc:
            num = puzzle.text[Point(*rc, Direction.CENTER, "sudoku_0")]
            if isinstance(num, int):
                solver.add_program_line(f":- #count {{ R, C: area({i}, R, C), turning(R, C) }} != {num}.")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Detour",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VVRa9s8FH3Pryh61oMl2Zbkl9GvS/eS5dvWjFKMKWnrrWHJvDnxKA757z33Sq47KAxW2PowjK+Pjq6so6Mre/u9W7a1dLiMk4lUuEyq+daJ5zuJ12K1W9fFkTzudrdNCyDl/6en8tNyva0nZcyqJvveF/2x7N8UpdBC8q1EJfv3xb5/W/RT2Z+hS0gFbgakhNSA0xGecz+hk0CqBHgObMKwC8DrVXu9ri9ngXlXlP1CCprnPx5NUGyaH7UIr+D2dbO5WhFxtdxhMdvb1bfYs+1umi9dzFXVQfbHQe7sCblmlEswyCX0hFxaxbPlrldf6+buKam+Ohxg+QeIvSxK0v1xhG6EZ8Uecc5RFXuRuwRvMCQG2NHbXrE0kfscrZSxdSkwigLYJTQiYqsfchyPRukAezuO9Z5yaAZMecETn3LUHBfQJXvD8TXHhGPGccY5UwhVmZfKKlFolFGO6a2JGK+2WcAWvIu8Be8GPgO2ATvwPvIOvB94C+wD9hkqPvLeUvVHjJOgggb0AweeT4iOvFLAQQP6pTaR1+BN5LUBDhrQL3UaeQM+HXhoSIMG9EudRT4Fnw08NGRRm6O1w2rGevSB1kvbxxhbMnhCa3fYJsb5I3/gA20lYwc8rJE8Cfl4PvjDPiQhH88Hr9gThVJhH5LRN/JHBZ14Ag+ekFcx3yB/8I38MTHfIH/wkLwyYV14PvITOk3UaaDTkE4U0TmX0gnHlGPOJWbpYPzG0XlONf9STqmxIz9d2K0/2a4mpZjha3M0b9rNco1PzvTm86PWvNtc1e3Qxtf+MBF3gm866zL99wP4Cz8Asj95abX80uTgdImbetd0ragm9w==",
        },
        {
            "url": "https://puzz.link/p?detour/12/12/4i461svho42s221q10sfps312904a1aldml2h84k190ka5bdlak2h03147g91374232",
            "test": False,
        },
    ],
}
