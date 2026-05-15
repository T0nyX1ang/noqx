"""The Suguru solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_number_adjacent


class SuguruSolver(Solver):
    """The Suguru solver."""

    name = "Suguru"
    category = "num"
    aliases = ["capsules"]
    examples = [
        {
            "data": "m=edit&p=7VXPb9pMEL3zV0R73gP7yyS+0RR6oaRtUkWRhRAQfw36jJwaXFVG+d/zZryLLYREqZKoh8jy6PE8s/OePbusf5azIpURLnMuu1Lh0lHEt7KW766/bpabLI3PZL/cPOQFgJRXw6H8b5atU9lJfNqks60u4qovq09xIpSQQuNWYiKrr/G2+hxXA1ld45GQCtyoTtKAgwbe8nNClzWpusBjjwHvABfLYpGl01HNfImT6kYK6vOBqwmKVf4rFV4H/V7kq/mSiPlsAzfrh+Wjf7Iu7/P/S5+LBcWqzDbLRZ7lBZHEPcmqX1sYH7BgGgsEawuEDlggZ69s4eKwhSd8nm8wMY0T8vO9gecNvI63iON4K7QOb6T+hkL3iMAnDYTlDNsi3F6Js0S4FsFrRA3R4zVMi+CM3aIQo1jSHcchR83xBoplZTh+5Njl6DiOOGcAI8pgtA36aKzojFSRqbHWDU9YBx45GsoJK2yEgJ2TykU1pk0SQWrgI1hnHvlt3PO1EdYPfQmTb8IW2LWw9TkWGpzHDvpDjqO+XoNCX+17aWDjsSHscwzyjddJvoxf0xD22gx0hlrqaz3Ph0BrzYCJpy/LeggTj5d9y6/8kqPlGPGn6NFonTZ8JJMHh3q8xBQclZfQBOwuuP1bPOkkYnD/Iz0b58VqlmGDjsvVPC3Cb5ySTx3xW/CdaJy3UqPo/ej8p49O+ljdk2b4DWb2iJwEbxz7PAn/z5jO8E9N+6pH7h/L6WwKs4JIX1BdHeZbG/JFCy0k7qT9iUQq2Es/XvDe4VU60Jl3QsH+iLz5lsFJP+k8Aw==",
        },
        {"url": "https://pzprxs.vercel.app/p?suguru/6/6/adbli15d2tluj2g1l2l3l4l5g"},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(unique_num(_type="area", color="grid"))
        self.add_program_line(avoid_same_number_adjacent(adj_type=8))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
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
