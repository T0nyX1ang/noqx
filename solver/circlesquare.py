"""The Circles and Squares solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, invert_c, shade_c
from noqx.rule.helper import validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import all_rect, avoid_rect


class CircleSquareSolver(Solver):
    """The Circles and Squares solver."""

    name = "Circles & Squares"
    category = "shade"
    aliases = ["circlesandsquares"]
    examples = [
        {
            "data": "m=edit&p=7VXBbtswDL37KwaeOcCS7MTWLcuaXdJ2WzIUhWAErueuxpy6S+JtVZB/L0Ub8ME6DAOaXQaBD09PjPRCRcz+R5vvSkxoqARDFDRUJDlkmHKE/VhXh7rUb3DWHh6aHRHE68UC7/N6Xwamz8qCo021naH9oA0IQJAUAjK0n/TRXmoomu1dBWhXtA6Y0MKyy5RELwZ6w+uOzTtRhMSvek70lmhR7Yq63Cw75aM2do3gDnvHn3YUts3PEnozbt4ZIOGu/vXQa/v2a/O97bNEdkI7Y7d25TGqBqOOdkYd8xh1/l/NaJqdTlTvz2R1o41z/WWgyUBX+kh4xSgYb/URVELbCDqms3bJ1iAKSZUjVXpzY58au9zRDrHyqRO/GnnV1HfadOpTRei2GMtC+GXv1xNiMpapeAsuoWRcU4XRKsb3jCFjzLjknAvGG8Y5Y8Q44Zypu6M/vEWQ5ChBUFQKOb7SV/Jm5IQbwzDi886zwMCq3d3nRUnPYN5sn5p9dSiBms0pgN/AYRSlRv/7z7n7j6t9+Ndd6N88J0N1pR+1vUZ4ajf5pmhqoP8udLpKR/rZ3dObg+fq8e1z/vgNsuAF",
        },
        {
            "data": "m=edit&p=7ZRfa9swFMXf/SnGfb4DS7IdW29Z1uwl7f4koxRjipu5q1lSb0ncrTL+7r26NhjGfRp0dDAUH46PbqQfkqzjj7Y8VKgUZmhSDFFRi+KEXkLMZv4Xjm1Tn3aVfYXz9nTXHMggvl8u8bbcHasgH6uKoHOZdXN072wOChA0PQoKdB9t584tbJv9TQ3o1tQPmFLHaqjUZM8me8n93i2GUIXkL0ZP9orstj5sd9X1akg+2NxtEPxkb/jf3sK+eahghPHvAwAFN7ufd2N2bL8039qxShU9ujnTurUAaiZQbwdQ7wRQz/9soFnR97Tenwj12uae+vNk08mubUd6wapYr2wHxtAwiqYZ0M4ZDUwqpZEW00xK40hKE3G2JBZTkSENpTQTx81EMqWUGGtxDKVFOKVnYiwvnIrksSN57EQApO1a8qZp1g3tKTrD+pY1ZI1ZV1xzxnrJumCNWBOumflT8cfn5plwcqP57vm9xf9WWgQ5rNvDbbmt6ItdNPvvzbE+VUD3Yh/AL+AnN/6S/X9V/u2r0q99+NIO/kvDoU8RHuv714/l/Vcogic=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(invert_c(color="gray", invert="green"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="gray"))
        self.add_program_line(all_rect(color="green", square=True))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__2":
                self.add_program_line(f"gray({r}, {c}).")
            if symbol_name == "circle_M__1":
                self.add_program_line(f"not gray({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"gray({r}, {c}).")
            else:
                self.add_program_line(f"not gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
