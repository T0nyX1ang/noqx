"""The Nagareru-Loop solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import directed_route

dict_dir = {"1": Direction.LEFT, "3": Direction.TOP, "5": Direction.RIGHT, "7": Direction.BOTTOM}
rev_dir = {
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
    Direction.TOP: Direction.BOTTOM,
    Direction.BOTTOM: Direction.TOP,
}


def nagare_wind(r: int, c: int, d: str, puzzle: Puzzle) -> str:
    """Generate a constraint for the wind direction."""
    if d in (Direction.LEFT, Direction.RIGHT):
        cols = range(0, c) if d == Direction.LEFT else range(puzzle.col - 1, c, -1)

        c1, c2 = cols[0], cols[-1]
        for c_ in cols:
            if puzzle.symbol.get(Point(r, c_, Direction.CENTER)) or puzzle.surface.get(Point(r, c_)):
                c1 = c_ + cols.step
        if d == Direction.RIGHT:
            c1, c2 = c2, c1
        return f':- white({r}, C), {c1} <= C, C <= {c2}, not line_out({r}, C, "{d}"), not line_in({r}, C, "{rev_dir[d]}").'

    if d in (Direction.TOP, Direction.BOTTOM):
        rows = range(0, r) if d == Direction.TOP else range(puzzle.row - 1, r, -1)

        r1, r2 = rows[0], rows[-1]
        for r_ in rows:
            if puzzle.symbol.get(Point(r_, c, Direction.CENTER)) or puzzle.surface.get(Point(r_, c)):
                r1 = r_ + rows.step
        if d == Direction.BOTTOM:
            r1, r2 = r2, r1
        return f':- white(R, {c}), {r1} <= R, R <= {r2}, not line_out(R, {c}, "{d}"), not line_in(R, {c}, "{rev_dir[d]}").'

    raise ValueError("Invalid direction.")


class NagareSolver(Solver):
    """The Nagareru-Loop solver."""

    name = "Nagareru-Loop"
    category = "route"
    aliases = ["nagareru"]
    examples = [
        {
            "data": "m=edit&p=7Vffb9s4DH7PXzHoWQ/WL8v2W9tb95Jtd2sPRWAEQZZlqLFk7jnJbXPR/30S9aXpVqZbi+Fu2IrE+iSSokhKpOXVP5tpN5c6i39TyEyq8PNlQU/hFD0ZfqfNejGvnsiDzfq87UJHypfHx/LtdLGay0ENsfHgsi+r/kD2z6paaCHpUWIs+7+qy/551Y9kfxJYQtpAG4aeElKH7tNd94z4sXeUiCoL/Rfoh+4odKdd136YHE4Ok+SfVd2fShEXOqTpsSuW7b9zkebReNYuXzeR8Hq6Du6szpsLcFabN+27jbheQyw3i3UzaxdtJ0ifGl/J/oB8gJqtI2rniNk5Yq4dMbwjGo7Mmm62mE+GSdE9/Vg07+dvmo4W+dKHkvfhKmzQq+DFpKqjQ3/vusWue1JdCudFZaXIFYFPo8IlSKMyS1AQqEwBHbBMqExCrYEeCL7JgOAbyBvoMZC3kLN5QlioPOZ5zPPge9jlsU4BfgF6AXqZ1tGZASa6Vmk9rRUQcrBf66RHw05tMd/ahC7ZpT3GsEsjlhp26QJyCK6BHSazQNAVxmo79sCkx+gMqIAaCH0GdLtFzHeYB3tNjnXyZK9BnEwJfgl+CX6Z+DZLfIu4WaWABuiAKW4W9lnE0yKe1kAf7LQO4xx6c8zLMc+D7iGPc2ARZ4tjass0drDPqRxYANM6juJ1FfP0MrSK2lHIiKivVvK68pxRDou4jbWTXxUkSg5GOgaRk45KzC0y5VTtb2mhHGLpJU+PZ5SxhnKLk7e89cp+Zc/WzpiTN93aysczz+mPuXnT3y29UGx4KBcZecpJRr/eEx9tMjbO2vB+6ViLbsbhmu55+dzz8nnB02Nt4OzcEzfKeSYOVAM4uubjRjWCpes9dMfGjWoKs+9UYzh6rC3MuTJFxsbTlHycqdYwdlJtYfRTrWHsoZrCxNnmfD5SbeH0xHcKc26p9nB2lo49Dy7jzw/VpFt6Ql06puqkqT0NL2/ZG2r/oDaj1lE7JJmn1J5Re0StpTYnGR9f/995QWAKpNK0LbkU4VYSLpeLZv1pm++U8J7hFBm25kvOfX2Li4ezFS6uUaWJve90t3bp4vvtn3uUe5T7/eTGg1qcbLq309k8fH4MQ54+edF2y+kijE7OpxeRetQuL9pVs56L8AV4NRAfBT2hZKnwoff4UfizfxTGzcoeXPn/nxdR3Q9lfH3I/qUUF5vJdBK8EjJE8y7O6K45+r6c0V1zwkvvfpzRj+Y8xOpfKga/jwXDeHuULiT5vs2zexPFPEDhg5j/eQUJ17vx4DM=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white", directed=True))
        self.add_program_line(adjacent(_type="line_directed"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line_directed"))
        self.add_program_line(directed_route(color="white"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            shape, style = symbol_name.split("__")

            if d == Direction.CENTER and shape == "arrow_B_B":
                self.add_program_line(f"white({r}, {c}).")
                self.add_program_line(f'line_in({r}, {c}, "{rev_dir[dict_dir[style]]}").')
                self.add_program_line(f'line_out({r}, {c}, "{dict_dir[style]}").')
            if d == Direction.CENTER and shape == "arrow_B_W":
                self.add_program_line(f"not white({r}, {c}).")
                self.add_program_line(nagare_wind(r, c, dict_dir[style], puzzle))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"not white({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            if label == "normal" and not draw:
                self.add_program_line(f':- line_in({r}, {c}, "{d}").')
                self.add_program_line(f':- line_out({r}, {c}, "{d}").')

            if label in ["in", "out"] and draw:
                self.add_program_line(f':-{" not" * draw} line_{label}({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_in", size=3))
        self.add_program_line(display(item="line_out", size=3))

        return self.program
