"""The Stostone solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, avoid_area_adjacent
from noqx.rule.reachable import area_color_connected
from noqx.solution import solver


def valid_stostone(color: str = "black") -> str:
    """
    Generate a constraint to enforce a valid stostone dropping.

    A grid rule should be defined first.
    """
    below_C = f"grid(R, C), {color}(R, C), #count {{ R1: grid(R1, C), {color}(R1, C), R1 < R }} = BC"
    below_C1 = f"grid(R, C + 1), {color}(R, C + 1), #count {{ R1: grid(R1, C + 1), {color}(R1, C + 1), R1 < R }} = BC1"
    return f":- {below_C}, {below_C1}, BC != BC1."


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.row % 2 == 0, "The stostone grid must have an even # rows."

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(count(puzzle.row // 2, color="gray", _type="col"))

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
    solver.add_program_line(valid_stostone(color="gray"))
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Stostone",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VZNb9s4FLz7VwQ88yB+iZRuaersJeu0dRZBIBiG4yiNsXad+qMoZPi/Zx75CBVtgbQoNosChW16/DR6HHFGtLYf97NNK5WSqpAmyEICSetKaVWQTvn4Kfh1tdgt2/pEnu53D+sNgJSX5+fyfrbctoOGWZPBoavq7lR2f9WNUEIKjY8SE9m9rQ/d33U3lN0Yh4RUqF0kkgYc9vA6Hid0loqqAB4xBrwBnC8282U7vUiVN3XTXUlB87yKZxMUq/WnVrAO+j1fr24XVLid7XAx24fFIx/Z7u/W/+6ZqyZH2Z0mueMsN/RyTS+XYJJL6Dty6Sr+Y7nV5HjEsr+D4GndkPZ/ehh6OK4PGEf1QZQWpzp4Tc6gpuKRmziex1HH8Qonys7E8XUcizi6OF5EzhD9tK6ktmiq4bcxwIGxBa4StsAu41LqUjEOwIYx+pA4wk4Bl4zB8cwpNbBnjJ6ee5boGbinBycwx0NPYD0e/MB8D36V+R5YM4aGijUEaKhYQ/DSFMwJAZj1hAqY+ZUCZn6lgVlDZYF53qqURqV50Q84cdAPOOlEP+DEN4WTRheMca7O50KPTnrQGzhpQD9pDNdxGxuTdKIfMHM07nfjGEOzSZqNxlyW5zLQZlkbPDXsKXoAszaDuRzPZdDfcX+Lesl1+GvYX5wHzBz4a9hf9ADmuRw0eNYArw17DS72KL72Ev0D9/e0d6VriRmzGTvgnB/4yDpjlnIOHeUtzYXvPpMlZY/5lLecT4+6zzmhHOY6MuY5A5Qxzxo8NPg+D7pifgU+Zyx6XbAX5DXnBxlBBr7wMedBY000r6eGL9l3jT46e0qZyZ5SZrKPODfnwYCTfTfgmMyh/GSvKT/Za3iXs2Gx5pa9sNBps9eUAeY4cBxzHLQ51kb+uuw75nXZX8oAaytxXTEn2GCu4zZzFkcbxzJuP552tR/c9wQJDFLEudIm+Ovb3rPaGiw3/aN+/aKd97evTgaNGO8397N5iz+l4d379mS03qxmS/wa7Ve37Sb/xjPBcSA+i/hpDD1i/HlM+J8eE8iC4qceFl7gPnlGToPVtVp2l1I87qez6XyNjGHtqO78N/UXV48bXWx3a7w/tGIyeAI=",
        }
    ],
}
