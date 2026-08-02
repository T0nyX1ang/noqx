"""The Tetro Chain-Y solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction
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
            "data": "m=edit&p=7VVRa9swEH73ryj3fA+WJbuxX0bWNXvJ3K3JKMUE43guNbNx58RjKOS/9+5siNeksD6sozAUfbl8Op303aHL5keXtQUqlz96gvRNw6iJTG8SyHSHsSy3VRGd4bTb3jctGYhXsxneZdWmQCcZ3FbOzoaRnaL9GCWgAMGjqWCF9ku0s58iG6Nd0BKgIW7eO3lkXh7MG1ln66InlUt2TDYFUwjXHO6WfuZlm1dFOieWmM9RYpcIvPheIrAJdfOzgOEu/Dtv6nXJxDrbkqLNffkwrGy6b833bvClgFB31bbMm6ppmWRuj3bay1ickKEPMtjsZbB1Qgar+8sSwtMS9lSiaxKRRgnr+XowJwdzEe0I42gHWvPOd6mW1Ht8igmY8lKWNFC+kkPTvkBCBW7vNab8o43n5pgKj2KFEt6MLxFKLH+8UblypBnvVK4cYFJ3xOkTfvppPNKvJAu3gjNBT3BJSUKrBT8IuoK+4Fx8LgVvBC8EjWAgPuec5j8sBPB1PQRNSTB9VV7hbonu+8Hvw3973MpJYNG1d1le0CuJu3pdtGdx09ZZBdSu9g78ApmJ5vb3v4O9gQ7G5XJf1Mf+/WtOKOP0puwVwkOXZilpAvrDROaN/zJeq2f8gyc8FekZ/tWzQy1l5TwC",
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

            if isinstance(clue, int) and label.startswith("arrow"):
                arrow_direction = label.split("_")[1]
                self.add_program_line(yaji_count(clue, (r, c), arrow_direction, color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
