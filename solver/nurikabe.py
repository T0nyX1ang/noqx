"""The Nurikabe solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import (
    avoid_unknown_src,
    count_reachable_src,
    grid_color_connected,
    grid_src_color_connected,
)
from noqx.rule.shape import avoid_rect


class NurikabeSolver(Solver):
    """The Nurikabe solver."""

    name = "Nurikabe"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVdT4MwFH3nV5j7fB8oLRvjxcyP+TLnx2YWQ8jCEOMiC5MNY7rw3729IGjcgyZmxsSUHs65benphZb1UxHlCQrbXNJDulNRwuPqeB2udl0mi02a+AfYLzYPWU4E8WIwwPsoXSdWUPcKra3u+bqP+swPQACCQ1VAiPrK3+pzX49Qj6kJUFFsWHVyiJ62dMrthh1XQWETH9Wc6C3ReJHHaTIbVpFLP9ATBDPPEY82FJbZcwK1D6PjbDlfmMA82tBi1g+LVd2yLu6yxwLepihR9yu74x12ZWtXNnblbrvOj9hNV9kuo72wLCnh12R15gfG9U1LvZaO/W1pHG1BeTTUo7fM7wQ6iqRoZNclKRvp2SQ7jewJkm4jhe2QVu90l3S31cLM1Wu1NJM5rXbN4+EQ6gg5FOzzlnHA6DBOaBmoJeMJo83oMg65zynjlPGYUTF2uE/XJOKLqQJJxhwERdlQVd724C2Q1fb7WNy/FwutAMZFfh/FCX2zo2I5T/KDUZYvoxToeCgteAGu/KWp/xNj7yeGSb79rXPj9/dmQHmlHaIvEFbFLJrFWQr0u0ETV+6n+N7d0wYOrVc=",
        },
        {
            "url": "https://puzz.link/p?nurikabe/19/12/g5zw3k2h4g4k.v.h2i2g4z3n7j3k2h4h4k3i4j3zzk2i2k2p6j2k6k",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="black"))
        self.add_program_line(avoid_unknown_src(color="not black"))

        all_src: List[Tuple[int, int]] = []
        for (r, c, d, label), _ in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            all_src.append((r, c))

        for (r, c, _, _), num in puzzle.text.items():
            current_excluded = [src for src in all_src if src != (r, c)]
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color="not black"))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num, (r, c), color="not black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
