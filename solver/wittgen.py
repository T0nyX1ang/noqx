"""The Wittgenstein Briquet solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, edge, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, general_shape


def edge_around_shade(color: str = "gray") -> str:
    """Generate constraints to ensure shaded cells are surrounded by edges."""
    rule = f':- {color}(R, C), not edge(R, C, "{Direction.TOP}").\n'
    rule += f':- {color}(R, C), not edge(R, C, "{Direction.LEFT}").\n'
    rule += f':- {color}(R, C), not edge(R + 1, C, "{Direction.TOP}").\n'
    rule += f':- {color}(R, C), not edge(R, C + 1, "{Direction.LEFT}").'
    return rule


class WittgensteinBriquetSolver(Solver):
    """The Wittgenstein Briquet solver."""

    name = "Wittgenstein Briquet"
    category = "var"
    aliases = ["wittgensteinbriquet"]
    examples = [
        {
            "data": "m=edit&p=7VRLb9pAEL7zK6I9z2EfNl77UqWp6YWSphBFyLKQIU6DamRqcFUt4r93dgxxs1gqUau2h2jZ0fibx87sLN/ma51VOQhpf0oDB4HLCz3aKvBp88OaLLdFHl3AZb19LCtUAK4HA3jIik0OveTglvZ2JozMDZj3UcIEAyZxC5aCuYl25kNkRmDGaGKgU2CrutguF2VRVowwgX7DJlCiGrfqHdmtdtWAgqM+OuioTlFdLKtFkc+GDfIxSswEmD37LUVbla3Kbzk71Ga/F+VqvrTAPNtih5vH5ZqBQsOmvi+/1Ox4wh7MZdNBfGYHqu1APXWgujuQf6SDYl121B6m+z2O5RNWP4sS28htq+pWHUe7vS1ox5RnQzkW0cyOqdACsgU8/3gxB8APHKCvLaBaIHBDtHKAUDqnCC6dJIL7LiI8J42QyilfKOn6eMJFfO5m9pWL9JVbYXCSWXPXR7t3I0Lt+EjBnZql6DtRUtAU3vyESPEsCscnaIhTkgOSkuQEZwxGkXxHkpP0SQ7JJyZ5R/KKpEeyTz6BfSVnviOmcEwaXwV2pZtH9fu1MW2HH2JaGWiQIc5d/bLeRHlEa6fLf8XtSnsJG9fVQ7bIkU/i+8/5xaisVlmBX6N6Nc+r4zdy+77HvjPaiQJpg1/p/r+kezsi/iLS//fckZgx4L/VXANb17NshtdM99KJS4tPz8dVk8cXXf4d+NGfd/nHloI8pCBk3udmfoYZu/G7TosBCa47n+b9FxqeOPLE/NenjiSc9n4A",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(general_shape("omino_3", 0, OMINOES[3]["I"], color="not gray", _type="grid", adj_type="edge"))
        self.add_program_line(all_shapes("omino_3", color="not gray", _type="grid"))
        self.add_program_line(edge_around_shade(color="gray"))
        self.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"gray({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="not gray", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"gray({r}, {c}).")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="gray", size=2))
        self.add_program_line(display(item="edge", size=3))

        return self.program
