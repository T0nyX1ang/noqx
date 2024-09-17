"""The Kakuru solver."""

from typing import List, Tuple, Iterator

from .core.common import area, display, fill_num, grid, unique_num
from .core.penpa import Puzzle, Solution
from .core.neighbor import adjacent
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:

    def get_adj_8_neighbors(r: int, c: int) -> Iterator[Tuple[int, int]]:
        """Get the 8-adjacent cells of (r, c)."""
        data = [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1), (r, c - 1), (r, c + 1), (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]

        for x, y in data:
            if puzzle.surface.get((x, y)) != 4 and x in range(0, puzzle.row) and y in range(0, puzzle.col):
                yield (x, y)

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(":- adj_8(R, C, R1, C1), number(R, C, N), number(R1, C1, N).")

    area_id = 0

    for (r, c), clue in puzzle.text.items():
        neighbors = tuple(get_adj_8_neighbors(r, c))
        assert len(neighbors) > 0, "Invalid clue position."

        solver.add_program_line(f"black({r}, {c}).")
        solver.add_program_line(area(_id=area_id, src_cells=neighbors))
        solver.add_program_line(fill_num(_range=range(1, 10), _type="area", _id=area_id))
        if clue != "?":
            assert isinstance(clue, int), "Clue should be integer or '?'."
            solver.add_program_line(f":- #sum {{ N: area({area_id}, R, C), number(R, C, N) }} != {clue}.")

        area_id += 1

    for (r, c), color_code in puzzle.surface.items():
        if color_code == 4:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(unique_num(_type="area", color="grid"))
    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions
