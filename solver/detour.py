"""The Detour solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, display, fill_line, grid
from noqx.rule.helper import full_bfs, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_turning, single_route


class DetourSolver(Solver):
    """The Detour solver."""

    name = "Detour"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7ZVLb9pAFIX3/Ipo1ncxD9sz402VpqQbmvSRqqoQQoTQBhVKCqGKHPHfe+6dAUcqKFVUpZvK8ujzuWP7+DB3WP1Yj5YTCjhcIE0GhyusnFZHOXU+Lqa3s0l9RMfr2+vFEkB0fnpKX0az1aTTz7MGnfsm1s0xNa/rvrKK5DRqQM27+r55Uzddaj6gpMhA64GMIgvstvhJ6kwnSTQafAZ26bbPwPF0OZ5Nhr2kvK37zQUpfs9LuZtRzRc/Jyo9Qq7Hi/nllIXL0S0+ZnU9vcmV1fpq8W2d55rBhprjZLe3x65r7bqdXbffrv0bdmfT75PF3T6rcbDZIPL3MDus++z7Y4uhxQ/1/YY98Wjqe1UFjSc4NgMO/LQXKl3FCleFsA8F2AgHrVv2djcnyN1aOPr23hhtfsOGE+AXn8poZbyAL2qcjK9k1DKWMvZkThdGTRnJeKNqi2VU4fXeZcajfZnYQw9Z99DDVi/BPnGAHrMeoMet7sExcSyx4rMePa/+zOgEkzygDo6ZodusGwN2maG7rFvoLuvWgZMH1MkWWXfQi60OD0XygDrZMusF9HKrw0OZvQX+dpvZtjnw9/LPJ1y0mfC3hypz9SAf5MA/pXAAb7+RM6kyV7t8JAcdModdVpKJ0TkH3ebG+RibGbuL2WbCWeX5Tre5cT4uz3e2zZCzckXm4kGe8OmyTwefjn1uuDt5KZ3IWMhYyRLz3BhPaJ2nrWblKniLgQA+gffkkZ/jNiMfE0XixgSFSDFR1BRNIkPcVC61xqPf1reVbOjtUT7v9aDTVz1sXUdni+V8NMP+1b36+uDqbD2/nCy31/jr2HTUnZKTNw4q/v+b/IN/E45fP1tj/OFafsROH8nmhqLmnNTNejgajhdYZAgvFaXHDhWl7Q4UUyceKKbmPFSUft1fxH5wqOB/Kzx72tg8Bp1f",
        },
        {
            "url": "https://puzz.link/p?detour/12/12/4i461svho42s221q10sfps312904a1aldml2h84k190ka5bdlak2h03147g91374232",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="grid", adj_type="line"))
        self.add_program_line(single_route(color="grid"))
        self.add_program_line(route_turning(color="grid"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))

            if rc:
                num = puzzle.text[Point(*rc, Direction.CENTER, f"corner_{Direction.TOP_LEFT}")]
                if isinstance(num, int):
                    self.add_program_line(f":- #count {{ R, C: area({i}, R, C), turning(R, C) }} != {num}.")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
