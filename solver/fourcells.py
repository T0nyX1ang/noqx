"""The N Cells solver."""

from typing import List

from .core.common import display, edge, grid
from .core.helper import extract_initial_edges
from .core.penpa import Puzzle, Solution
from .core.neighbor import adjacent, count_adjacent_edges
from .core.shape import OMINOES, all_shapes, general_shape, count_shape
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