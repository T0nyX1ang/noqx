"""The Light and Shadow solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Point, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected


class LightShadowSolver(Solver):
    """The Light and Shadow solver."""

    name = "Light and Shadow"
    category = "shade"
    aliases = ["lightandshadow"]
    examples = [
        {
            "data": "m=edit&p=7VZdT9tcDL7vr0C+9kXOR/N1MzEGu2Fle8uE0FFVpV0QFe3CUjJNqfrfsX0CJ2WgFzSpV6iK7Tx5Yj92zkm6/tUUdYlKobJoUoyQIrTDGIdJhHGcyBF1v/PF3bLMD/CwubuuagoQz05O8KpYrsuB61iTwabN8vYQ28+5AwUImg4FE2y/5Zv2S96OsB3TJUBL2KknaQqPQ3gh1zk68qCKKB75mG+7pHC+qOfLcnpKVwn5mrv2HIHrfJS7OYRV9buETgefz6vVbMHArLijZtbXi9vuyrr5Ud00HVdNttgeernjZ+SaIJdDL5ejZ+RyF/8ud3lbPSc0m2y3NPD/SOo0d6z6ewjTEI7zDZgUcosQD8UlyrtMXOrPlNLea+O97XD7cJ54n0Sdt95nHS/z6XTki2jD+aj+iOvTvQ4y6t+vBxHkn2gHxJTNgQkM1kqMKFC4sIM0ULgPB8MeQ7L2knCLDj4ERio5CHhgcPc7OZQSJA4UmYwD2+NoQWh1P3J4ag6SHsdKqX4enuiOGmUlT0+OTFvuCpy4Uxg4Ms2+5lj67DUuT2m3ViKZ+7X4Ce7Wyp6OR57ubu+ZDJmQwHk6ZR1J5l4eWRU7ebR5mPwjh1eMTNVzaO2ofEP2UuyJWC32nJY2tkbsJ7GR2KHYU+Eci70QeyTWio2Fk/DmePX28VvDUufar+g9aHNGyyv56W/4jr6MTgYOxk19VcxLemeOmtWsrA9GVb0qlkCfp+0A/oAczvDX7v2LtfcvFg8/euXG29te+x85juZqEmzPEG6baTGdV0ugvzv4Mn75Rpzy6Bdw8zbcpn/he58mvbzgZ1MvbopZCZPBPQ==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(avoid_unknown_src(color="black"))
        self.add_program_line(avoid_unknown_src(color="not black"))

        all_src: List[Tuple[int, int]] = []
        for (r, c, d, label), _ in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            all_src.append((r, c))

        for (r, c, _, _), num in puzzle.text.items():
            current_excluded = [src for src in all_src if src != (r, c)]
            color = "black" if puzzle.surface.get(Point(r, c)) == Color.BLACK else "not black"
            self.add_program_line(f"{color}({r}, {c}).")
            self.add_program_line(grid_src_color_connected((r, c), exclude_cells=current_excluded, color=color))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num, (r, c), color=color))

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"black({r}, {c}).")
            else:
                self.add_program_line(f"not black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
