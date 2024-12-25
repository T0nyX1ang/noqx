"""The Araf solver."""

from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected
from noqx.solution import solver


def araf_region_clue_count(src_cell: Tuple[int, int]) -> str:
    """Generates a constraint for counting the number of clues in a row / col."""
    src_r, src_c = src_cell
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    rule = (
        f"araf_link({src_r}, {src_c}, R, C) :- {tag}({src_r}, {src_c}, R, C), clue(R, C, _), (R, C) != ({src_r}, {src_c}).\n"
    )
    rule += f":- #count {{ R1, C1 : araf_link({src_r}, {src_c}, R1, C1) }} != 1."
    return rule


def araf_region_count(src_cell: Tuple[int, int]) -> str:
    """Generates a constraint for counting the number of cells in an araf area."""
    src_r, src_c = src_cell
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    cnt_area = f"N = #count {{ R0, C0: {tag}({src_r}, {src_c}, R0, C0) }}, (N - N1) * (N - N2) >= 0"
    rule = f":- araf_link({src_r}, {src_c}, R, C), clue({src_r}, {src_c}, N1), clue(R, C, N2), {cnt_area}."
    return rule


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)

    assert len(puzzle.text), "No clues found."
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."  # ignore clues with ?
        solver.add_program_line(f"clue({r}, {c}, {num}).")
        solver.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))
        solver.add_program_line(araf_region_clue_count((r, c)))
        solver.add_program_line(araf_region_count((r, c)))

    for r, c, d in puzzle.edge:
        solver.add_program_line(f":- not edge_{d.value}({r}, {c}).")

    for r, c, d in puzzle.helper_x:
        solver.add_program_line(f":- edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Araf",
    "category": "region",
    "examples": [
        {"url": "https://puzz.link/p?araf/9/9/44g644g14h9i9h33h4h61h1i9h9h395h1g4k1g6g4i7g1g2g9g1g4i9g5g9h", "test": False},
    ],
}
