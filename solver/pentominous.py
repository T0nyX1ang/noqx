"""The Pentominous solver."""

from typing import Dict

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, avoid_same_omino_adjacent, general_shape


class PentominousSolver(Solver):
    """The Pentominous solver."""

    name = "Pentominous"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VTfb9owEH7nr6j8fA/+kQQnb6yDaRKj3aBjXYRQoOmKBkoXyDQZ5X/v+Zw0mUS0TtU6TZqCz5+/s/Hns+/234okT0Fw+1MasMfPE5qa1AE1Xn2zzWGbRmcwKA53WY4A4GI0gttku097cTVr0TuaMDIDMG+imEkG1ARbgHkfHc27yEzBTNHFwENujEgwkAiHDZyT36JzRwqOeFJhhNcI15t8vU2XY8dcRrGZAbP7vKLVFrJd9j1lbhmN19lutbHEKjngYfZ3m/vKsy9usq8Fq7cowQyc3OEJuaqRqx7lqtNy5Z+XGy7KEsP+AQUvo9hqv2qgbuA0OrJ+wCIPmNauC6kLOXWCe9iXVvqRKWn/fYJy3fUxpSwxbxGBJS5bRN8SHxtC04xRQ4S+Jd42hODcMtdtJrTMrMX42jJXbYbmfG4xAckdtxnS+6lm8FgiOpb2MqwdkZVkZxgeMIrsa7KcrE92THOGZOdkz8l6ZAOa07cBfuIVuPg+Xw4L+hiFUAMLNK+BqIF0QGqBOYwDhVh4IKWuMOa3qviQgwwFYeV5oHxdYSwKPj4J9cuTx8qVjp8//9/jFr2YTYv8NlmnmGnDmy/p2STLd8kWR5Nit0rzeoyFruyxH4xarGzd/F/7/lLts1fAXzj9nlsNYozuY3qCuQB2XyyT5TrDp4YhdO4qYzvdLom73FVed7jrVO90u+w/7Q763m86vKBrhZZdDtHl4F2bh0/f/MXfA5bJRe8B",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        shaded = len(puzzle.surface)
        fail_false((puzzle.row * puzzle.col - shaded) % 5 == 0, "The grid cannot be divided into 5-ominoes!")
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_shapes("omino_5", color="grid"))
        self.add_program_line(avoid_same_omino_adjacent(5, color="grid", adj_type="edge"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

            for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
                d = Direction.LEFT if c1 != c else Direction.TOP
                self.add_program_line(f'{prefix}edge({r2}, {c2}, "{d}").')

        shape_dict: Dict[str, int] = {}
        for i, (o_name, o_shape) in enumerate(OMINOES[5].items()):
            shape_dict[o_name] = i
            self.add_program_line(general_shape("omino_5", i, o_shape, color="grid", adj_type="edge"))

        for (r, c, d, label), shape_name in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(shape_name in shape_dict, f"Shape {shape_name} is not defined!")
            t_be = tag_encode("belong_to_shape", "omino_5", "grid")
            self.add_program_line(f":- not {t_be}({r}, {c}, {shape_dict[str(shape_name)]}, _).")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
