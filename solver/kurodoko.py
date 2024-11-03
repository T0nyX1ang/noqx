"""The Kurodoko solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="black"))
    solver.add_program_line(grid_color_connected(color="not black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(bulb_src_color_connected((r, c), color="not black"))
        solver.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Kurodoko",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VRNb5wwEL3zK6I5+4AxOKxv2zTby5Z+sFUUIRSxlCgoIKewVJUR/z3jgdahyqWHRqlUef32Pc/YfgzY/beh6CrGffsTMcN/bCGPqQexpO4v7VCfmkqdse1wutMdEsY+7Hbstmj6ysuWrNwbzUaZLTPvVAYcGATYOeTMfFKjea9MwkyKIWAhju3npADppaNXFLfsYh7kPvJk5hLpNdKy7sqmutljFEc+qswcGNh93tBsS6HV3ytYfFhd6vZY24FjccKH6e/qhyXSD1/1/bDk8nxiZjvbTZ+xK5xdS2e7lv01u82Dfs7oJp8mLPhntHqjMuv6i6Oxo6kaERM1gvBxqmByficgBMrASYkycnKzSpbruTJCKX/J82C1VMxXS3Eeoo6dDtY789+McWFXD52OrDW3G4+styfzpd3+yX7k7mccH55TCa4Jd4QB4QErxIwgfEvoE0aEe8q5JLwivCAMCSXlnNsa/9FbeAE7mZgP87pF/95Y7mWQDt1tUVZ4ApKhPVbdWaK7tmgAL5vJgx9AHT8evLv+3z8vfv/Y4vuv7ft/bXbwRML90GksnobcewQ=",
        }
    ],
}
