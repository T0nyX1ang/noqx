"""The Sukoro Room solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, display, fill_num, grid, invert_c, unique_num
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_same_color
from noqx.rule.reachable import grid_color_connected


def num_count_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """Generate a constraint for counting the number of adjacent black cells."""
    return f":- number(R, C, N), N != #count {{ R1, C1 : adj_{adj_type}(R, C, R1, C1), {color}(R1, C1) }}."


class SukoroRoomSolver(Solver):
    """The Sukoro Room solver."""

    name = "Sukoro Room"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7ZRPb9pAEMXvfIpoz3vYP6Zg30gKvaSkDVQRWlnIJG5BAZkCrqJFfPe8Ga8xVROljZScqsWjn59nx29nF29/ltkml20M25VKagxjunxFin71GC92yzw5k71yNy82ACmvBgP5PVtu85YLWWlr7+PE96T/lDihhRQGlxap9F+Tvf+c+L70IzwSUkO7rJIMsN/gDT8nuqhErcDDwMAJsHiYnld3XxLnx1LQO855JqFYFb9yETzQ/W2xmi1ImGU7LGQ7X6zDk215V9yXIVenB+l7ldXhE1ZtY5Wwskr0hFVaQbDafwOrcXo4oN3XMDtNHPn+1mC3wVGyRxwme2EMTbXwUu2JiBQJ2KJaaHd/y8A8zbMnHAccDccxiktvOX7kqDi2OV5yTh/v1AqHSmmRGFRUOF4KJpgN2DLH0RG1iqXWsEWsMVXHgaGbWkeZU9Z1Sduw6SAHq2HugkMdg5pHhm47J3qwaVDThvoWuq3z6b11fdg3wbOFTq2s2YYcTTmhJrEO+Zp8RsEz1l7rxKrdtEfTXPTxhrt5wTHi+IG73KEN/qcjcLqhglrosNHH8ymoMS5qlNft+YuOHTU7jPbfUdpyon/3Iz8bFptVtsT/YViuZvmmuR/Ns3Uu8AE6tMSD4MuhzzL6/016528StV69+li+0Zl7wY7zE4lT6a+kWJfTbHpb4Eyhb6zHz+jP5f+pv/tq8SfDztwXG4xiJdLWIw==",
        },
        {"url": "https://puzz.link/p?sukororoom/10/10/nrnfdbp5timpmpdnns4svecvuufnvsbvtst7g1zzzn", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_num(_range=range(0, 5), color="white"))
        self.add_program_line(invert_c(color="white", invert="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(num_count_adjacent(color="black"))
        self.add_program_line(unique_num(color="black", _type="area"))
        self.add_program_line(area_same_color(color="black"))

        areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, (ar, _) in enumerate(areas.items()):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "ox_E__1":
                self.add_program_line(f"not white({r}, {c}).")
            if symbol_name in ("ox_E__4", "ox_E__7"):
                self.add_program_line(f"white({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
