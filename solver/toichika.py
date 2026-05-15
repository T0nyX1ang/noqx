"""The Toichika solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, count, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, tag_encode, validate_direction
from noqx.rule.neighbor import adjacent, area_adjacent


def toichika_pair(color: str) -> str:
    """Generate a rule to create Toichika pairs and constraints."""
    rule = "{ pair(R, C1, R, C2) } :- arrow_N_W__5(R, C1), arrow_N_W__1(R, C2), C2 > C1.\n"
    rule += f":- pair(R, C1, R, C2), grid(R, C), C1 < C, C < C2, not {color}(R, C).\n"
    rule += "{ pair(R1, C, R2, C) } :- arrow_N_W__7(R1, C), arrow_N_W__3(R2, C), R2 > R1.\n"
    rule += f":- pair(R1, C, R2, C), grid(R, C), R1 < R, R < R2, not {color}(R, C).\n"

    # every arrow symbol should belong to a pair
    rule += ":- arrow_N_W__1(R, C), not pair(_, _, R, C).\n"
    rule += ":- arrow_N_W__3(R, C), not pair(_, _, R, C).\n"
    rule += ":- arrow_N_W__5(R, C), not pair(R, C, _, _).\n"
    rule += ":- arrow_N_W__7(R, C), not pair(R, C, _, _).\n"

    # paired numbers must not be in adjacent rooms
    tag = tag_encode("area_adj", 4, None)
    rule += f":- pair(R1, C1, R2, C2), {tag}(A1, A2), area(A1, R1, C1), area(A2, R2, C2).\n"
    rule += f":- pair(R1, C1, R2, C2), {tag}(A2, A1), area(A1, R1, C1), area(A2, R2, C2).\n"

    return rule


class ToichikaSolver(Solver):
    """The Toichika solver."""

    name = "Toichika"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VdrTxs5FP3Or6j8tZbWj3lG2g+BQrddCFBALImiaAgDhE4YdpJAO4j/3nM9d8gTulR0H9IqiX1yfOfec23H1xn9OUmKVGpFbxtJ9Hh5OnIfEwXuo/h1OBhnaeONbE7Gl3kBIOXu1pY8T7JRKj+eXG5v5M27d80/bqNxu63fq8kHdXy1dfX20/D3DwNb6K1WtLeztzMwF83fNtb3g823wd5kdDROb/eHev3qqH14vnd8EZuvm622V7Z3lf+xff7LbfPo17UOa+iu3Zdxo2zK8n2jI7SQwuCjRVeW+437cqdRnsjyAENCRl0phpNsPOjnWV4Ix2nYbVcPGsDNKTx244Q2KlIr4BZjwBPApCjyu16rt15Re41OeSgFBV93jxMUw/w2pWgkjr738+HpgIjTZIz5G10OboS0GBhNzvLPEzbV3QdZNl+WApzUKRCsUiC0IgXKbDaF49dPIe4+PGB5PiGJXqND+RxNYTSFB417tC3XateeNO6F1XATyoU5FoEF7S/RWgXg7TJvidcLPEJsuUDGtYfQIUvr2neuVa71XbvtbDYhyRhfGgOHBtvM4LdgQsahNB70EvbUFNsYWFVYe7CP2B6/Jc+wvZHGZ58+/D9i2Pv+FAf8bIBng5gx/IfsP0TcyKtwZGcw/EeYNIc1MMf1ob9+NoL/iGNF0BCxBvd75xxD8snYp7js0yPNrMfCv8d+NOaE1tDlS/NQ28OPX/uBTcg2IZ4Na23IscYezQPnbmluOS/yaVk/xbVsb5Gvx/o96Pc4lodYAccKKBbrDClf1h/BZ1zPJ56tcQCfYe2T5r/WRutYPwv/EeuM6KyseKtiaXXlB720ptKPXlpb2aMHZnvssUesNewrnQ7rKi568JUe9MBVjuil5b2HXtp6/9Caxqwzhh7FehT0KLZX5L+OBW2P2AKzZsL1nkeOVrEeBT2a9Wjo4XWxWKMphr2pcwTm/Y8euNob6IE5Ftbd8ro7n5pzxL6yvK/Qw551kn2NSY+q9zzlyzimfNm/ohxr/zT/rAf7x/L+QQ9McXEAHLtjYMO1nmsDdzyEdIj9xWNOkMBoxWFHSc+eau40/rFT6rtSO/gVUVWff/n/Pa671hEHk+I86aeoS5tnF+mbVl4MkwzfDi6Tm1TgdiBGedYbVVa99EvSH4tGdUGZHZnjrifD0xTVdYbK8vwmG1yv8lAPzZGDi+u8SFcOEZlC6xOuaGiFq9O8OFvQdJdk2Xwu7vI2R/UHRT+bp8YFKvfMd7fl5phhMr6cI2aq/Jyn9HphMsfJvMTkc7IQbTidjoc18UW4D+q2oeX8/yr3r77K0VKpH77Q/aTT7DtyOphx3FbKXSluJr2kh9kW+Ncgn+NRyf8RHjesF+l8Lf6puE/p1LgqvGwAd8Sfy3uvwR8s+w+7f/t+dsdkXjxTs6aDi/SKygX2meI1M7qKf6JOzYwu8ktFicQu1yWwK0oT2MXqBGq5QIFcqlHgnihT5HWxUpGqxWJFoZbqFYWaLVmd7to3",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent())
        self.add_program_line(area_adjacent())
        self.add_program_line(shade_cc(colors=["gray", "arrow_N_W__1", "arrow_N_W__3", "arrow_N_W__5", "arrow_N_W__7"]))
        self.add_program_line(toichika_pair(color="gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(1, color="not gray", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"gray({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            fail_false(
                symbol_name.startswith("arrow_N") and symbol_name.split("__")[1] in ["1", "3", "5", "7"],
                f"Invalid symbol at ({r}, {c}).",
            )
            self.add_program_line(f"{symbol_name.replace('B', 'W')}({r}, {c}).")

        self.add_program_line(display(item="gray", size=2))
        self.add_program_line(display(item="arrow_N_W__1", size=2))
        self.add_program_line(display(item="arrow_N_W__3", size=2))
        self.add_program_line(display(item="arrow_N_W__5", size=2))
        self.add_program_line(display(item="arrow_N_W__7", size=2))

        return self.program
