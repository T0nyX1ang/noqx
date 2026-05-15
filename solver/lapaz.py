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
            "data": "m=edit&p=7ZVvb6JOEMef+yqafdpNjgVUJLlcrNVe+7PWVo1XiTFoUWnB7SHYHsb33tlBzwVp7y6X3/1JLso4fGb/zMzKl+XnyA4cyhTx1QwKv/DRmYGXapTwUrafrht6jnlEq1E45wE4lF41GnRqe0uHXtzOmzVefTqtfloZ4WDAzpToXOnfN+6Pb/z/zl0tYI2W0b5sX7rqrPqxdnJdqh+X2tGyFzqra5+d3PcG3Wm7P6uoX+qtgR4PrpTixWD6blXtvS9Y2xyGhXVcMeMqjc9Mi6iE4sXIkMbX5jq+NOMOjTsQIlQfUuJHXuhOuMcDgozBuCZ4jFAV3Pre7WNceLUEMgX81tYH9xbciRtMPGfUTEjbtOIuJWLvE5wtXOLzlSM2g2l4P+H+2BVgbIfQvuXcfSRUg8AyuuMP0XYoG25oXE0qqO8qgGzeqgAW2VUg3KQC4eVUIAr7fyuoDDcbOJwbqGFkWqKc3t419m7HXINtmWuisV3xyQkSTRXggwQqAsAJ70AJpygSwCm6BLQs0AXQ9qCMQNqljLtIeRhGZkoFF5UAU3DfFClnCStlsmcqpi+TpAfyrKQJUgFMy5bENCxBypiViqmVocMM+3yLtoFWRduFY6CxhvYUrYK2iLaJY+po+2hraHW0JRxTFgf5nUdNdEhVpaQILdWTc//53IiuQpMqBjz8TKWqCn3WvpmvpSXilv4U/z42LFikEwVTe+LAA1q/mzlHLR74tgd3rcgfO8HuHsSSLLk3WiajR86zPQmJmei1HEmxBa6RQh7nj567yFthF0pBd7bggZMbEtCBnF9ZSoRylhrz4C6T05Pteela8F2WQonapVAYgJRJ93YQ8KcU8e1wngKS7KVWchaZZoZ2OkX7wc7s5u/bsSmQZ4KXpVH135vtD3+ziYNSfuj99vs12IK/jMZofEXJYzSyR9Bs7Fcuh7IFLxr543U9b3ydghRnAnA2IvBVmw/Cv7xL+Ojx4A0d3AezOEcNgb4hiFI0j7+ifVI0yw+ETiR7qHVAc+QOaFbxAB2KHsAD3QP2ivSJVbPqJ7LKCqDY6kADxVayDFrDwgs=",
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
