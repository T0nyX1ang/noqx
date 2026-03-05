"""The Fillomino solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import count_reachable_src, grid_src_color_connected


def fillomino_constraint() -> str:
    """Generate the Fillomino constraints."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")

    # propagation of number
    rule = f"number(R, C, N) :- number(R0, C0, N), {tag}(R0, C0, R, C).\n"
    # this is a huge optimization
    rule += ":- grid(R, C), number(R, C, N1), number(R, C, N2), N1 < N2.\n"

    # same number, adjacent cell, no line
    rule += f':- number(R, C, N), number(R, C + 1, N), edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- number(R, C, N), number(R + 1, C, N), edge(R + 1, C, "{Direction.TOP}").\n'

    # different number, adjacent cell, have line
    rule += f':- number(R, C, N1), number(R, C + 1, N2), N1 != N2, not edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- number(R, C, N1), number(R + 1, C, N2), N1 != N2, not edge(R + 1, C, "{Direction.TOP}").\n'

    # special case for 1
    mutual = [
        f'edge(R, C, "{Direction.TOP}")',
        f'edge(R + 1, C, "{Direction.TOP}")',
        f'edge(R, C, "{Direction.LEFT}")',
        f'edge(R, C + 1, "{Direction.LEFT}")',
    ]
    rule += f"{{ {'; '.join(mutual)} }} = 4 :- number(R, C, 1).\n"
    rule += f"number(R, C, 1) :- {', '.join(mutual)}.\n"
    rule += ":- number(R, C, 1), number(R1, C1, 1), adj_4(R, C, R1, C1).\n"

    return rule


def fillomino_filtered(fast: bool = True) -> str:
    """Generate the Fillomino filtered connection constraints."""
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")
    rule = ""
    tag1 = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    rule += f"have_numberx(R, C) :- grid(R, C), not {tag1}(_, _, R, C).\n"

    rule += f"{tag}(R, C, R, C) :- grid(R, C), have_numberx(R, C).\n"
    rule += f"{tag}(R, C, R0, C0) :- grid(R0, C0), grid(R, C), {tag}(R, C, R1, C1), have_numberx(R0, C0), have_numberx(R, C), adj_edge(R0, C0, R1, C1).\n"

    if fast:
        rule += "{ numberx(R, C, 1..5) } = 1 :- grid(R, C), have_numberx(R, C).\n"
        rule += f":- numberx(R, C, N), #count{{ R1, C1: {tag}(R, C, R1, C1) }} != N.\n"
    else:
        rule += f"{{ numberx(R, C, N) }} = 1 :- grid(R, C), have_numberx(R, C), #count{{ R1, C1: {tag}(R, C, R1, C1) }} = N.\n"
    rule += ":- number(R, C, N), numberx(R1, C1, N), adj_4(R, C, R1, C1)."

    rule += f':- numberx(R, C, N), numberx(R, C + 1, N), edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- numberx(R, C, N), numberx(R + 1, C, N), edge(R + 1, C, "{Direction.TOP}").\n'
    rule += f':- have_numberx(R, C), have_numberx(R, C + 1), numberx(R, C, N), not numberx(R, C + 1, N), not edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- have_numberx(R, C), have_numberx(R + 1, C), numberx(R, C, N), not numberx(R + 1, C, N), not edge(R + 1, C, "{Direction.TOP}").\n'

    return rule


