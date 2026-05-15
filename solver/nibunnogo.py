"""The Nibun-nogo solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_covering
from noqx.rule.reachable import grid_branch_color_connected


def constrain_branch_size(max_size: int, adj_type: int = 4, color: str = "gray") -> str:
    """Constrain the size of branches."""
    tag = tag_encode("reachable", "grid", "branch", "adj", adj_type, color)
    return f":- grid(R0, C0), {color}(R0, C0), #count {{ R, C: {tag}(R0, C0, R, C) }} > {max_size}."


class NibunNogoSolver(Solver):
    """The Nibun-nogo solver."""

    name = "Nibun-nogo"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VXRbpswFH3PV1R+9gO2gRhepqzr9pLRbclUVQhFhFEVjYiOhGlylH/f9TUJKba0VtqqTZqIb26Oj517jm28/dblbUmZpz9CUviGx2cSG5chNq9/ltWuLuMLOut2900LCaXXCb3L621JJ2nPyiZ7FcVqRtW7OCWMUMKhMZJR9THeq/exSqhaQBehErC5IXFIr4b0Bvt1dmlA5kGemDyE9BbSomqLulzNDfFDnKolJfp/XuNonZJN870kfR36d9Fs1pUG1vkOxGzvq4e+Z9t9ab52PZfpoV29q4qmblqC87HsQNXMSFgcJfBBghgkiJME4ZbALQnsd0uI3BIOsDyfQMQqTrWez0Mqh3QR7w+61j3hgumhHow1iwiIrxF+hvjI8c8RMeYE4dHaIxJyC4nGo6TFkTiPOEemY07ERohg01GFgiPyCnbTERFypFT4/ngePxxVKAKLY5Se5gEjGdp5e7ITOh7t3d5TG/bdbHTXhvGPbRh9dsCRE5ZutnTPjd7bcOSs26yCDaPxNuw7PTFLYMOBm+3yBNbiLa4Ix7iEPU+VwPgGo4cxwDhHzhXGG4yXGH2MIXKm+tQ88VwR4ZFYajNIzM0hO98hf6i2VJg3++Mn+PewbJKSRdfe5UUJL72k26zL9iJp2k1eE7h5DhPyg2BLOeVwe7H/19Fffh3pxfKedSm9wHn5RTkpOA4nSl1T8tCt8hVoQhMRZyNcZC9ePRz4bPIT",
        },
        {"url": "https://pzplus.tck.mn/p.html?nibunnogo/10/10/i16ai3ch22aidj7cjch6bmce53drbg6ddibch2dagcib", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_branch_color_connected(color="gray"))
        self.add_program_line(grid_branch_color_connected(color="not gray"))
        self.add_program_line(constrain_branch_size(max_size=5, color="gray"))
        self.add_program_line(constrain_branch_size(max_size=5, color="not gray"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_covering(num, (r, c), Direction.TOP_LEFT, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
