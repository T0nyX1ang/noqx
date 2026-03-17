"""The La Paz solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, edge, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.shape import OMINOES, all_shapes, general_shape


def edge_surrounding_color(color: str = "black") -> str:
    """Generates a rule to ensure that the black cells are surrounded by edges."""
    rule = f':- grid(R, C), {color}(R, C), not edge(R, C, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), {color}(R, C), not edge(R, C, "{Direction.TOP}").\n'
    rule += f':- grid(R, C), {color}(R, C), not edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), {color}(R, C), not edge(R + 1, C, "{Direction.TOP}").\n'
    return rule.strip()


def lapaz_constraint(color: str = "black") -> str:
    """Generate a constraint for La Paz."""
    rule = ":- number(R, C, N), number(R1, C1, N1), adj_edge(R, C, R1, C1), N != N1.\n"
    rule += f':- grid(R, C), number(R, C, N), edge(R, C, "{Direction.LEFT}"), edge(R, C + 1, "{Direction.LEFT}"), N != #count {{ R0 : {color}(R0, C) }}.\n'
    rule += f':- grid(R, C), number(R, C, N), edge(R, C, "{Direction.TOP}"), edge(R + 1, C, "{Direction.TOP}"), N != #count {{ C0 : {color}(R, C0) }}.\n'
    return rule


class LaPazSolver(Solver):
    """The La Paz solver."""

    name = "La Paz"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VTdb9pADH/nr6j87IfcB5DkZWId7IXRbTBVVRShQNMVLVG6QKbpEP/7fD5o6BWtnaZ9SdNxxvezzflnc15/brI6RxHYjwqRvmlpEfKWYY93sF+z1abI4zMcNJvbqiYF8WI0wpusWOfYSfZuaWdrotgM0LyOE5CAvAWkaN7FW/MmNlM0UzIB6hShbIrNalkVVQ2MCfIbkyYAJanDVr1ku9XOHSgC0id7ndQrUperelnk87FD3saJmSHYu19ytFWhrL7k4ML4vKzKxcoCi2xDDNe3qztARYZ1c119auBwww7NwDEYHhjI7zNQLQN1z0CdZiB/OYMo3e2oOe+JwzxOLJ0PrRq26jTe7mxaW1DiQN51EJS0wIsjIALX5QPQ45DgCOAQfQQoH9AWUC3Q194t/cjLIwy9kEh5gAjkI6TvI6LnZS+k8BFXg+Mo5TMSyqcklPYyFr3ug1+mCguu8xXLEUvJckZtQKNYvmIZsOyyHLPPkOUly3OWmmWPffq2kc9sNWhKVSJ0qaTa9f3ncwMtqUhRSI9fSJSS6qyezDdRbv48XN1/D0s7CUyb+iZb5vRAh9cf87NJVZdZQadJUy7y+nCmYbnrwFfgnSiU/+fnXz4/baOCH5qif/6lJ/SXUQLNBcJdM8/mVGyu10lcObwbnvbX+pT/EOnBe4bAGe4nwCPzb68SjZi08w0=",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))
        self.add_program_line(edge_surrounding_color(color="black"))
        self.add_program_line(lapaz_constraint(color="black"))

        for i, o_shape in enumerate(OMINOES[2].values()):
            self.add_program_line(general_shape("omino_2", i, o_shape, color="not black", adj_type="edge"))

        self.add_program_line(all_shapes("omino_2", color="not black"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(f"not black({r}, {c}).")
                self.add_program_line(f"number({r}, {c}, {num}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="black", size=2))
        self.add_program_line(display(item="edge", size=3))

        return self.program
