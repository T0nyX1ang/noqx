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
            "data": "m=edit&p=7VZfb9o+FH3nUyA/+yH+k5DkjfVXfi+MbqNTVUURClmqooWFBdJNRnz33ntDZZt106ZJ7AWFXN3je2wfH8ch269d0VZcjPCnYh5wAVcUa7qlDOh+uW5Xu7pKh3zc7R6bFhLObyYT/lDU22qQHVn5YG+S1Iy5+T/NmGCcSbgFy7l5n+7N29TMuJlDiXEBbdOeJCG9tukd1TG76htFAPnsmEN6D2m5asu6Wkz7lndpZm45w3neUG9M2bp5qthRB+KyWS9X2LAsdrCY7eNqc6xsu0/N5+7IFfmBm3Evd/4iV1u5ysrFtJeL2StycRV/L7feNK8JTfLDAQz/AFIXaYaqP9o0tuk83UOcpXsWRtAVd5n2hIUjD44UQGWh9iGSHRh7MAl8KLyRExzKgaFHFoE/tAhwbEsXwh9NCAk4slgiXzs4ASwt1if99Un/CHHsYDTC4SdYdzHW7XxSILbzSeEvV0q03alL33epETvjad9bSdY7fPLe6pfJCT/B9Vu+Iv9sXZF/Tp38s+OpE/+UQr7Vp5Tvj9K4n6GDcb0OX+N4zvwhPixOf/Lfxb6fKvIfWxWhH8588Qk/dv2HR1/QAbinOKEoKd7C+eBGUfyPYkAxpDglzjXFO4pXFDXFiDgjPGG/eQaZBlmaM1yN7A/kGbRlGjfi1xdaeWFcGD+58kHG5l37UJQV/A3NuvWyaoezpl0XNYN//MOAfWd00xnXl4+As38EoPnBH30K/Pu3Yga+wrvJ3HC26RbFomxqBl+QHNuj6If2s6uHVycriy9FPXxaVd9YPngG",
        },
    ],
}
