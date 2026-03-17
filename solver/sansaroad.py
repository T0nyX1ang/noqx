"""The Sansa Road solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false
from noqx.rule.neighbor import adjacent, count_adjacent, count_covering
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route
from noqx.rule.shape import avoid_rect


class SansaRoadSolver(Solver):
    """The Sansa Road solver."""

    name = "Sansa Road"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVLb9swDL7nVww662C9/LplXbdL2m5zhiIwDMN1XcSYM2dOvA0K8t9H0d4CNDRQDHsdCkUE84n+zI+yxN3nvugqLqT7qZB7XMDQkcapAoPTG8ey3jdV/ILP+/267cDh/OaaPxTNruKzdIzKZgcbxXbO7Zs4ZYJxJmEKlnH7Lj7Yq9iuuE1gifEw42zTN/u6bJu2Y4gJiFsMD0pwL0/uLa4772IAhQf+9eiDuwJ339X37ddP+dUQ+TZO7ZIz9/KX+Lhz2ab9UrExOfe/bDd3tQPuij0o3K3rLeMKFnb9ffuxZz9eceR2PkhInihBnSSonxIULUGOEsq6K5sqXwxEv1NBlB2PsDvvQUMep07Oh5MbntwkPhxdWs4KtKv4wIwCGsEflZgZn4R9b4BHNUkywCFNErloeRYtpCHDhRI0HkgSl94ELmh+GdHZK4/OUwk9gfs0j1Y0bsIJPKL5gwmeYCKfwJ/AA5ondLgh8JDGI0HzR5Lmj+j6aNyvc34taX4tab1a0Xq1ofdR+zRuNK3X4JkgcF+TeOBFNC7o+FDQ7w3J7xPO6Ws8rRLtEg4ztwrtK7QeWoN2gTGXaG/RXqDVaH2MCdx18MQLA75pFkPlDOxQeH57/KHcUqWxY50P84y7kc1SlvTdQ1FW0CqSdbGtGHTo44x9YzhTxaULe27a/3PTdjvl/XLr/jcXQwoFh+Npbzjb9nmRQ7GxXg434hGusr+ePdwe2ew7",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_rect(2, 2, color="not gray"))
        self.add_program_line(fill_line(color="not gray"))
        self.add_program_line(single_route(color="not gray"))
        self.add_program_line(grid_color_connected(color="not gray", adj_type="line"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(
                not (d == Direction.CENTER and symbol_name == "circle_SS__5"),
                f"Gray circle cannot be placed in the center of ({r}, {c}).",
            )
            target = 2 if d == Direction.TOP_LEFT else 1

            if d == Direction.CENTER and symbol_name == "circle_SS__1":
                self.add_program_line(f"not gray({r}, {c}).")

            if d == Direction.CENTER and symbol_name == "circle_SS__2":
                self.add_program_line(f"gray({r}, {c}).")

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__1":
                self.add_program_line(count_covering(("lt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__2":
                self.add_program_line(count_covering(("gt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__5":
                self.add_program_line(count_covering(target, (r, c), d, color="gray"))

            if d == Direction.CENTER and symbol_name == "tridown_M__1":
                self.add_program_line(f"pass_by_route({r}, {c}).")
                self.add_program_line(count_adjacent(3, (r, c), color="not gray", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
