"""The FiveCells solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.shape import OMINOES, all_shapes, general_shape


class FiveCellsSolver(Solver):
    """The FiveCells solver."""

    name = "FiveCells"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VdNb+M2EL37Vyx45kEkJUvUpUi3Ti+p0yYpFoFgGI5X2xi1odS2ikJG/nvejOSYokykh8Uih8AW/TRfnC8N5d0/9WJbSpXQ12QykgqfcZTxpTLc4zp+7lb7dZl/khf1/rHaAkh5fXkpvy3Wu1KOik5sNjo0Nm8uZPNrXggtJF9KzGTzR35ofsubqWxuwRLSgHYFpITUgJMT/MJ8Qp9booqApx2W4obM3eN2udou1+X8ClRQfs+L5k4KYv7MFgiKTfVvKVpVvl9Wm4cVER4We0S0e1w9dZxd/bX6u+5kYVBs6vV+tazW1ZaIRHuWzUUbxuQYBu3chUERdWEQbMMgdC6M7xLC+qk657w97/wzinMD9+d5QZH8eYLZCd7mBxFHIjdSJJZ/0ox/bMo/So3xC8EpBMcQPFaFiizGigio+StB+wRDBOMQYiJEDiHxJbBjfxe40peAi30JuN6TSNlTx4/U9zT1PU3ZhkOwrOIYtbytI6GUnxClfF+VZruujPEDVFQBj8Kb9yjssGs55ty6/sSc3B6FfXa1Ej/figrfpwyqptoauP6kvJcrQ53T3z3juH5yKRyFU36VcTZcO3awOzVjj6Ijvzg64ric3bXyM6apmXtR6LZePS2/ubTyO0Nrv7209rOhzcDDtl5O7DphOy6lfYBcrUFv68zvZZ35VdbZwGc78LltcDdS6z8UelALbf0HWFu/o7Qd5HlYwfZp6sn4kZqo7zPGkMoPWO95veRV83qHcSYbw+svvEa8JrxescwEI8xkWsbUPFpi7ikZUykJ60jGBg4QNlbGCdwjnGQyTuE84XTcYRj7wiY/8xrzEIUBMgxXYwUDZJgwjlo2TDhJW8MKSmP2LKUx/D8HdTuFv0MSUnqabUazHoUikGWoIQEbobwM4o5lE7QAA5rUDGh2MqCqElARPVmM1FEP6MjVNPQ71NlQRp/QUcOYzjBQt6ky6SuXUk8ojpBGUqJzyauDl9gibl9zQh+8DH1w3zd3NirEbb39tliWePmZfP2r/DSttpvFGnfTevNQbo/3eBt9Hon/BF+FgXL88YL6rl9QqVDRD55+b86MN9wpkGsMUNlcS/FUzxdzBCXwV0gSg8ZfkBPQwRA+z8BQDtjCQD3PwfgOqgSMYdAHVDCiAyohWzTLAyo2lDEM+AAHh0pQJ2ANh1VIxeiAShpg0CF0nvN6Ag3YP7xXccTNRi8=",
        },
        {
            "url": "https://puzz.link/p?fivecells/10/10/a32213a32a1h22c31a3b3a3d3a23a2b2a2a23a1a1b2a22a2d2a3b3a31c11h3a22a21321a",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()

        fail_false((puzzle.row * puzzle.col - len(puzzle.surface)) % 5 == 0, "The grid cannot be divided into 5-ominoes!")
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))

        for i, o_shape in enumerate(OMINOES[5].values()):
            self.add_program_line(general_shape("omino_5", i, o_shape, color="grid", adj_type="edge"))

        self.add_program_line(all_shapes("omino_5", color="grid"))

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
