"""The Tetro Chain-K solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent, count_covering
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, avoid_same_omino_adjacent, general_shape


class TetroChainKSolver(Solver):
    """The Tetro Chain-K solver."""

    name = "Tetro Chain-K"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVtb+JGEP7Or6j2661U7/olxlI/kBy53pUQcoAoWBYyxATn7DhnbHI14r/fzNoIv6xRpfbUVqrMDsMzw7zt+tnd19SNPcoU/KgmhW94NGaKxU1DLKV4Jn4SeNZPtJcm2ygGhdL7Id24wc6jn+bbwU3Ue3vf+31vJosF+6CkH5XZ8+3zu8/hbx99NWa3Q3N0N7rz+VPv15vrB6P/zhilu2ni7R9Cdv08XUw2o9lTl//RHy60bHGv6J8Wm5/3vekvHbsowekcsq6V9Wj2wbIJI5RwWIw4NHuwDtmdlc1pNgYTocyhJEyDxF9HQRSTE5YN8j9yUPtndSbsqN3kIFNAHxY6qHNQ1368DrzleJx7jiw7m1CCya/F31ElYbT3MBsWh7/XUbjyEVi5CYxvt/VfCVXBsEsfoy9p4cqcI816eQvjUwvm5RYgyKkFVPMWUJO0gPWWWhj8/R10neMRducz9LC0bGxnelbNszq2DiCHQjIh59aBcG5AHA7JKjMmXNUA15u4xgBnEvxKjuuIS+LoXTl+hfEl9Vyp8vhmGy6PryqK1F9l2K8E17g0jq7g3GS4vF9dxJfhujSv3jJ/XUV/Cd5Wp4bzac7TYDifZl6D4/ybcQyOcWS4vH7DaIljyOYDh/FWHEku5AROLM1UId8LqQipCzkQPn0hZ0LeCKkJaQifKzzzf/KtgDNBLBOPALF48xX5QbXZas751Uf/72FOxybjNN64aw94a7x1Xz0C1wXZRcFyl+NL75u7ToiV31hlC7GSOC2glzRcecC2Ja8gil4D/0UW4GSqgP7TSxR7UhOC3uNTWyg0SUKtovixVtObGwTVVsRdXoHyw12BkhiovPTbjePorYKEbrKtACXar0TyXmqzTNxqie4Xt5YtPI/j2CHfiFi2Sjnu3/9X+7/5asedUv7CBY8XZHZfMHuuCOSf4VwbtgKYD+t4TZfuErZBzE2Kw0Au+rMW/zquFTiv4XqLv5HjmtGStx6nyNvw15zWfflR0xdvexRfYN6zsQ5LCBjQCxxcssrwFrotWet4g1ux2Ca9AiphWEDrJAtQk2cBbFAtYC1si1HrhItV1TkXUzVoF1OVmdd2Ot8B",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="gray", adj_type=8, grid_size=(puzzle.row, puzzle.col)))

        self.add_program_line(all_shapes("omino_4", color="gray"))
        self.add_program_line(avoid_same_omino_adjacent(4, color="gray", adj_type=4))
        for i, o_shape in enumerate(OMINOES[4].values()):
            self.add_program_line(general_shape("omino_4", i, o_shape, color="gray", _type="grid", adj_type=4))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            target = 2 if d == Direction.TOP_LEFT else 1

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__1":
                self.add_program_line(count_covering(("lt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__2":
                self.add_program_line(count_covering(("gt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__5":
                self.add_program_line(count_covering(target, (r, c), d, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
