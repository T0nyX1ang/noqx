"""The Heteromino solver."""

from typing import List

from .core.common import display, edge, grid
from .core.penpa import Puzzle
from .core.helper import extract_initial_edges, tag_encode
from .core.neighbor import adjacent
from .core.shape import OMINOES, all_shapes, general_shape
from .core.solution import solver


def avoid_adj_same_omino(color: str = "black") -> str:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An split by edge rule, an omino rule should be defined first.
    """
    t_be = tag_encode("belong_to_shape", "omino", 3, color)
    constraint = "split_by_edge(R, C, R + 1, C) :- grid(R, C), grid(R + 1, C), edge_top(R + 1, C).\n"
    constraint += "split_by_edge(R, C, R, C + 1) :- grid(R, C), grid(R, C + 1), edge_left(R, C + 1).\n"
    constraint += "split_by_edge(R, C, R1, C1) :- split_by_edge(R1, C1, R, C).\n"
    constraint += f":- grid(R, C), grid(R1, C1), {t_be}(R, C, T, V), {t_be}(R1, C1, T, V), split_by_edge(R, C, R1, C1)."
    return constraint


def solve(puzzle: Puzzle) -> List[str]:
    shaded = len(puzzle.surface)
    assert (puzzle.row * puzzle.col - shaded) % 3 == 0, "The grid cannot be divided into 3-ominoes!"

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(extract_initial_edges(puzzle.edge, puzzle.helper_x))

    if shaded == 0:
        solver.add_program_line("black(-1, -1).")

    for (r, c), _ in puzzle.surface.items():
        solver.add_program_line(f"black({r}, {c}).")
        solver.add_program_line(f"edge_left({r}, {c}).")
        solver.add_program_line(f"edge_left({r}, {c + 1}).")
        solver.add_program_line(f"edge_top({r}, {c}).")
        solver.add_program_line(f"edge_top({r + 1}, {c}).")

    for i, o_shape in enumerate(OMINOES[3].values()):
        solver.add_program_line(general_shape("omino_3", i, o_shape, color="not black", adj_type="edge"))

    solver.add_program_line(all_shapes("omino_3", color="not black"))
    solver.add_program_line(avoid_adj_same_omino(color="not black"))
    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions
