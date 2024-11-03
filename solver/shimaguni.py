"""The Shimaguni solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_adjacent, avoid_area_adjacent
from noqx.rule.reachable import area_color_connected
from noqx.solution import solver


def adjacent_area_different_size(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to enforce that adjacent areas have different sizes.

    An adjacent area rule and an area rule should be defined first.
    """
    size_count = f"#count {{R, C: area(A, R, C), {color}(R, C) }} = N"
    size1_count = f"#count {{R, C: area(A1, R, C), {color}(R, C) }} = N1"
    return f":- area_adj_{adj_type}(A, A1), A < A1, {size_count}, {size1_count}, N = N1."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="gray", _type="area", _id=i))
        else:
            solver.add_program_line(count(("ge", 1), color="gray", _type="area", _id=i))

    solver.add_program_line(area_color_connected(color="gray"))
    solver.add_program_line(avoid_area_adjacent(color="gray"))
    solver.add_program_line(area_adjacent())
    solver.add_program_line(adjacent_area_different_size(color="gray"))
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Shimaguni",
    "category": "shade",
    "aliases": ["islands"],
    "examples": [
        {
            "data": "m=edit&p=7VVda9tKEH33rwj71MI+aL+kld5yU6cvqdtep4QgTFAcJTG141s7uhQZ//ec2Z2NGgiUUkpTKLZWZ8ezM8dzZqTtl67ZtFJl9DVe4o6PVT5c2ufhyvhzurhfttWBPOzub9cbACnfHx/L62a5bUc1e81Gu76s+kPZv61qoYQUGpcSM9l/rHb9u6ofy36Kn4T0sJ1EJw04HuBZ+J3QUTSqDHjCGPAccL7YzJftxUm0fKjq/lQKyvNPOE1QrNb/t4J50H6+Xl0uyHDZ3OPPbG8X//Ev2+5q/bljXzXby/4w0p0+Q9cMdAlGuoSeoUv/4hfTLWf7Pcr+LwhfVDVx/zRAP8BptcM6qXbCZDiqoXVQRhjzZKt0+XRvC+ypNWiPECoEOg/rcVh1WE+RR/YmrG/CmoXVhfUk+IyRXisjtUZQjfZQFtgzRscRt4ALYMUY3Wh0xBp2y3YNu2W7yYAtYwXsGGvgnDFyWc5lgV3CDhh/OmBwyJmDRfyc4zv45+zv4FOwj4NPwT45chWcK6cJYnsBbp65FfDx7FMgTslxPOwl2z1ylZwLE2iy5FMCQyzCJeyK7aUHjrngCxxzwRc41hm+0mi2KwUc64NzwDEvzgHHvDgnDdcf54DZrh1wrBXOSWMjB5wDZg54lhiXMDi7yBm+wMzBgpvjHiCNqAkDRm+YpCPqYJKOJbRLupDW3AOWtOY6W9Ka4yD+Yz84YM4bdHQc05HuXHPSNPFx6LHUG6Rv6g0HDqk3cnDImUMODqlPcpxNfRKeoBzTw+6TnXqDY0LTxx4oEbPkmmeoG+sbtFNsJ+2S1lRzGtaA4c+zg/ugHWbB8OzgDvyNFlxD3AftUENoM2jENcQdmHsG82J4pnAHpv+I4T4LI34UVhvWPIx+QQ+gH3pE/fxT5rt0alSJHmpPP+7Ps81GtZh2m+tm3uL1ML66aQ8m682qWWI36VaX7Sbt8Xbej8RXEa7a0Mv+7wv7N72wSYLspc3ES6ODKRWo4qq56e4WB68W22Vzd7V9LWajBw==",
        },
        {
            "url": "https://puzz.link/p?shimaguni/15/12/55a19a6l11nhcnqlddnqkr5cmajmaoeahc3gqv3nftavvke414681sk3e7cekml25fok2o43g1s",
            "test": False,
        },
    ],
}
