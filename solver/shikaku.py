"""The Shikaku solver."""

from typing import List, Tuple

from .core.common import display, edge, grid
from .core.helper import extract_initial_edges, tag_encode
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import bulb_src_color_connected
from .core.shape import all_rect_region
from .core.solution import solver


def shikaku_cell_constraint(target: int, src_cell: Tuple[int, int]) -> str:
    """
    Generate a cell-relevant constraint for shikaku.

    A bulb_src_color_connected rule should be defined first.
    """
    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {count_r}, {count_c}, CR * CC != {target}."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(extract_initial_edges(puzzle.edge, puzzle.helper_x))
    solver.add_program_line(all_rect_region())
    solver.add_program_line(f":- {{ upleft(R, C) }} != {len(puzzle.text)}.")

    for (r, c), clue in puzzle.text.items():
        solver.add_program_line(f"clue({r}, {c}).")
        solver.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

        if isinstance(clue, int):
            solver.add_program_line(shikaku_cell_constraint(clue, (r, c)))

    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
    solver.add_program_line(f":- clue(R, C), clue(R, C), (R, C) != (R1, C1), {tag}(R, C, R, C1), {tag}(R1, C1, R, C1).")
    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Shikaku",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VTLbtswELzrKwye90CKsh68uandi6s+4iIIBCGQHbYxYkOtZBUFDf97dpdKZBW59NA2BQqa45nla7z0sv3WVY0FJemjU8BvbJFKuYdpzF32bbU97KyZwKw73NUNEoB3iwV8rnatDYp+VhkcXWbcDNwbU4hQAHclSnAfzNG9NS4Hd4lDAhTGlsiUgBDpfKBXPE7swgeVRJ57niC9RrrZNpudvVn6jd6bwq1A0DmveDVRsa+/W+GXsd7U+/WWAuvqgD+mvdt+7Ufa7ra+7/q5qjyBm3m782fs6sEuUW+X2O+ya2+/2LZbP+c1K08nzPlHdHtjCjL+aaDpQC/NETE3R6GnuDSDxF+LiFKU6ZOMQ5Txk0ySkUxjlHqQ2UhmmkxN8Ec/BqKfAkqq0X5K0nHRmaYDxivojFFEkeOzPTQde7ZHNPasYnmmMQmKU3HNuGAMGVeYKXCa8TWjZJwyLnnOnPGK8YIxYox5TkK5/qXb+AN2Cu3retym/16sDAoxx0qY5HWzr3ZYDXm3X9vmUePbcwrED8Ed/5b4lP1/jv7Gc0T5ly+tDF6aHSxMgTd+X2HuyuAB",
        },
        {
            "url": "https://puzz.link/p?shikaku/24/14/h5x6i.j8g6lag4j.l9i8j6i4l3z9g6i4i4h56h6i4i6j8h4n3h6zn4j4r6j4g6j8i8hci6j8q6h2r8k5l8k8j.l9j4l.lataock36kck",
            "test": False,
        },
    ],
}
