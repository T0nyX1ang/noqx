"""The Paintarea solver."""

from typing import List

from .core.common import area, display, grid, shade_c
from .core.helper import full_bfs
from .core.neighbor import adjacent, count_adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.shape import area_same_color, avoid_rect
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(grid_color_connected(color="gray", adj_type=4, grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))
    solver.add_program_line(avoid_rect(2, 2, color="not gray"))
    solver.add_program_line(area_same_color(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, (ar, _) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c), num in puzzle.text.items():
        if num == "?":
            continue

        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(count_adjacent(num, (r, c), color="gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Paintarea",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7ZZBb5tOEMXv/hTRnvfAwgK73NLU7SV1+/87VRQhFBGHNFbtOsWmqrD83fNmmA0+RKqqtmoOFfb4t8NjmX07IG+/dnXb6BxH4nSkDY4ksvzNIvqE42K5WzXFiT7tdvebFqD1+5m+q1fbZlKKqJrse1/0p7p/W5TKKK1ifI2qdP9fse/fFf1U93OcUtohdz6IYuB0xEs+T3Q2JE0EngkDr4CLZbtYNdfnQ+ZDUfYXWtF9XvHVhGq9+dYoqYPGi836ZkmJm3qHtWzvlw9yZtvdbj53ojXVQfenQ7nzZ8pNxnIJh3KJnimXVvGHy/XV4QDb/0fB10VJtX8c0Y04L/aIs2Kv4hSX0kbzzqjMYJg8DV2EYSxDXGH4uiuObzjGHC8wre4Tjq85RhxTjuesmeJuJkm1sZkqYsyIHjPWD2yRTyVvkU9D3muToQjiNAc7YWgy0aTQ5KJBj5oca2CGPhd9Bg0thjiHxokmx+JcIow5ncyZQ+9F76DxonFex5HkfQSWeXwMFo1PwFbYgmExGFodm1gYeTPkjbXwIXAGzoVRv5X6yYc0+ID6U7lvCn0qevIk+EY+0F4yY3uz4b7sSfAwO/KQPAm+kSd58OTIQ/IkeOiOPHSY38n85FXwE/4YH/yBxosG/sAX8WH0kP2Jgj+jn/h98hNegqlP0FCX3FZnHC3HjNstpx7/qafg1zv7h+WUMXb56EC//+5RNSnVvGvv6kWDd8P09lNzMtu063qF0axb3zRtGOPVfJio74q//Ljbf2/rv/S2pi2IXlq3vrRy8Pyoh3r5ZYf/J7WqJo8=",
        },
        {
            "url": "https://puzz.link/p?paintarea/18/10/fesmfvrsi3vrvsntsvuttippjvnvrnvdferjbmtvtmnftnrnvrfbanmunev6vffddd8a1zj2b0t2b2a2c1o1d2b1c3zx2d2a2a3t",
            "test": False,
        },
    ],
}
