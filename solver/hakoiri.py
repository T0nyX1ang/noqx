"""The Hakoiri-masashi solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, count, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected


class HakoiriSolver(Solver):
    """The Hakoiri-masashi solver."""

    name = "Hakoiri-masashi"
    category = "var"
    aliases = ["hakoirimasashi"]
    examples = [
        {
            "data": "m=edit&p=7VfvT+M4EP3OX7Hy1410sZ0fTqX7UNiyt3tQYAFxtEJVKAHKpoRNU+CC+N/3jTOhSVt2pT3t6e50ams/P9vjNxN74s6+zOM8caRLX20c1Ph40tifMoH9ufw5mhRp0nnjdOfFdZYDOM7e9rZzGaezxPl4er2zlXUf3nX/uDfFYCDfu/MP7snN9s3bT9PfP0x0Lrf7Zn93f3eirrq/bW0eBL23wf58dlwk9wdTuXlzPDi63D+5itSfvf7AKwd7rv9xcPnLfff4140hazjbeCqjTtl1yvedoZDCEQo/Kc6c8qDzVO52yp5THqJLOAbcTjVIAfYW8MT2E9qqSOkC9xkDngJmj6PNqrXfGZZHjqA1Nu1MgmKa3SeCNVB7nE3PJ0ScxwXCNLue3HHPbH6RfZ7zWBgU03laTMZZmuVEEvfslN1K/uka+Xohn2Aln9Aa+eQVy+/9BPnRevnPeCyf4MCoMyRfjhfQLOBh5wll35bSlqedJ6FdWJHOIt7CV2B0kwl8MKrJSGWWp0ntrVDLE7Hmtl1Z2fIIwpxS2/KdLV1b+rbcsWN60Kh05CgPQmFKKRyKJlZhhaVeYB/YhxyLPWDosNgHDirsqQVWOGwe3LY4hB14V/MqYgwNFCzC2gWWjCUwz9WwqTVjaKCQWAwNutYAzX6tE2uFbIfsezzXw1yP53qkn/X40BPyWiHWrTGN8di+Bx+92keKFa9FemrsYV2PbXqwGbCdAPpDnhtibsT+RshObqUHNXDtC+b6HB8f+gMeHyA+IesPoS3k8SG01fZpfMj+htBmWJuBNsPaDCVBtm8wvtYTQqdhO0iQ2q141I6WrFNCp6zW1a58wWQf7Rf72q18Rw1c6UGN8ZUe1MCVHtTAlR7L8x7Q2A8vGM8RbcYYz/tHY1+hzRiaea9qiXVV5YvFkmMSwU4Ts492DwcckwAxMTzGIIZRHUOKJ8ffIP6m9h1z67hFiHPEcY7IL94DhmJb28QeM8xHmBvVc6Ffso/05lIcc4WYK465RMwZ01po8xgf8eGY4Fxrn2NOMeFzjRp8bRPa+GyiBs+xopjzGUENnmOL/a95T1rMZ0HjbLawPadIMCc2zWzZ0rNlYNNPSFnzL+RVuMupr3oRCBLLebVmKD2aBfNj6fG7PgwRKrpXtD/+v4872xiK3sVV8qaf5dM4xQvy8Dq+SwRuJWKWpaPZPL+Mx8koeYzHhehUF6NmT4u7nU/PE7xDG1SaZXfp5HadhbqrRU6ubrM8WdtFZAKtr5iirjWmzrP8YknTQ5ymbV/spbFFjSf5OG1TRY7rRKMd53n20GKmcXHdIhpXj5al5HYpmEXclhh/jpdWmy7C8bwhHoX9YfPjcvv/FfIfeoWkR+T+cML7SbnrO3KGiDYuYOWeI+7mo3gEnwT+pTjE46Wwnvf/c/zf/lTsIc/yb2TcRecyvSbvgv1G6m30ruNfybKN3mV+JaWS2NWsCnZNYgW7nFtBraZXkCsZFtwrSZasLudZUrWcammplWxLSzUT7lDEX+DL2cZX",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(colors=["ox_E__1", "ox_E__2", "ox_E__3", "white"]))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(avoid_same_color_adjacent(color="ox_E__1", adj_type=8))
        self.add_program_line(avoid_same_color_adjacent(color="ox_E__2", adj_type=8))
        self.add_program_line(avoid_same_color_adjacent(color="ox_E__3", adj_type=8))
        self.add_program_line(grid_color_connected(color="not white", grid_size=(puzzle.row, puzzle.col)))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(1, color="ox_E__1", _type="area", _id=i))
            self.add_program_line(count(1, color="ox_E__2", _type="area", _id=i))
            self.add_program_line(count(1, color="ox_E__3", _type="area", _id=i))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            symbol, style = symbol_name.split("__")
            validate_type(symbol, ("ox_B", "ox_E"))
            fail_false(style in ["1", "2", "3", "4", "7", "8"], f"Invalid symbol at ({r}, {c}).")
            if style in ["1", "2", "3"]:
                self.add_program_line(f"ox_E__{style}({r}, {c}).")
            else:
                self.add_program_line(f"white({r}, {c}).")

        self.add_program_line(display(item="ox_E__1"))
        self.add_program_line(display(item="ox_E__2"))
        self.add_program_line(display(item="ox_E__3"))

        return self.program
