"""The N Cells solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.reachable import grid_src_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))

    all_src = [(r, c) for (r, c), clue in puzzle.sudoku.items()]
    assert len(all_src) > 0, "No clues found."

    for (r, c), clue in puzzle.sudoku.items():
        solver.add_program_line(f"not black({r}, {c}).")

        current_excluded = [src for src in all_src if src != (r, c)]
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color=None, adj_type="edge"))
        tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
        solver.add_program_line(f":- grid(R, C), not {tag}(_, _, R, C).")

        clue = {"u": clue[4], "r": clue[5], "l": clue[6], "d": clue[7]}
        constraint = {"u": f"R < {r}", "l": f"C < {c}", "d": f"R > {r}", "r": f"C > {c}"}
        for direction, num in clue.items():
            if not isinstance(num, int):
                continue
            solver.add_program_line(f":- #count{{ (R, C): {tag}({r}, {c}, R, C), {constraint[direction]} }} != {num}.")

    for r, c, d in puzzle.edge:
        solver.add_program_line(f":- not edge_{d.value}({r}, {c}).")

    for r, c, d in puzzle.helper_x:
        solver.add_program_line(f":- edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Compass",
    "category": "region",
    "examples": [
        {
            "url": "https://puzz.link/p?compass/9/9/p.96.k..8.zh5..1i...2h..37z0224i.4..o",
            "test": False,
        },
        {
            "url": "https://pzplus.tck.mn/p?compass/8/12/...4...8j.51..72.y.4.711..zx31..1.1.y6..71..1j..0...5./",
            "test": False,
        },
    ],
}
