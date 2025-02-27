"""The Norinori solver."""

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.variety import nori_adjacent
from noqx.solution import solver


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))

    solver.add_program_line(adjacent())
    solver.add_program_line(nori_adjacent(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count(2, color="gray", _type="area", _id=i))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))

    return solver.program


__metadata__ = {
    "name": "Norinori",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7ZXPattMFMX3foow61lo/kia0S5NnW7SpK1TQhDCKI7SmCpVKscfRcbvnnNnrhAfhDaQ4lURuhxf/cY+c3w93vzc1n0jHS7jZCIVLmN1uHXiw53wdbl+apviSB5vn+67HkLKi9NTeVe3m2ZWMlXNdoMvhmM5fChKoYQUGrcSlRw+F7vhYzHM5bDAIyEdemcR0pDzSV6F56ROYlMl0OesIa8hV+t+1TbLs9j5VJTDpRT0Oe/CapLiofuvEeyDXq+6h5s1NW7qJ2xmc79+5Ceb7W33fcusqvZyOI52Fy/YNZNdktEuqRfs0i7ebrd97F4y6qv9HoF/gdVlUZLrr5N0k1wUO9TzUFWo16GehqpDvQQqBxPq+1CTUNNQzwIzL3ZCZVqq3IpC43vNrVQuY51Bu6idkcqnrMF4ZlwO7Vk7jFcStc+gea1HX8U+nkNr1mBUZMBKrZlRYDQzSkEb1hhhHX1qjb7hvkbfjH0DHX2ChY4+tQFjmTFgLDMmhc5Zw49lPxZrU15rwaTM2Bw67hes1Bnvl7LKIxOycpwnZeXG3NIpW0fZjjwyHHP2lDOv9ZQzr0WeyjPvKfMp2zF/ncBnwp4ptzFnRfkzo3AEjDlryllNGY45azCGGQPGMGMoc35PynDM3KJvuU/HjOX3sZQzMRi0qzBuJ6HaULMwhjnN8ysnXui4uRTe3N8a/z96KzWi/9+Fr/GQr6tZKRbb/q5eNTgy5rffmqPzrn+oW4GzeT8Tv0S4S0yOtP+O64Mf1xR+cuBD+62/qBK5Yq6HCyket8t6uepagf96+bt+mryaP/hu8TMVP7p+TbeoZs8=",
        },
        {
            "url": "http://pzv.jp/p.html?norinori/20/10/ahkcfeorctdhkqdffmk9jprqnqd57ea6us16ok4jboec2oku7ck43rbqseje3kc16cvv8f7i7f",
            "test": False,
        },
    ],
}