class FillominoSolver(Solver):
    """The Fillomino solver."""

    name = "Fillomino"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VNdT4MwFH3nVyx97gO0fGy8zbn5MvFjM8tCyMI2dEQICsOYEv67txc2bKIPmqh7MM09Oae9Tc9te4vnMswjasPgfapTAwazbQzDNDH0dszjfRK5PTos97ssB0Lp1WRC78OkiDS/zQq0SgxcMaTiwvUJIxTDIAEVN24lLl3hUTGDJUINmJsCMwhlQMcdXeC6ZKNm0tCBey0HugS6ifNNEq2mzcy164s5JfKcM9wtKUmzl4g021BvsnQdy4l1uIdiil381K4U5TZ7LMnhiJqK4ed2eWeXH+3yj+2yn7c7COoarv0WDK9cX3q/62i/ozO3qqWvijAGW+Vb48sQZoJknbSVVc5B9jtpgXSO0jSVZNNRpKUeZFmKtOVe3klbkQ5Xkh1LMem8PwjKMrC4JeIEkSHOoXYqOOI5oo5oIU4xZ4y4QBwhmog25jjy9r50v79gx2cMm7UZ1vd5oPlkvH2Iel6Wp2EC/8sr03WUHzQ0dK2RV4KBr2P+9/gf9bh8Av3UfuKp2YHeCLQ3",
            "config": {"fast_mode": False},
        },
        {
            "data": "m=edit&p=7VRNb9pAEL3zK6I9z2G//HmjKfRCSdtQRZGFEBC3QQU5BVxVi/zfOztecNfCitK0aQ/V2qM3+3bW49nZt/tazrc5JDhUDBwEDhVzemNtH+7GZLVf5+kF9Mv9fbFFAHA1HMKn+XqX9zK3ato7mCQ1fTBv0oxJBvQKNgXzPj2Yt6kZg7lGioHAuREiwUAiHDTwhniLLutJwRGPHUZ4i3C52i7X+WxUz7xLMzMBZr/ziqItZJviW87qMPKXxWaxshOL+R5/Zne/enDMrrwrvpTs+IkKTL87XdWkq07pqvPpyj+fbjKtKiz7B0x4lmY2948NjBt4nR4qm9eByRhDFZ40nQyTCbr65Crpu8p3Ay9Wxx4bSo8NI9/1F0fcYyM/NvK/G/nfTXw2CXw39Bf7/ys4b/nCixbcDxeS+3yrJKJVE6HCFu8XWOif98MzEXQyt2SHZCXZCR4cGEX2NVlONiA7ojUDsjdkL8lqsiGtiezRP6k5np8O07a+SYzNEcQ1CGwFLAh1WAOByiISbA+F/ScVSFszi0MB0naRxYHF2uEQceLWxyC1cFgCxtc4Qe3ibj3HPQk/Wp0MtxOtEfxbM9NexgZ3n/OLcbHdzNeoAuNys8i3Rx9lt+qx74xe6kT9X4n/khLbI+AvfOWeqwCZGTRXEswVsIdyNp8tC2w1LCHRx1vaRbuL20W7u9xJ19f7PI060kFwfp5AwTlPoAB1/l+tKl1x8onESY66aKdQv0g/srmTxd+c2ou3LarztPcD",
        },
        {
            "url": "https://puzz.link/p?fillomino/15/15/h1o5i8g2m6g3g7i3h4h1i1g6g4h2g3h4g2i5h2i4h3l4h1h5m4h2g2h6k7h3i3h7k7h2g2h3m2h1h5l3h4i3h3i-10g4h4g1h3g7g1i8h4h3i2g2g2m8g6i1o1h",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?fillomino/9/9/rb-134k-13i-13i7k5h-13k-13h8k6i-13i-13k9-13am2j",
            "test": False,
        },
    ]
    parameters = {"fast_mode": {"name": "Fast Mode", "type": "checkbox", "default": True}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(fillomino_constraint())
        self.add_program_line(fillomino_filtered(fast=puzzle.param["fast_mode"]))

        numberx_ub = puzzle.row * puzzle.col - sum({num for _, num in puzzle.text.items() if isinstance(num, int)})
        self.add_program_line(f":- #count{{ R, C: grid(R, C), have_numberx(R, C) }} > {numberx_ub}.")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")
            self.add_program_line(grid_src_color_connected(src_cell=(r, c), color=None, adj_type="edge"))
            self.add_program_line(count_reachable_src(target=int(num), src_cell=(r, c), color=None, adj_type="edge"))

            if num == 1:
                self.add_program_line(f':- not edge({r}, {c}, "{Direction.LEFT}").')
                self.add_program_line(f':- not edge({r}, {c}, "{Direction.TOP}").')
                self.add_program_line(f':- not edge({r}, {c + 1}, "{Direction.LEFT}").')
                self.add_program_line(f':- not edge({r + 1}, {c}, "{Direction.TOP}").')

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))
        self.add_program_line(display(item="number", size=3))
        self.add_program_line(display(item="numberx", size=3))

        return self.program
