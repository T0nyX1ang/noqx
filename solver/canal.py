"""The Canal View solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(bulb_src_color_connected((r, c), color="black"))
        solver.add_program_line(count_reachable_src(num + 1, (r, c), main_type="bulb", color="black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Canal View",
    "category": "shade",
    "aliases": ["canalview"],
    "examples": [
        {
            "data": "m=edit&p=7VVNb5tAEL37V1h73gP7AQZubhr34rofdhVFCEXYJYpVXFJs0mot//fMDES7i9JIVaUoBwszmrfzdvbtgzX7X23RlFxM8KdiHnABVxRruqUM6H66VttDVaZjPm0Pd3UDCeefZjN+W1T7cpT1rHx0NElqptx8SDMmGGcSbsFybr6kR/MxNQtullBiXMDYvCNJSC9tekV1zC66QRFAvuhzSK8h3WybTVXezLuRz2lmVpzhOu9oNqZsVz+UrNeBeFPv1lscWBcH2Mz+bnvfV/bt9/pH23NFfuJm2sldPsnVVq6ycjHt5GL2jFzcxf/Lre7r54Qm+ekEhn8FqTdphqq/2TS26TI9QlykRxZGMBWfMj0TFk48OFEAlYXah0h2YOzBJPCh8Don2MqBoUcWgd9aBNjb0oXwuwkhAUcWS+RrByeApcV6MF8P5keIYwejEQ4/wbqLsW7XkwKxXU8Kf7tSou1OXfq+S43Y6ad9byVZ7/DJe6tfJgN+gvu3fEX+2boi/5w6+Wf7qYF/SiHf6lPK90dpfJ6hg3G/Dl9jP2f9EF8WZz7572LfTxX5r62K0A9nvXjAj13/4dUXdACuKc4oSoorOB/cKIrvKQYUQ4pz4lxSvKJ4QVFTjIgzwRP2T2fwFeRkGr1/+UL3zowz4y9XPsrYsm1ui00JX55Fu1uXzXhRN7uiYvCRP43YH0Y3HWt9/u6/+ncfzQ/e2j/PW5MD/4VsU/wsqvHDtvzN8tEj",
        },
    ],
}
