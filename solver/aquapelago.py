"""The Aquapelago solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import count_reachable_src, grid_color_connected, grid_src_color_connected
from noqx.rule.shape import avoid_rect


class AquapelagoSolver(Solver):
    """The Aquapelago solver."""

    name = "Aquapelago"
    category = "shade"
    aliases = ["aquapelago"]
    examples = [
        {
            "data": "m=edit&p=7VZNj9owEL3zK1Zz9iH+SAi5VHS79ELZtlCtKitCgWa1qEGhgVSVUf57Z8YRIS1V91BxqFaOZyZvxs6bsWVn/63OqlzIiB4di0BIbJGJuIfxiHvQtsXmUOTJjRjXh6eyQkOI+8lEPGbFPh/YNiodHN0ocWPh3iYWJAhQ2CWkwn1Iju5d4mbCzdEFwiA29UEKzbvOfGA/WbcelAHaM2/TsM9orjfVusiXU/Qi8j6xbiGAvvOaR5MJ2/J7Di0Pel+X29WGgFV2wGT2T5td69nXX8qvdRsr00a4sac7v0BXd3T1ia6+TFf9E7rFrrxEdJQ2DRb8I1JdJpZYf+rMuDPnyRGMgsQIMENWYcgqNl5FrEaSlZQ+Rg59kBxp1irwYUr5USr2U+og9lr6OG28X4etP6T5GiqJp4HcaSH9vmBGfmVbgLj1AGJp4dUZEBFgOoCYWxh2AOfQm4SzsbQdTwjlhTFnEKfYp8fZ9sZx3hZ0h3AF+ojUv3yfq9Kbh+tjITxHhr15sGYyOTa0g0hOWCqWC1xZ4TTLNywDliHLKcfcsXxgecvSsIw4Zkh749m7B9NRAiJ9WskrcLNG8Yn05xa++P9nfzqwMK+rx2yd4/E3q7ervLqZldU2KwBvmmYAP4C71RhuXi6fq18+VPzgmYfI1c6Nv9CxWNdIC3cvYFcvs+W6LAD/XATh5nf86uzx4EsHPwE=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))
        self.add_program_line(avoid_rect(2, 2, color="not black"))
        self.add_program_line(grid_color_connected(color="not black", adj_type=4, grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color="black", adj_type="x"))
                self.add_program_line(count_reachable_src(num, (r, c), color="black", adj_type="x"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
