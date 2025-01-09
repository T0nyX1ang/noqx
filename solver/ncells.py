"""The N Cells solver."""

from typing import List

from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.reachable import grid_branch_color_connected
from noqx.solution import solver


def count_reachable_edge(target: int) -> str:
    """
    Generates a constraint for counting grids in a region divided by edges.

    An edge rule and a grid_branch_color_connected rule should be defined first.
    """
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")

    return f":- grid(R0, C0), #count {{ R, C: {tag}(R0, C0, R, C) }} != {target}."


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    assert puzzle.param["region_size"].isdigit(), "Invalid region size."
    size = int(puzzle.param["region_size"])
    assert puzzle.row * puzzle.col % size == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(grid_branch_color_connected(color=None, adj_type="edge"))
    solver.add_program_line(count_reachable_edge(size))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(count_adjacent_edges(num, (r, c)))

    for (r, c, d, _), draw in puzzle.edge.items():
        assert d is not None, f"Direction in ({r}, {c}) is not defined."
        solver.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "N Cells",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VjfbyI3EH7nr4j22Q/2+tfuvqVX0peUa5tUUbRCiBDaQwWRQqiqRfzv99m7hM3CrJNycNeqQmsGf+OxPTP+PMvyz9VwMWaCMyGYTBi+8VEiYUobZqXyD68+t5Pn6Ti7YJer50/zBQTGPl5dsd+G0+W4k1da/c66SLPikhU/ZHkUR8w/Iuqz4udsXfyYFT1W3ACKmEDfNSQRsRhidyfeedxJH8pOwSH3KhniPcTRZDGajgfXZc9PWV7cssjN850f7cRoNv9rHJXD/O/RfPYwcR0Pw2dsZvlp8lQhy9Xj/I9VpSv6G1ZclsvtHliu3C3XieVynXSy5U6f5ocWmvY3Gzj8Fyx1kOVu1b/uxGQn3mRrtL1sHSmz3WMZlUhZ14EgvXQkrkPWOtLGEM0bQ7RodBivURtidEPDqsYsiZ+2piF43DAiuNzT8WZe6fiZaoYFb25Z8OaehfA69Z7Y76luRzY3JWRzV0Ltraf0Xt2ObjpYaK9Tt1M6sK5j9tZj9vxjXvsHIRc+8Pe+vfJt7Ntb5AUrpG+/9y33rfbttdfp+vbOtx98q3xrvI51mfWu3Dt+OchN+CVNkHEK7vCCgcedAKaqBAtveiHZCmmlHGvNYo1QSxZJMJy0MOdkk+5k6ADb6Wgki5Mthw4MyaBTclkS6euP/m/09Tt51H38fXzRmy9mwylYqbeaPYwX29+4ADad6O/IP7l098n/d8LZ7wTnfH7m03ksWeTw68sRZcVHFj2tBsPBaI4kg/Mq2AC2JKxkKxynDCq0cYXRmjbOAatWGLREzm1bYGPiw4AyigA0p0xRgNWUKWJyYw01Qr53H19wDmofZfhxBZMw4qta4ovUQ31Ewkg9VEsk7OKbkDAKaRpWOqX8SYTfGMIJxhD+NMaSeY+loyoh4YTFFpTd4hfUKxSMdIxR7VGwRcja4BgwfWKtaF1aO7wtASi4qgrI0WWh0GacpqJtOXEYRulCAClxuFsA8aUIhOSic2QpeUSCvBxg9cCFcwyrB6+rwH30b6Wzr8sJAboKkF2gggjAbzBOB1QKUAbeMttgQTOKsBhNpqJEtkg6WzxMrxwQ4JSEOdiM03Nz/L0k6LkF5qbhGDwcJ3S8Ezg1ackW5BoJ44WSoE0k+EEAb57ECEtxNlUTWUNUOFoSpjRVE5FzkKboyak5kASSSUMnIKhbmpYUQpRJGO/xXyH8YYo95rif9FSclixOGOkTM9EbqrJ/XvK1Fm2hki9UKwQqjTdUObTPQ/AJX21DFdY3WYWf/a8R/GvY73wG",
        },
    ],
    "parameters": {"region_size": {"name": "Region Size", "type": "number", "default": 5}},
}
