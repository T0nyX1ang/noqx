"""The Circles and Squares solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import all_rect, avoid_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line("green(R, C) :- grid(R, C), not gray(R, C).")
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))
    solver.add_program_line(all_rect(color="green", square=True))

    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name == "circle_M__2__0":
            solver.add_program_line(f"gray({r}, {c}).")
        elif symbol_name == "circle_M__1__0":
            solver.add_program_line(f"not gray({r}, {c}).")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Circles & Squares",
    "category": "shade",
    "aliases": ["circlesandsquares"],
    "examples": [
        {
            "data": "m=edit&p=7VRdb5swFH3nV0z32ZNs8xHwW5Y1e0mzDzJFFUIVZXRFI2WDsK1G/PdcX5B4wE+TWvVhsu7R4fhgn1wTt7+6rClYiMMNGWcCh+tJKskjKj6NQ3muCvWGrbvzQ90gYezjdsvus6otnGRypU6vI6XXTH9QCQhgILEEpEx/Vr2+VpDXp7sSmI5xHliIE7vRKZFezfRI84ZtRlFw5PuJI71BmpdNXhW3u1H5pBJ9YGA2e0dvGwqn+ncBUxjzPAZA4a768zBpbfet/tFNLpEOTK8prY4tQd05qKFjUMMsQU3+ZwsapcOA/f6CUW9VYlJ/nWk401j1iHtCQXijenBDXEbgNmO0a4oGHkdVLlRp9fo21TfexQq+a1MDu+pZ1ci222plUwU3SyxlIeyy9ecJESxlbN6WWigJD9hhpl3C94Sc0CfckeeK8Ei4IfQIA/KszBn98yk+U5xEBnQXzMN/2efUSSDumvssL/DL39Snn3VbngvA+2Vw4C9QJS5avf9XzktfOab3/LV9sq8tDv6J4Kl8fPuUPX6H1LkA",
        },
        {
            "data": "m=edit&p=7ZRfa9swFMXf/SnGfb4DS7IdW29Z1uwl7f4koxRjipu5q1lSb0ncrTL+7r26NhjGfRp0dDAUH46PbqQfkqzjj7Y8VKgUZmhSDFFRi+KEXkLMZv4Xjm1Tn3aVfYXz9nTXHMggvl8u8bbcHasgH6uKoHOZdXN072wOChA0PQoKdB9t584tbJv9TQ3o1tQPmFLHaqjUZM8me8n93i2GUIXkL0ZP9orstj5sd9X1akg+2NxtEPxkb/jf3sK+eahghPHvAwAFN7ufd2N2bL8039qxShU9ujnTurUAaiZQbwdQ7wRQz/9soFnR97Tenwj12uae+vNk08mubUd6wapYr2wHxtAwiqYZ0M4ZDUwqpZEW00xK40hKE3G2JBZTkSENpTQTx81EMqWUGGtxDKVFOKVnYiwvnIrksSN57EQApO1a8qZp1g3tKTrD+pY1ZI1ZV1xzxnrJumCNWBOumflT8cfn5plwcqP57vm9xf9WWgQ5rNvDbbmt6ItdNPvvzbE+VUD3Yh/AL+AnN/6S/X9V/u2r0q99+NIO/kvDoU8RHuv714/l/Vcogic=",
        },
    ],
}
