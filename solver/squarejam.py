"""The Square Jam solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region, avoid_edge_crossover


def squarejam_constraint(target: int, src_cell: Tuple[int, int]) -> str:
    """Generate a constraint for squarejam size."""
    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)

    src_r, src_c = src_cell
    return f":- {{ {tag}({src_r}, {src_c}, R, C) }} != {2 * target - 1}."


class SquareJamSolver(Solver):
    """The Square Jam solver."""

    name = "Square Jam"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VRNb5tAEL3zK6I5z4FlAbNcKie1c3GdtnEURQhZ2CGJFVukYKpqLf57Zwdj0k2iqkqUqlKFeXrMB/v8ltnqW52VOSoUAmWELgo0xEU/CFENzM/dX7PVdp3HRzist3dFSQTxbDzGm2xd5U6yr0qdnVaxHqI+jRPwAPkWkKL+Eu/0p1hPUZ9TCtCn2ISYAPSIjnp6yXnDTtqgcIlP95zoFdHlqlyu8/mkjXyOEz1DMOscc7ehsCm+59C28fOy2CxWJrDItvRnqrvVwz5T1dfFfQ3dEg3qYSt31MkVvVzZy5UHufJ5ud5byM2vb/OqXjynVaVNQ55/JbXzODHCL3oa9fQ83jVG1A6C0LRKEtJuDAQDE/jwKBBBu3mHgLIqQteqCJX10sizKlRgvUOFdsDWoWwdwo26LeoinrCahPQtKUIGTyK2B0Laiwv561rknmAPrxjHjB7jjCxGLRk/MrqMAeOEa0aMl4wnjD5jyDUDs0l/tI2vlwO+Ty6oiEaUJt8LyEj5W4mJF/ER8fgK/r1I6iQwoqE6mhblJlvTYE3rzSIvu2c6xhoHfgDfiaQW///J9jdONuO/+86D8do5Tcjaw0yhPkN4qOfZfFnQd0b+mXQo5EsJ/606aLyfJN7dKToxUucn",
        },
        {"url": "https://puzz.link/p?squarejam/11/11/zj1h2h3zl2h3h3zl2h1h3zj", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region(square=True))
        self.add_program_line(avoid_edge_crossover())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))
            if isinstance(num, int):
                self.add_program_line(squarejam_constraint(num, (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
