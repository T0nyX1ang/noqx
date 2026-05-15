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
            "data": "m=edit&p=7VZNTxsxEL3nVyCffbA93l3v3oBCLxTahgqhKIoChBI1UWggbbUo/71vvLM45aMUBP2Qqs3aL7PjN2/sWXsvPi+G85G2hn8UNHpc3oZ4u5DH28i1P76cjKo1vb64PJvNAbTe297Wp8PJxUh3euLW71zVZVWv6/p11VNWaeVwW9XX9bvqqn5T1Ye67uKR0qGv1XQxuRwfzyazuYo2C7+dZqAD3ErwID5ntNkYrQHeFQx4CDicz2dfB7uDjcb0turV+1px8I04nKGazr6MlIjj/8ez6dGYDUfDS6R4cTY+V5rw4GJxMvu0UG2Ipa7XH5cCpRToOgW6OwV3I4WD50+h7C+XWJ73SGJQ9TifDwmGBLvV1ZJ1cWtje1hdKbKgKfSNOVY5wZzdMluTw0637cR2e8OOENsxkIvtPnTommL7KrYmtllsd6LPFiQ5l2nnQOhQZg7l6grBhXbeNtibhKkENg22Hv5B/FHu3om/0y4TzixbwfDPsoRzGZtjbF4KBn8h/AXiBt/gQCsY/IEEW2CJm+VpbAB/kFgh49dQML+SkmNBCWccVzg9axY9BH4vPBZzQjIPjueh9QdP1vLApxCfAmOLVltI2PM8SO7Ec+sTJ5kUl8SfkK8X/R76vcTyiJVLrJxjic6C8xX9AZxlO595wjk4i5aT598l7Nux4A+iM4RrTjKlJtvwEO97rtGPXhM1/uiBxR81do2thX+WsHWCHey5+OfAheBCk9Qeek3ZypqWorOEHiN6DPQY8TfM38byK5iAfcJtzSNHMqLHQI8VPRZ6ZF0Ia5Qw/F2ZsNQ/emASDH5ZX/TQHxKnlRxRVyR1hR7+WfJvMesxbc2XCZecr/AbzrHl5/kXPcR6JBfUD8X6WfJuytvAZmx9bPO4PRS8if3iNqdYYLhjs+OkV3e1g6fvUg9K7VFz8P54Zf+erd/pqe5ifjo8HuFc2jr5OFrbnc2nwwn+dc+G5yOFr4NlR31T8cbp4HjQ/w+Gv/qDgZfKPPmz4YXemQfk9DDjOBPrPa3OF4PhALOt8G2qf2bHefFH7DjHH6Xzuez3xb1Pp8WB9LgH+BJ5Wbt/Dnv3Nn/R/+31jGOg3/kO",
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
