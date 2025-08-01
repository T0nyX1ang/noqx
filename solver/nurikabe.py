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
            "data": "m=edit&p=7VXBjtowEL3nK1ZznkOcOBB8qeh26YVm20K1WkURCmlWG21oaCDVyoh/35lxRFqVQ6tKVJUq48d74wl+Hsdm97XL2xKVz58wRvqmplUsPYhH0v2+Lat9XZornHb7x6Ylgng7m+FDXu9KL+2zMu9gJ8ZO0b41KShACKgryNB+MAf7ztgE7YKGADXF5i4pIHoz0DsZZ3btgsonnvSc6D3RomqLulzNXeS9Se0Sged5LU8zhU3zrYTeB+ui2awrDqzzPS1m91ht+5Fd97l56vpclR3RTp3dxRm74WCXqbPL7IxdXsWf2623zTmjk+x4pIJ/JKsrk7LrTwONB7owB8LEHEDH9GhMuyx7AiNNkjfdyXFEMjzJ2Cc5OsmJIhmdpPID0vo7PSY9HrTiuSaDDnmyYNAR/zy8oopIhBwq8XkvOBMMBJe0DLSh4BtBXzASnEvOjeCd4LWgFhxJzpgL8YulgpCMBQiaqqFd3S7gLQ3d8fuxcbn/sVjmpbDo2oe8KOmdTbrNumyvkqbd5DXQ9XD04Bmky5um/98YF78xuPj+b90bf/9splRXOiH2FmHbrfJV0dRAfzfIcR39FL+4ezrA8KVrq6d8XULmvQA=",
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
