"""The FourCells solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape


class FourCellsSolver(Solver):
    """The FourCells solver."""

    name = "FourCells"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VVLj9owEL7zK1Y+z8GvPC8V3UIvlG0LqxWKIgRs2kUNCgVSVUb8944nUFo7qxXqqpWqlePR5BtP5vN4Mt5+rWebAkRoHxUDB4Ej1CHNIE5o8uMYL3dlkV5Bt949VBtUAG76ffg0K7dFJzuuyjt7k6SmC+ZtmjHJgKZgOZgP6d68S80QzAhNDARiA9QEA4lq76zekd1q1w0oOOrDo47qBNXFcrMoi+mgQd6nmRkDs3Fek7dV2ar6VrDGjd4X1Wq+tMB8tsPNbB+W66NlW99XX2p2CnEA023o9lroqjNd9ZOuaqcrn4Vuua7aiCb54YAJ/4hUp2lmWd+e1fisjtL9wTLaM52c9ticCgu0A4QeEDiA4JGLCOkhnpdULqJDFwm4h3jfibxYkccn9mLF3nfi2EMoOa9+QRLuIe53JHe9pHC9pJcfKV3OUrl7l9rdhfROS3rZkJGbVentXSZuLMXdWIq7+VHeLpR3gioQHvJ7dCxEQeU4IdknKUmOsVrBKJJvSHKSAckBremRvCN5TVKTDGlNZOv9oj/iz+lgZWtMTBID01qDtj+QepJjpiV128dH8GL/n+15J2O9+8/F1bDarGYltvdhvZoXm9M73qSHDvvOaGYKXfTL5frXL1ebfH7ZFetcoP++32VmBDoBcwNsXU9n00WF1YZZfByfXIgPLd6cyLHrty1oceyde2a7WchQXW7B3upanrnpP30m2OLzzg8=",
        },
        {"url": "https://puzz.link/p?fourcells/10/10/d3g1c3g1c3b1a3b1j3a13a3j1b1a3b1c3g1c3g1d", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row * puzzle.col % 4 == 0, "It's impossible to divide grid into regions of this size!")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))

        for i, o_shape in enumerate(OMINOES[4].values()):
            self.add_program_line(general_shape("omino_4", i, o_shape, color="grid", adj_type="edge"))

        self.add_program_line(all_shapes("omino_4", color="grid"))
        self.add_program_line(count_shape(target=puzzle.row * puzzle.col // 4, name="omino_4", color="grid"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent_edges(num, (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
