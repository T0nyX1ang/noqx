"""The KaitoRamma solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


def straight_line() -> str:
    """Generate a straight line rule."""
    rule = f':- grid(R, C), grid(R + 1, C), edge(R, C, "{Direction.LEFT}"), not edge(R + 1, C, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), grid(R + 1, C), not edge(R, C, "{Direction.LEFT}"), edge(R + 1, C, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), grid(R, C + 1), edge(R, C, "{Direction.TOP}"), not edge(R, C + 1, "{Direction.TOP}").\n'
    rule += f':- grid(R, C), grid(R, C + 1), not edge(R, C, "{Direction.TOP}"), edge(R, C + 1, "{Direction.TOP}").\n'
    return rule


class KaitoRammaSolver(Solver):
    """The KaitoRamma solver."""

    name = "KaitoRamma"
    category = "region"
    aliases = ["kaitoramma"]
    examples = [
        {
            "data": "m=edit&p=7Vbfa9swEH73X1HuWQ86yb/f0jTZS9pua0YpxoQ09dYwB3dJvA0F/+87ndOFsiuDlgYGw9Hly6fT6dNZJ2XzrZ2vK4Xaf2yq6JueEFNuJo256f0zXW7rKj9Rg3Z736wJKHU5HqvP83pTBcXeqwx2LsvdQLl3eQEGFDeEUrkP+c6d57BoVrdLUO6K+kEhdUwIIShDcHSA19zv0bAnURO+2GOCNwQXy/WirmaTnnmfF26qwE92yqM9hFXzvYJ+GP/uBRBxW/+433Ob9q752sJj8E65Aat1I0GoPQi1v4VaWah5S6FZ2XWU748kdZYXXvWnA0wP8CrfdV6Rt8j2Jt+BtRQG1aO0c5YGNiTW/MHGom8q+YZihDAWWTFChNJskRHZTGJjcW1xIs2WhJJvkohsKrGpuIpMjJtFEotaSyFQizFQiwtBFHOMKKYIjTylEZeIVsw+2kgMYmUloZVpOUgobjqUdwdGck5iI9NCYqkuxlwdhu2Uikc5y/aMrWYbsZ2wz4jtNdsh25BtzD6JL78XF+jL5ECM9AKzlA5eEyljKIf2rxIL2x/9T5/o3+PKoIDR3Zfq5KJZr+Y1HZrDZvXQbJbbCuhq6gL4CdwK62+6/7fVsW8rn3t95JJ4bYUWlFcwaLialLtU8NDO5rNFQ/uLktd3G/qzFOpnu18zmir62XGRHPboGaQzpAx+AQ==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black"))
        self.add_program_line(defined(item="white"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(straight_line())
        self.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))

        tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__1":
                self.add_program_line(f"white({r}, {c}).")
                self.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))
                self.add_program_line(f":- {tag}({r}, {c}, R, C), black(R, C).")

            if symbol_name == "circle_M__2":
                self.add_program_line(f"black({r}, {c}).")
                self.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))
                self.add_program_line(f":- {tag}({r}, {c}, R, C), white(R, C).")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
