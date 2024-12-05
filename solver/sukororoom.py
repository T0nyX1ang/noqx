"""The Sukoro Room solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import area, display, fill_num, grid, invert_c, unique_num
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import area_same_color
from noqx.solution import solver


def num_count_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """Generate a constraint for counting the number of adjacent black cells."""
    return f":- number(R, C, N), N != #count {{ R1, C1 : adj_{adj_type}(R, C, R1, C1), {color}(R1, C1) }}."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(fill_num(_range=range(0, 5), color="white"))
    solver.add_program_line(invert_c(color="white", invert="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(num_count_adjacent(color="black"))
    solver.add_program_line(unique_num(color="black", _type="area"))
    solver.add_program_line(area_same_color(color="black"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, (ar, _) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert d == Direction.CENTER, "The symbol should be placed in the center."
        if symbol_name == "ox_E__1":
            solver.add_program_line(f"not white({r}, {c}).")
        if symbol_name in ("ox_E__4", "ox_E__7"):
            solver.add_program_line(f"white({r}, {c}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Sukoro Room",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7ZRPb9pAEMXvfIpoz3vYP6Zg30gKvaSkDVQRWlnIJG5BAZkCrqJFfPe8Ga8xVROljZScqsWjn59nx29nF29/ltkml20M25VKagxjunxFin71GC92yzw5k71yNy82ACmvBgP5PVtu85YLWWlr7+PE96T/lDihhRQGlxap9F+Tvf+c+L70IzwSUkO7rJIMsN/gDT8nuqhErcDDwMAJsHiYnld3XxLnx1LQO855JqFYFb9yETzQ/W2xmi1ImGU7LGQ7X6zDk215V9yXIVenB+l7ldXhE1ZtY5Wwskr0hFVaQbDafwOrcXo4oN3XMDtNHPn+1mC3wVGyRxwme2EMTbXwUu2JiBQJ2KJaaHd/y8A8zbMnHAccDccxiktvOX7kqDi2OV5yTh/v1AqHSmmRGFRUOF4KJpgN2DLH0RG1iqXWsEWsMVXHgaGbWkeZU9Z1Sduw6SAHq2HugkMdg5pHhm47J3qwaVDThvoWuq3z6b11fdg3wbOFTq2s2YYcTTmhJrEO+Zp8RsEz1l7rxKrdtEfTXPTxhrt5wTHi+IG73KEN/qcjcLqhglrosNHH8ymoMS5qlNft+YuOHTU7jPbfUdpyon/3Iz8bFptVtsT/YViuZvmmuR/Ns3Uu8AE6tMSD4MuhzzL6/016528StV69+li+0Zl7wY7zE4lT6a+kWJfTbHpb4Eyhb6zHz+jP5f+pv/tq8SfDztwXG4xiJdLWIw==",
        },
    ],
}
