"""The Smullyanic Dynasty solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected


class SmullyanicDynastySolver(Solver):
    """The Smullyanic Dynasty solver."""

    name = "Smullyanic Dynasty"
    category = "shade"
    aliases = ["smullyanicdynasty"]
    examples = [
        {
            "data": "m=edit&p=7Vbfb9NADH7vXzHd8z3EvsvPF1TGykvpgBZNUxRVbcm0ilQZaYNQqv7v+JyWFqeggcTgYUrPcr+z7/zZOV/Wn+tZlWsw7mci7WmgxzfIA6zl4e2fyXJT5MmF7teb+7IiRevrwUDfzYp1rnvp3izrbZs4afq6eZ2kCpRWSANUppt3ybZ5kzQj3YxpSmmbabWqi81yURZlpRgDshu2jkjq1VG94XmnXbYgeKSP9jqpt6QultWiyKfDFnmbpM1EK7f3S/Z2qlqVX3K1j839X5Sr+dIB89mGGK7vlw9KG5pY1x/LT7U67LDTTb9lMD4wwF8zMEcG5jsDc54B/nUGcbbbUXHeE4dpkjo6H45qdFTHyXbnwtoqEzhXQ6G0FVTWcwCeAMYB3gkgXXzrAP8IBAzYIxDCIcUHwIg1Ql8CgXQJhUUUisBiGRh4sVgEwJM2AB1EBgcQiK0AQaQJEAVpQE7Di1Mk6NhIVmA6ERpZAbDQQToxW1kEsDLHYEOZH9+XvPxIegWdjAUo4wkCuU4QSiTEDtLZvVN1CCPJK4ylTSxrgZ6sF3bqjtDx6rwJCDKHCPI1RJSZR2Oll5Xc0UruaCOJ+D960RkGPsm3LAcskeWEDrpuDMtXLD2WPssh21yxvGF5ydKyDNgmdK3ikc2E20iklaFcIDUEShu2DeYJQkxNwJfaucd/nvmTmayXqnFd3c0WOd0/o3o1z6uLUVmtZoWi23/XU18Vj9RodObPHwT/8QeBK5T3W58F/76xpJRwOtfNtVYP9XQ2pWRzvs7i5ie43eOhwP0W98359enifuyEyZ48b9Twst43",
        },
        {
            "url": "https://pzplus.tck.mn/p.html?smullyan/14/14/0222212212111121323232333112233322333233221313333133232221312213133231233323243222321332331223213222222334322231222023222332212310123433332123313333231311223234343331322323233331323202121222122221",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(avoid_same_color_adjacent(color="gray", adj_type=4))
        self.add_program_line(grid_color_connected(color="not gray", adj_type=4, grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if isinstance(num, int):
                self.add_program_line(
                    count_adjacent(num, (r, c), color="gray", adj_type=8).replace(":-", f":- not gray({r}, {c}),")
                )
                self.add_program_line(
                    count_adjacent(("ne", num - 1), (r, c), color="gray", adj_type=8).replace(":-", f":- gray({r}, {c}),")
                )

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
