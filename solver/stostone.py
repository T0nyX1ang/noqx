"""The Stostone solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import area_color_connected


def valid_stostone(color: str = "black") -> str:
    """Generate a constraint to enforce a valid stostone dropping."""
    below_C = f"grid(R, C), {color}(R, C), #count {{ R1: grid(R1, C), {color}(R1, C), R1 < R }} = BC"
    below_C1 = f"grid(R, C + 1), {color}(R, C + 1), #count {{ R1: grid(R1, C + 1), {color}(R1, C + 1), R1 < R }} = BC1"
    return f":- {below_C}, {below_C1}, BC != BC1."


class StostoneSolver(Solver):
    """The Stostone solver."""

    name = "Stostone"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VbBbhMxFLznKyqffVj72Ws7F1RKyqW0QItQtYqiNN3SiEQpSYPQRvl3xt7nGolKBSFAQiiKNfsy+97EM3F282k7XbdSKakqSV5WEkgaW0ujvLTKpXfFr4v5/aIdHsjD7f3tag0g5dnxsbyZLjbtoGHWeLDrwrA7lN3LYSOUkELjrcRYdm+Gu+7VsBvJ7hwfCalQO+lJGnBU4Pv0eURHfVFVwKeMAS8BZ/P1bNFOTvrK62HTXUgR5zxPd0colqvPrWAd8Xq2Wl7NY+Fqeo8vs7md3/Enm+316uNW5BF72R32cs+zXF/kUpFLD3Lpcbn698sN4/0e2/4WgifDJmp/V6Av8Hy420ddO0E63voMWnpvRG1QsHwJkkrUy7Qep1Wn9QKdZEdpfZHWKq02rSeJM8IArYPUBk01AkAE7Bkb4NBjA2wzrqWuFWMPTIzRp+Y+VgHXjMFxzKk1sGOMno571ujpuacDxzPHQY9nPQ58z3wHfsh8B6wZQ0NgDR4aAmvwTlLFHO+BWY8PwMwPCpj5QQOzhmCAeW6oJal+LvoBO8YE7BmDrwJjK0lXjHGvzvdCj9aMoUH3GtBPEnEdv2siYgwOMUfjACDLGJqpZoxZhmcRtBnWBk+JPUUPYNZGmGV5FqG/5f4G9Zrr8JfYX9wHzBz4S+wvegDzLAsNjjXAa2KvwcWhxd+9Rn/P/V08zGzJmMnYAuf8wEfWmbKUc2hj3irOT1UyWcfs6ZK3nE+Huss50SWTMWPOlIw51uCgwZU86MD8QA8ZS15XtnjN+UFGkIFvfMx50NgTzfupqfiu0UdnT2NmsqcxM9lHXfJAtvhO4FDmxPxkr2N+stehZMNgzw17YaDTZK9jBphjwbHMsdBmbfHXZt8x12Z/dclJTZyTfTxv4zFzlFaT1jodPy4ecz94EIoo0EuRZvWn4q8fe09qa7Dd6pGX/Req40Ejzrfrm+msxb/U6PpDe3C6Wi+nC1ydbpdX7Tpf4yFhPxBfRHo3FJ85/j83/KXnhmhB9VNPD3/gd/KEnAa7a7TszqS4206mk9kKGcPexbp139X/uHr80MeDrw==",
        },
        {"url": "https://puzz.link/p?stostone/8/6/r6olfpe0002rg40fvm3", "test": False},
        {
            "url": "https://puzz.link/p?stostone/18/18/9812a08ig24k9418p0a682gi0k4k515vfs091024c0h31c8oq3a6vqk46h11200000000007vvvo000001u0000fs0051bvbqg00vg001go01ovu7180eagc00s0g66g458gb436g8b8486g4638j",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row % 2 == 0, "The stostone puzzle must have an even number of rows.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(count(puzzle.row // 2, color="gray", _type="col"))
        self.add_program_line(area_color_connected(color="gray"))
        self.add_program_line(valid_stostone(color="gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            flag = True
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    flag = False
                    self.add_program_line(count(num, color="gray", _type="area", _id=i))

            if flag:
                self.add_program_line(count(("gt", 0), color="gray", _type="area", _id=i))

        for (r, c, d, _), draw in puzzle.edge.items():
            if d == Direction.TOP and r > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r - 1}, {c}).")

            if d == Direction.LEFT and c > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r}, {c - 1}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
