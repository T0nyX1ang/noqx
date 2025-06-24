"""The Square Jam solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region, avoid_region_border_crossover


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
            "data": "m=edit&p=7VTRbpswFH3nKyo/3weMgWC/TFmX7CWj25qpqhCKSMrWqInoIEyTo/x7772QJvU6TVOmTpMmwtHh+BofjnPdfG2LugQNUoJKwAeJl0p8CKMY9IB+fn9Nl5tVac5g2G5uqxoJwMV4DJ+LVVN6WV+Ve1urjR2CfWsyEQjgW4oc7Aezte+MTcFe4pCAELUJMikgQDo60CseJ3beidJHnvYc6TXSxbJerMrZpFPem8xOQdA6r3k2UbGuvpWim8bPi2o9X5IwLzb4Mc3t8r4fadqb6q7ta2W+Azvs7I72dmmV3q462CXa2SX2jF36ipPtljdfyqadP+dV57sdZv4R3c5MRsY/HWhyoJdmi5iarYhimqrQSLcxIhqQ8OpISEjAjXsUtFMR+05FzBVHL00Cp0JHzjs0+zgWXB/a9SF9VijivRJIZ5JUoWNFKl76ieJmIJW7uFRP18L0JGd4zThmDBinGDFYxfiG0WeMGCdcM2K8YjxnDBljrhnQJv3WNp5uR4QhpqATbFHs/CDCINUvLWZBwkfE8RX9e0ruZWKETXWWVvW6WGFjpe16Xtb7ZzzGdp74LvjOFE4J/59sf+Nko/z9F26MU/s0w2gfewrsBYj7dlbMFhX+zzA/Go6l+tlA+KdmYHv/MPDiSeGJIfDPeFfgtubeAw==",
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
        self.add_program_line(avoid_region_border_crossover())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))
            if isinstance(num, int):
                self.add_program_line(squarejam_constraint(num, (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
