"""The Tetro Chain-Y solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, avoid_same_omino_adjacent, general_shape
from noqx.rule.variety import yaji_count


class TetroChainYSolver(Solver):
    """The Tetro Chain-Y solver."""

    name = "Tetro Chain-Y"
    category = "shade"
    aliases = ["tetrochainy"]
    examples = [
        {
            "data": "m=edit&p=7VVNb9pAEL37V0RznsN+mYBvNA29UPIBURRZlmVcR0E1cmpwFC3yf8/sLIqdwqE5NFGlar3Pj7ezw9tZdtn8arK6QCnco4dIb2pGDrmr4YC72LfFalsW0QmOm+1DVRNBvJhM8D4rN0UQ76OSYGdHkR2j/RbFoAC5S0jQXkU7+z2yM7RzGgI0pE2JSUBF9Lyjtzzu2JkXpSA+8wkl0Tui+arOyyKdeuUyiu0CwX3PF57tKKyrpwJ8Cv6cV+vlygnLbEuL2TysHvcjm+ZH9bPZx8qkRTv2dudH7OrOrn61q4/bVX/f7ihpWyr7NRlOo9h5v+nosKPzaNc6XzswAzdVpc6r2yHKGErOlqpOGggf1ZfCg4mn5lAaHeQacXqT6p7EucL+RCmED1N9zXhN9DR9JE7/no8WK3nJd4wTRsW4oIqg1YxfGQVjyDjlmHPGW8YzRsM44JhTV9M/rDo4uwpBUxGM34IP8BZrf57ftvDf05IghnlT32d5QT//WbNeFvXJrKrXWQl037QBPAP3WLvr6/8V9ElXkNsC8a6L6PNPaEzVpXNiLxAemzRL86oE+hdDp5vwfbqWB/qHr5aOfRK8AA==",
        },
        {"url": "https://puzz.link/p?tetrochain/9/9/c33d37k32d35k31d32k22d41t34", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="black", adj_type=8, grid_size=(puzzle.row, puzzle.col)))

        self.add_program_line(all_shapes("omino_4", color="black"))
        self.add_program_line(avoid_same_omino_adjacent(4, color="black", adj_type=4))
        for i, o_shape in enumerate(OMINOES[4].values()):
            self.add_program_line(general_shape("omino_4", i, o_shape, color="black", _type="grid", adj_type=4))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            self.add_program_line(f"not black({r}, {c}).")
            fail_false(isinstance(clue, int) and label.startswith("arrow"), "Please set all NUMBER to arrow sub.")
            arrow_direction = label.split("_")[1]
            self.add_program_line(yaji_count(int(clue), (r, c), arrow_direction, color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
