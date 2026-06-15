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
            "data": "m=edit&p=7VVRb9owEH7Pr6ju+R7s2KHgN9qVvbB0G0xVFaEoZKkaLShdINNkxH/v3SUS2eBhfVi3SZPxx8fn89mfLR/br23WFKgVf8wY6Zua1WPp4XgkXfVtWe6qwl3gtN091g0RxNvZDB+yaltgkPRhq2DvJ85P0b91CWhACKlrWKH/4Pb+nfMx+gUNAVrS5l1QSPTmSO9knNl1J2pFPCZOyTTRe6J52eRVkc475b1L/BKB17mS2UxhU38roN8H/87rzbpkYZ3tyM32sXzqR7bt5/pL28dSQti01a7M66puWGTtgH7aWVicsWCOFph2FpidscDOfrOFyXkLB7qej2QidQn7+XSk4yNduD1h7PZgRzwzTHn/fJOUNNKyQso30Usj1UUNpehk4qU9lSYnuSaS3qZmIEmuaDhRK1nSDmdqJQvYVA00cybO/JyPzGqxfC84EwwFl3Qi6I3gG0ElGAnOJeZG8E7wWtAKjiTmks/0F08deLshgqFDsN0VvMLeEtM9/B9b9O9pqyCBRds8ZHlBTyJuN+uiuYjrZpNVQHXpEMB3kJ4YrnP/S9VfXqr4qtSLCtaff8kJnTi9J3+L8NSmWUqegP4VkXUbvUw3+kR/dbdUHlbBMw==",
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
