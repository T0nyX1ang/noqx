"""The Nuribou solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected
from noqx.rule.shape import all_rect


def noribou_strip_different(color: str = "black") -> str:
    """Generate a rule to ensure that no two adjacent cells have the same shaded strips."""
    rule = f'nth(R, C, 1) :- rect(R, C, "{Direction.TOP_LEFT}").\n'
    rule += f'nth(R, C, N) :- rect(R, C, "{Direction.TOP}"), nth(R, C - 1, N - 1).\n'
    rule += f'nth(R, C, N) :- rect(R, C, "{Direction.LEFT}"), nth(R - 1, C, N - 1).\n'
    rule += f":- {color}(R, C), nth(R, C, N1), nth(R, C, N2), N1 < N2.\n"

    rule += f'len_strip(R, C, 1) :- rect(R, C, "{Direction.TOP_LEFT}"), not rect(R, C + 1, "{Direction.TOP}"), not rect(R + 1, C, "{Direction.LEFT}").\n'
    rule += f'len_strip(R, C, N) :- rect(R, C, "{Direction.TOP_LEFT}"), rect(R, C + 1, "{Direction.TOP}"), {color}(R, C + N - 1), not {color}(R, C + N), nth(R, C + N - 1, N).\n'
    rule += f'len_strip(R, C, N) :- rect(R, C, "{Direction.TOP_LEFT}"), rect(R + 1, C, "{Direction.LEFT}"), {color}(R + N - 1, C), not {color}(R + N, C), nth(R + N - 1, C, N).\n'
    rule += f":- {color}(R, C), len_strip(R, C, L), len_strip(R, C, L1), L < L1.\n"
    rule += f'len_strip(R, C, L) :- rect(R, C, "{Direction.TOP}"), nth(R, C, N), len_strip(R, C - N + 1, L).\n'
    rule += f'len_strip(R, C, L) :- rect(R, C, "{Direction.LEFT}"), nth(R, C, N), len_strip(R - N + 1, C, L).\n'
    rule += f":- {color}(R, C), {color}(R1, C1), adj_x(R, C, R1, C1), len_strip(R, C, L), len_strip(R1, C1, L1), L = L1."
    rule += f':- grid(R, C), rect(R, C, "{Direction.BOTTOM_RIGHT}").\n'
    return rule.strip()


class NoribouSolver(Solver):
    """The Nuribou solver."""

    name = "Nuribou"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVNb9pAEL37V0RznoP3C4gvFUlDL4S0hSqKLAsZ11FQjUwMrqpF/u+dHbsYpxySKCKXyOzTvJndnccMjDePZVykKJT7qAH6KOgxSvISWvPym2e23GZpcIbDcvuQF2Qg3oxGeB9nm9QLm12Rt7PngR2i/RKEIABB0hIQof0W7Ox1YCdopxQC1OQb15skmVetectxZ13WTuGTPWlsMu/ITJZFkqXzce35GoR2huDyXPBpZ8Iq/51Co8PxJF8tls6xiLf0ZTYPy3UT2ZQ/818l/EtRoR3WcqdH5KpWrtrLVcflyjeRm63zY0LPo6qign8nqfMgdKp/tOagNafBrnKKdqB6dNR1mXsCWribPkHrGHTiRhNVe9rr0r67rL+nwneHZcuF7HKliOuWa/9JdsHpOx5jOikF5zy4c+B3uOSchzdI2RUt1RPOKsQB73dUSiMP4lRGwcW8YxwxSsYZ1RqtYvzM6DMaxjHvuWK8Zbxk1Iw93tN33XpmP0FRqTR1iOoj6+aeQFuoejwjjj3mI/KaSOSFMC2L+zhJ6S8+KVeLtDib5MUqzoCmaeXBH+DFv1n9MWBPPmBd8f0Xjdn3nxIh1ZXe6PYGYV3O43mSZ0BvZ3R+Y/7zn1w9jZLI+ws=",
        },
        {"url": "https://puzz.link/p?nuribou/20/15/h5o6zs6k3i3h6zg4p4zi.pbzl7h3zz4k4l9v7zn4h.l4k4o4q7i2", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(avoid_unknown_src(color="not black", adj_type=4))
        self.add_program_line(noribou_strip_different(color="black"))
        self.add_program_line(all_rect(color="black"))

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

        self.add_program_line(display(item="black"))

        return self.program
