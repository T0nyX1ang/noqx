"""The Norinuri solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected
from noqx.rule.variety import nori_adjacent


class NorinuriSolver(Solver):
    """The Norinuri solver."""

    name = "Norinuri"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVNj9MwEL3nV6A5zyGO3TT1BZWy5VJ2gRatVlFUpSGrjUhxSRuEXPW/78wk2sCyBz6kIiTk+vW98Vh9nsTT/ec2b0pUIX90gvRNw6hEZpTEMsN+rKpDXdpnOG0Pd64hgng1n+NtXu/LIO2zsuDoJ9ZP0b+yKShAiGgqyNC/tUf/2vol+iUtASqKLbqkiOjFQK9lndmsC6qQ+GXPid4QLaqmqMv1oou8salfIfDvvJDdTGHrvpTQ+2BduO2m4sAmP9Bh9nfVrl/Ztx/cx7bPVdkJ/fSRXTPY1YNdpp1dZk/Y5VP8ud16554yOslOJyr4O7K6tim7fj/QZKBLeyS8tEfQIW99Ti66pwKjiAL8BvQ6Zj15kGOW8YOcjB5tV2pMkdGgtSGdfKN5fTxoo0lHg47ZkOk1mVRi9UZwLhgJrugk6LXgS8FQcCS4kJwLwWvBmaARjCVnzLX4yWqBVmAjBEOnMV3pzuAt1d0N/H5wcf+xWBaksGyb27wo6bWdue3O7atDCdQdTgF8BZmp5mbzv2GcvWFw8cNfaht//16mVFet0F8h7Np1vi5cDfRvg78TN+aH+NlPS5cdPrVNtXEtZME9",
        },
        {"url": "https://puzz.link/p?norinuri/10/10/o.zt9g8lcg5zt.o", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("black"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_unknown_src("not black"))
        self.add_program_line(nori_adjacent(color="black"))

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
            if color in Color.DARK:
                self.add_program_line(f"black({r}, {c}).")
            else:
                self.add_program_line(f"not black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
