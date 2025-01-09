"""The Cojun solver."""

from typing import List

from noqx.puzzle import Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_num_adjacent
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(unique_num(_type="area", color="grid"))
    solver.add_program_line(avoid_num_adjacent(adj_type=4))
    solver.add_program_line(":- area(A, R, C), area(A, R + 1, C), number(R, C, N1), number(R + 1, C, N2), N1 < N2.")

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        assert isinstance(num, int), f"Clue at ({r}, {c}) must be an integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Cojun",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7ZVPb9NMEMbv+RTVnvfg/RN717dQUi4l/GlRVVlWlbaGBpI3kDQIOcp37zOzs6RFlRB6BfSALK+eXc9unvmNx1l/2UxXnQ64XNCFNrict3zbIvJdyHU6u5139YEebW5vlisIrV8dHen30/m6GzQS1Q62faz7ke5f1I0ySiuL26hW92/qbf+y7se6P8EjpQ3WjlOQhRzv5Rk/J3WYFk0BPRENeQ55NVtdzbuL47Tyum76U63od57xbpJqsfzaKfFB86vl4nJGC5fTWySzvpl9lifrzfXy00ZiTbvT/SjZnTxi1+3tkkx2ST1il7L4zXZju9sB+1sYvqgb8v5uL8NentRbjJN6q2yJrQ615sooZzCl0qepd5ja/XT44KkpLOZ+PzfFD3M6bXhv7u/thwHDNs55POLR8ngKl7p3PD7nseBxyOMxx4xh3pR4TyuYsDixxA9XyIZ0hfUg6xV+MCAP1sglwARrZB2QEGvsDbI3ICZKTMB6zOtIJFaiK+goOqA3kDjp6KElPg6hJT6W0EE04gkUa/QVQYLGPugUg33Q6XzuPSsxpoBOeVmDvrTJJ/Zp69KZiIVO+VrroFOOiIVO3qxDDNWWNc7xco6DBy8ePPwPk3+saVuK5zKCs2him/kTzyqzpVpktuCW60Jscy2IbeYfSujMNkALWzD8zj8S88yQvkeSb0H8hRXxyTwNcjT3WBnJl1hltobYZm7EVvYSw8yZGGbODjHUIpmhkxhimJk7Yp7jibnwJ7Yu8yT+spe+r7kWHvHUZJm/l3p5qkvei3eDa4QmOONWOOTR81hyi1TU5r/0Ifj/3fhTO41FlR9c9Gn4g/N20Kjx9YfuYLJcLaZzfEAnm8Vlt8pz/GPtBuqb4ps/iv7fn9hf+hOjEhRP7Q1+anbQU4D6cfOfagd3"
        }
    ],
}
