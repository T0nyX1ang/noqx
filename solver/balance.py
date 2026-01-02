"""The Balance Loop solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import validate_direction
from noqx.rule.loop import loop_segment, loop_sign, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected


def balance_rule() -> str:
    """Generate a balance rule."""
    rule = ':- black(R, C), segment(R, C, N1, N2, "T"), |R - N1| = |C - N2|.\n'
    rule += ':- black(R, C), segment(R, C, N1, N2, "V"), |R - N1| = |R - N2|.\n'
    rule += ':- black(R, C), segment(R, C, N1, N2, "H"), |C - N1| = |C - N2|.\n'
    rule += ':- white(R, C), segment(R, C, N1, N2, "T"), |R - N1| != |C - N2|.\n'
    rule += ':- white(R, C), segment(R, C, N1, N2, "V"), |R - N1| != |R - N2|.\n'
    rule += ':- white(R, C), segment(R, C, N1, N2, "H"), |C - N1| != |C - N2|.\n'
    return rule


def count_balance(target: int, src_cell: Tuple[int, int]) -> str:
    """
    Generate a constraint to count the length of "2-way" straight lines.

    A balance loop rule should be defined first.
    """
    r, c = src_cell
    rule = f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| + |{c} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "V"), |{r} - N1| + |{r} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "H"), |{c} - N1| + |{c} - N2| != {target}.\n'
    return rule


class BalanceSolver(Solver):
    """The Balance Loop solver."""

    name = "Balance Loop"
    category = "loop"
    aliases = ["balanceloop"]
    examples = [
        {
            "data": "m=edit&p=7Vbfb5swEH7PXxH52Q82vwK8ZV27lyzd1k5VhVBEMqZGIyVLylQR5X/v3RkK5Vxp0aa+bEJY5+/sj+/MZ8P+Z5Xtcql9GUk3lEpquAIVQgdix6VbNdf1+qHI47GcVg935Q4CKS8vLuT3rNjno6QZlY4OdRTXU1l/iBPhCEm3FqmsP8eH+mNcz2R9BSkhNWAziLSQDoTnXXhDeYzODKgVxHMTTyC8hXC13q2KfDEzRJ/ipL6WAp/zjmZjKDblr1yYadRflZvlGoFl9gDF7O/W2yazr76VP6pmrE6Psp6+Ltft5GJo5GJkkYtV/LHcYn2fP9qURunxCCv+BbQu4gRlf+3CsAuv4gO08/ggvACmhtIzL0V4E2Qaiw4IAQieu4HT5HULuAB4Xdcb5Cc4v084iWhC2w3Vi26E3f78SA+BoQKtsIT+I7QaVqHVUIZ2GI+DpbxEhtVoF3ncjsXFal7wem0Fz4jPWHyfIVhDt4w6wL7fcQSsogCV9EaEWE+PIWTVhKijNyJChm7pdTSsxVH9lwOG0WSb29Y2Dliyb2PjHo7icxhKTgItAxRVcxSVM5SsxXjJXwwlmzGU3MZ4yXIcteo15mPExoEW2CrZeJFzkyEtsHU1jDU5NzmUw2RTDpNXOTcZ1gJj8Rwm83Ju8rAFtusmP3NusrUFtusmi3NucjqDjd0HMPj9glzvUHsN56esXWrfU6uo9amd0Zhzam+oPaPWozagMRM8gU86o/sb71Q5wnfh1UUh7gCoDgNPSQ8c7lLkw0q4v6k5gfH4Q/Da5f9b2XSUiBl8iMfzcrfJCvgcz6vNMt+1ffj1OY7Eo6Abvhlaev//ht7+bwhXX73Zfvs72z+BhW32qawvpdhWi2yxKsFjsHZtErbua0mwGhjr9CScEfYEnCIs8eZrBicQWLPI7ld5UZZbkY6eAA=="
        },
        {"url": "https://puzz.link/p?balance/10/10/q1i8k8k0i1g8h1g9k9h0j1h8k8g0h9g0i1k9k9i0q", "test": False},
        {"url": "https://puzz.link/p?balance/10/10/0g00zg0l0m0k0k0k0k0h0m0k0n0l0h", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black"))
        self.add_program_line(defined(item="white"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line(shade_c(color="balance"))
        self.add_program_line(fill_path(color="balance"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="balance", adj_type="loop"))
        self.add_program_line(single_loop(color="balance"))
        self.add_program_line(loop_sign(color="balance"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            self.add_program_line(f"balance({r}, {c}).")
            self.add_program_line(loop_segment((r, c)))

            if symbol_name == "circle_L__1":
                self.add_program_line(f"white({r}, {c}).")
                num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count_balance(num, (r, c)))

            if symbol_name == "circle_L__2":
                self.add_program_line(f"black({r}, {c}).")
                num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count_balance(num, (r, c)))

        self.add_program_line(balance_rule())

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_io", size=3))

        return self.program
