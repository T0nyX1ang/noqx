"""The FourCells solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.shape import OMINOES, all_shapes, general_shape


class FourCellsSolver(Solver):
    """The FourCells solver."""

    name = "FourCells"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VbfT9swEH7vX4H8fA/xjzg/XibGyl5Y2SgTQlFVlRJGtVRhaTNNqfjfubsYFewihuBhmlAb+8tnn+8+2zl79audNSVIS3+dQgQSf9ZYfuI04ydyv9PFuirzPdhv19d1gwDg+PAQrmbVqoRB4bpNBpsuy7t96D7nhVAC+JFiAt23fNN9ybsRdGNsEqCRO0IkBSiEwy0843ZCBz0pI8Qjh0Gc0HDn+DpfNPOqnB4hi8zXvOhOQVDjRx6BoFjWv0vRm/L7vF5eLIi4mK1R0ep6ceNaVu1l/bN1fXFAsWyr9WJeV3VDJHG30O33Mob3Msizk0GKnAyCvQxCO2SQutdLqG7qXcFnu4O/xcU5wfCneUFKvm9huoXjfCNUpESuce2Uq42rravTvtaun3b9NPfDQUY4iMnup7LfACI2HmEDIvYIGSU+I9GFxwRWSvuMsT4TRwETjJMEvpIgnjTwlQbjpGnA8OR8eMBkHM8jxh9HRb6Vkr6VCuZHKT9mpX3tyvgqVLBaKpgNlfizqgLtqtf1gNGR70tH/vzoQIUOVlDHMmAee8eNKPMNludcHnKpuDzFzQ6d5vITlxGXMZdH3GeImzhOJWZBDEbh/k0VWNrxiLEGS7uesEJMO5+wQUxfCWGL2NliDYmzxRoSZ4s1JGyLDs/Y7QGXBp3bCNMxGaEcqxCTEWFDadphi5gcEsZg2SHiBG3ZIWG0ZYcSB7asMKGP/S/TQf89v8FkSs4jWQrCGAOGPn9KFp5sL8YCZ5TOpad/8Xv7/9w+GRRi3DZXs3mJZ93w8ke5N6qb5azCt1G7vCib+3e8fNwOxB/BT6HR2LzfR/7p+wgtVPSiNORfGl6flp7NQM+EV3RjMBl0xyBu2ulsihoFXoThaf78hfyI+H6V3Em3q8MOw+E20+5ulsrql7dgRvZb3vioeH5N8GCYDO4A",
        },
        {"url": "https://puzz.link/p?fourcells/10/10/d3g1c3g1c3b1a3b1j3a13a3j1b1a3b1c3g1c3g1d", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()

        fail_false((puzzle.row * puzzle.col - len(puzzle.surface)) % 4 == 0, "The grid cannot be divided into 4-ominoes!")
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))

        for i, o_shape in enumerate(OMINOES[4].values()):
            self.add_program_line(general_shape("omino_4", i, o_shape, color="grid", adj_type="edge"))

        self.add_program_line(all_shapes("omino_4", color="grid"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

            for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
                d = Direction.LEFT if c1 != c else Direction.TOP
                self.add_program_line(f'{prefix}edge({r2}, {c2}, "{d}").')

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent_edges(num, (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
