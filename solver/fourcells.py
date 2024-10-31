"""The N Cells solver."""

from typing import List

from .core.common import display, edge, grid
from .core.helper import extract_initial_edges
from .core.neighbor import adjacent, count_adjacent_edges
from .core.penpa import Puzzle, Solution
from .core.shape import OMINOES, all_shapes, count_shape, general_shape
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.row * puzzle.col % 4 == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(extract_initial_edges(puzzle.edge, puzzle.helper_x))

    for i, o_shape in enumerate(OMINOES[4].values()):
        solver.add_program_line(general_shape("omino_4", i, o_shape, color="grid", adj_type="edge"))

    solver.add_program_line(all_shapes("omino_4", color="grid"))
    solver.add_program_line(count_shape(target=puzzle.row * puzzle.col // 4, name="omino_4", color="grid"))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(count_adjacent_edges(num, (r, c)))

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "FourCells",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VVNi9swEL37VwSd52B9+POWbtNeUm/bpCzBmOBk3W6og1MnLkUh/31HYy+hUpayFEIpi6LH89PI82Yi5P2Prmwr4KH5yRh84DhCFdIM4oSmP4z55lBX6QjG3eGhaZEA3Gbwtaz3lZcPQYV31Emqx6DfpzkTDGhyVoD+lB71h1RnoGe4xICjNkXGGQikkzO9o3XDbnqR+8izgSNdIF1v2nVdLae98jHN9RyYyfOGdhvKts3PivXb6HndbFcbI6zKA9ayf9jshpV9d99874ZYXpxAj3u7kwt25dmuob1dwy7YNVX8vd1611wymhSnEzb8M1pdprlx/eVM4zOdpUfELD0ylTzV2P8rLFCWEDpCYAncj2yFC0dxdglpKyq0lcB3FOc9kZMrcvzETq7YeU8c20pixwinLiHsXELanoWyswuny8KpQkR2N4TjWSR2LunbuaRv1yWdKqTTeRlwR/k9Ox4gTsdoQfiOUBDO8ZSBloRvCX3CgHBKMRPCO8IbQkUYUkxkzumLTvIV7ORK0H34/Ahe1//n9cLL2eT+WzXKmnZb1ngDZ912VbVPz/ixO3nsF6OZS9yiXr9/V//+meb7/9rd8Qc7uZ6BSkDfAtt1y3K5bvB0Ydee1xcv1DOj9//AcKFfCrA3Xr1NeMsW3iM=",
        },
    ],
}
