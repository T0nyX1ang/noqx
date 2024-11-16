"""The Mochinyoro solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import (
    count_reachable_src,
    grid_color_connected,
    grid_src_color_connected,
)
from noqx.rule.shape import all_rect, avoid_rect, no_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(grid_color_connected(color="not black", adj_type=8, grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="black"))
    solver.add_program_line(all_rect(color="not black"))
    solver.add_program_line(no_rect(color="black"))

    all_src = []
    for (r, c), _ in puzzle.text.items():
        all_src.append((r, c))
    assert len(all_src) > 0, "No clues found."

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(f"not black({r}, {c}).")
        current_excluded = [src for src in all_src if src != (r, c)]
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color="not black"))
        if isinstance(num, int):
            solver.add_program_line(count_reachable_src(num, (r, c), color="not black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Mochinyoro",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVRj5pAEH73V1zmeR5YFhB5aez17Iv12mpzuRBikHKRFItFaa5r/O83M9AA3jWpaWKTptH98s3szO7HjIy7b1VcpqgUf7WPFhJDx/VkKWXLsprPItvnaXCF42q/LkoiiLeTCT7E+S4dhE1UNDiYUWDGaN4GIShAsGkpiNB8CA7mXWBmaOa0BajIN62DbKI3Lb2TfWbXtVNZxGcNJ3pPNMnKJE+X09rzPgjNAoHveS3ZTGFTfE+h0cF2UmxWGTtW8Z4eZrfOts3OrvpcfKmaWBUd0YxrufOfcllOI1e3cpnWcpm9IJfT/lxuvi1eEjqKjkcq+EeSugxCVv2ppX5L58GBcBYcQHuc+opU1F0BxyYHt70xh2RS3xvT1SfhnnPiGFq9fF/18v3+cSO+rGP6vVxljXrbSrl922bxnXjdP07p/m3KYfUd22XxHdtj7d2HUUOW3/ecnOnznU7H5mdoM6jMSop9LzgRtAUX1As0WvCNoCXoCk4l5kbwTvBa0BH0JGbI3fzNfgMXx0bQVAOnbv4FtIWaS/X84/673mgQwrwqH+IkpVd0Vm1WaXk1K8pNnANNw+MAHkFWqHm4/h+QFx+QXHzrrDH599/ikOpK75K5RdhWy3iZFDnQvyuKX//Cf278uf7n51+8ajRi6FeQrLOvP4qygGjwBA==",
        },
        {
            "url": "https://puzz.link/p?mochinyoro/17/17/hdzmenajfzh71zw4zu6i5zu3zw-108zh2jcn9zmbh",
            "test": False,
        },
    ],
}
