"""The Nurimisaki solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from noqx.rule.shape import avoid_rect


def avoid_unknown_misaki(known_cells: List[Tuple[int, int]], color: str = "black", adj_type: int = 4) -> str:
    """Generate a constraint to avoid dead ends that does not have a record."""

    included = ", ".join(f"|R - {src_r}| + |C - {src_c}| != 0" for src_r, src_c in known_cells)
    main = f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }} = 1"

    if not known_cells:
        return f"{main}."
    return f"{main}, {included}."


class NurimisakiSolver(Solver):
    """The Nurimisaki solver."""

    name = "Nurimisaki"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVRj5pAEH7nV5h5ngeWBcR9s97ZF8u11eZyIcQg5XLkoFiQplnjf7/ZgYSIPrQPtUnT4H759ptZ+BidsfneJnWGQpiPDNBGYuh6Pi8hHF52f23yQ5GpCc7bw0tVE0F8WC7xOSmazIr6rNg66pnSc9TvVQQCEBxaAmLUn9RRf1A6RL2mEKBL2qpLcojeD/SR44YtOlHYxMOO+0SfiKZ5nRbZdkVRUj6qSG8QzHPe8WlDoax+ZND7MPu0Kne5EXbJgV6mecn3faRpv1avbZ8r4hPqeWd3fcWuHOwa2tk17I/ZLfbVNaOz+HSign8mq1sVGddfBhoMdK2OhKE6gpzSUR/97jsBz6atHLauufGEXPfCdHYWD7xRXIjxCeHIC8U8c7iJkGKc4ZmMM8UfnZleZATnCr2f4Ld8YlwyOowbKgJqyXjHaDN6jCvOuWd8ZFwwuow+50xNGX+x0CAdUC6CG4ByuqrfwFskqVmvXN6/q8ZWBOu2fk7SjHojbMtdVk/Cqi6TAmgMnSz4Cbzod0RT7f9kuvlkMsW3f2s+/f0ujqiu1Ev6AWHfbpNtWhVAf2todDe40G/unlodvrV1XuZN8ppDbL0B",
        },
        {
            "url": "https://puzz.link/p?nurimisaki/15/15/v.h.h.h.h.zr.j.h.i.zk.l.q.m.j.l.r.i.i.i.zr.h.h.h.h.v",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?nurimisaki/22/15/j.zj3j.h.v.n.g..k3q4z4l.l2w3n4h.u5g3o3k.m.h.g4u.p.k3h.j.p3n.i3k.t.u4o.h3h.g3r4",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not black"))
        self.add_program_line(avoid_rect(2, 2, color="black"))
        self.add_program_line(avoid_rect(2, 2, color="not black"))
        self.add_program_line(count(("gt", 0), color="black", _type="grid"))

        all_src: List[Tuple[int, int]] = []
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(count_adjacent(1, (r, c), color="not black"))
            all_src.append((r, c))

            if isinstance(num, int):
                self.add_program_line(bulb_src_color_connected((r, c), color="not black"))
                self.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black"))

        self.add_program_line(avoid_unknown_misaki(all_src, color="not black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
