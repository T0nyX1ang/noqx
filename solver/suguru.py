"""The Suguru solver."""

from typing import Set, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, defined, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_number_adjacent


class SuguruSolver(Solver):
    """The Suguru solver."""

    name = "Suguru"
    category = "num"
    aliases = ["capsules"]
    examples = [
        {
            "data": "m=edit&p=7VRRa9swEH73rwj3fA+WZSe23rKu3UvmbU1GKcYEx3OpmY07Jx5DIf+9nySbDDboOlihMBSdP52ku/vudNl/G4q+4ogly5h9FhhBELOIApbC/PxxbOpDU6kZL4fDfdcDMH+4uuK7otlX7GXjsdw76kTpJet3KiNBTAGmoJz1J3XU75VOWa+xRSxypnZoDnXZNV1Pk06v3MUA8PIMb+y+QRdOKXzgdMRM18bFLZZl3ZdNtV05Yx9VpjdMZvONtWAgtd33yjg08Zl12bW72ih2xQEs9/f1A7HExn740n0dxqMiP7FePo8FjEwsDHQsDPoNi+BFWCT56YQiXYPHVmWG0uczjM9wrY4UJKRCplDgA1VqVCHshCbjKCp0Qh0hb63c4CZraeVbK30rIytX9swlbCxCjiUp8F3MOY4sikNOnC6ec+J0iUR+AqeUHMOzOzhdweUFEKzeWNsXVoZWzq3PheHyh2wngv6YKHj4a4pPhpQFrtfMiH5FuZfReujvirJCcdOh3VX9LO36tmiwXtt6Tmu03MmjH2RnJhF3+L8LX0UXmoL5z3qd/+g1PhFChkTjvf7UFUwPw7bYItuE//wXCRE9k3uP",
        },
        {
            "url": "https://pzprxs.vercel.app/p?suguru/16/6/gkca9ilcv6lapem2c8fraajtje56rd8u3r2j5h1n3k3p4m4j42j2m2p5k5g2l2h2j3000g0000000000000000",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(unique_num(_type="area", color="grid"))
        self.add_program_line(avoid_same_number_adjacent(adj_type=8))

        exclude: Set[Tuple[int, int]] = set()
        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")
            exclude.add((r, c))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, exclude=exclude)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
