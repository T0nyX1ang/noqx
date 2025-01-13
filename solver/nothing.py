"""The All or Nothing solver."""

from typing import List

from noqx.puzzle import Puzzle
from noqx.rule.common import area, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.loop import count_area_pass, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import area_same_color
from noqx.solution import solver


def avoid_area_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint to avoid same {color} cells on the both sides of an area.

    An adjacent rule and an area fact should be defined first.
    """
    return f":- area(A, R, C), area(A1, R1, C1), adj_{adj_type}(R, C, R1, C1), A < A1, {color}(R, C), {color}(R1, C1)."


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="anything"))
    solver.add_program_line(fill_path(color="anything"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="anything", adj_type="loop"))
    solver.add_program_line(single_loop(color="anything"))
    solver.add_program_line(area_same_color(color="anything"))
    solver.add_program_line(avoid_area_adjacent(color="not anything"))
    solver.add_program_line("nothing(A) :- area(A, R, C), not anything(R, C).")

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, (ar, _) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count_area_pass(1, ar).replace(":-", f":- not nothing({i}),"))

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "All or Nothing",
    "category": "loop",
    "aliases": ["allornothing"],
    "examples": [
        {
            "data": "m=edit&p=7ZjPb9tGEIXv/isMnnkQyZ0lqZubOr246Y+kCALBCJzEbYw6UWvHRSDD/3u+2X1DXlL0UCDIIZDEfZKGM0Py7beUbv++u7i5bDvz5zC1m7bjkTdTeXUT73nF49nVh+vL7XF7cvfh7f4G0bY/PX7c/n5xfXt5tFPU+dH9Yd4eTtrDD9td0zdteXXNeXv4ZXt/+HF7OG0PT/mqaTs+O0N1TdsjT1f5vHzv6lH9sNugn0gjXyBfX928vr58eVY/+Xm7OzxrG6/zXdnbZfNu/89lU3cr71/v37268g9eXXzgYG7fXv2lb27v3uz/vFNsd/7QHk5qu2efaXdY23VZ23X1mXb9KP53u9dX7y8/fq7T+fzhgTP+K72+3O687d9WOa3y6fae7ZOy7cr2Rdk+Ltu+bJ8R2h6Gsv2+bDdla2V7VmJOt/fNMA1t2vTNtm/RCT1IZ7RJj+gsPaHHqucNepbu29R10uTplGc2dCo6bbo29Rtp4vsaT0107SFt2Lev+1IfHfvST1/7oT669pM6euhrD9Rv06D8HTkH5ezIOShnT/yg+J74pPiefpL66YlPET+jp6oH4k3xA/lN+QdiTDGJ/Kb8iZxZORM5s3ImjivruBLHknUsiTxZeYx9R+1rnPOxnvOUyT8qfyZmUkwm/6T8mfyT8mfyT8qfyT8p/8ixzDqWkfyz8o/EzIqBF2lWralvbaNaeMbkmTQZWrXwickn1EEr5zSjlRPPmDxDzdY6xc/Ed4qfie9qvG2I72o89VuTfwzPmDxDfXQ9dsMzJs/QC7p6hl7QtZYBSBsU0xEzKKYjZogY+hlqP9RHqx/8Y/KP4R+Tf6iPVj/4x+Qf6qNVq6dWUq2eWkm1BuJN8QMxphgobqYe8JXJV5aom1U3UTerLr4y+crwlclXZuQfld+IGRVj1BpVC4+ZPEZutGplak2qlak1qRYeM3mMOmjlGYmZFTPy+Ryf08+sfvCbyW/UQevc4jeT32zytUt18V6W9wzvZXnPZmI6xcCfLP5QE63e5oxWD/gty2/URKsH/JblN2qiaw8Zj2V5LOOxLI9RE60YvJTlJfKha37yoWt+9muzvMF+aNWCJ1k8yfAkiyfkQNeeM2zJYkvmumddd/Kh6/FmuJHFjWzEjIoxco7KybXOutbkQ6s3rnUOnnDsMHpldcxxZ7LWgsLemMvcVwT/GeF8sJc8uhaFyV1w2NeI4KrzP7QzX/mZLwvbmS+pFxOYL6lX3Z66wfzBea5azudg/kD+YD7zaGG+8zk4z/mE0Surg/nOas3TwmrNU0a0+knkTJHT+a9jN+d/cNvXC+V3nmuOF57HGmHOfO3rbI/1wtke64WzPasf5hpMlyZPjrWAPLrujOvawbyD7yvPY71gfsH0he3L2uH3A7F2+P2A5rVzfllH/N5gCrbTwxQ8J0ZznHFZUwrDY/46w2P+cg8Ax1eGy2OsFcsawQj/Nced2zF/ncmxFjiHYy3AV8ta4EyOtcDZKy8V9spLjGjVGnxdCCb7WqAY5uDCeWdvcN7ZG2zHGzB3Za/muHHdF7YzH2HxymELPhOvOV44HJzHGwvnncPBeedwcB5vwOKVvcH20TkfvCW/PFDYG2x39gbb8cPCdl/fg+14YGG7r/XygPk6Pgdv2VfMh9MLnxnRYqazVPcJhaW61jAb3ioePmTxgXFheGGsrjvjwm04DYfFOtblrPtJxpXbzlvdEzKiFePsFSsY0arrHA6esy5n3Rswrmx3Pgfb8UmWTxjRWhec2/IMIzpYTd1YC2AI7BaTiRE3CsNjLcA/cHzlufzDuK4ReAm+r2yXfxjX9QL/5OIfbvyfl9v/R2WbyjaXnwWj/774wr9A/rOdHWfPf8n+24Pfu9++/bq/PT/aNWf86j1+sr95d3HNb9/TN38s7/iX4eGo+diU125gh/Ttj4cv/8eDn/3N1zb5v7Z2wBHnd//+eH9zfHv3vjk/+gQ=",
        }
    ],
}
