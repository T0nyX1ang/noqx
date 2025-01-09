"""The N Cells solver."""

from typing import List

from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    assert puzzle.row * puzzle.col % 4 == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))

    for i, o_shape in enumerate(OMINOES[4].values()):
        solver.add_program_line(general_shape("omino_4", i, o_shape, color="grid", adj_type="edge"))

    solver.add_program_line(all_shapes("omino_4", color="grid"))
    solver.add_program_line(count_shape(target=puzzle.row * puzzle.col // 4, name="omino_4", color="grid"))

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
    "name": "FourCells",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VVPj9o+EL3zKVY+zyH+k5DkRrehF5ptf1CtUBShwKZd9AsKBVJVRnz3HU+yQrWzqhASh2oVPHp5YzNvxqPJ/mdT7ErggfnJEDzg+AQqoOWHES2ve2brQ1XGdzBqDs/1DgHAw3gM34tqXw6yblc+OOoo1iPQn+KMCQa0OMtBf42P+nOsU9BTdDHgyE0QcQYCYXKGj+Q36L4luYc47TDCOcLVereqysWkZb7EmZ4BM3E+0GkD2ab+VbL2GL2v6s1ybYhlccBk9s/rbefZN0/1/023l+cn0KNWbtIjV3ZyVQtbuQb1yDVZXC+32tZ9QqP8dMKC/4dSF3FmVH87w/AMp/ERbRofmYpec2xvhfnKIgKH8C2Ce0Ob4cJhnFNC2owKbMb3HMb5n6ETa+joCZ1YofM/YWgzkb1HOHkJYccS0tYslB1dOFUWThZiaFdDOJpFZMeSnh1LenZe0slCOpWXPneYP6NjA3FqoznZMVlBdoZdBlqS/UjWI+uTndCehOwj2XuyimxAe4amTy/q5OvlYEcqLEwUAlNKgTKNL/+qMVOCpuTbj//u/5f9+SBjydOP8i6td5uiwrGcNptluXt9xy/gacB+M1qZxCPq/aN484+iKb5344Fy7XzL9BRUBPoB2LZZFItVjd2FVXubn1/Ip4Zvb6Cb8n0beg4m5xnZ7+YikJd7cJbanpvfCY70fPAC",
        },
    ],
}
