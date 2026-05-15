"""The Pentopia solver."""

from typing import List

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, avoid_same_omino_adjacent, count_shape, general_shape


def opia_constraint(r: int, c: int, mask: List[bool], lmt: int, color: str = "black") -> str:
    """Generate a constraint for opia-like puzzles."""
    m_t, m_l, m_b, m_r = mask
    cmp = f"N {'=' if m_t else '<'} N1, N {'=' if m_b else '<'} N2, N {'=' if m_l else '<'} N3, N {'=' if m_r else '<'} N4"

    rule = f'opia({r}, {c}, {r} - Mt, "{Direction.TOP}") :- Mt = #max {{ R: grid(R, {c}), {color}(R, {c}), R <= {r} }}, grid(Mt, _).\n'
    rule += f'opia({r}, {c}, {lmt}, "{Direction.TOP}") :- Mt = #max {{ R: grid(R, {c}), {color}(R, {c}), R <= {r} }}, not grid(Mt, _).\n'
    rule += f'opia({r}, {c}, Mb - {r}, "{Direction.BOTTOM}") :- Mb = #min {{ R: grid(R, {c}), {color}(R, {c}), R >= {r} }}, grid(Mb, _).\n'
    rule += f'opia({r}, {c}, {lmt}, "{Direction.BOTTOM}") :- Mb = #min {{ R: grid(R, {c}), {color}(R, {c}), R >= {r} }}, not grid(Mb, _).\n'
    rule += f'opia({r}, {c}, {c} - Ml, "{Direction.LEFT}") :- Ml = #max {{ C: grid({r}, C), {color}({r}, C), C <= {c} }}, grid(_, Ml).\n'
    rule += f'opia({r}, {c}, {lmt}, "{Direction.LEFT}") :- Ml = #max {{ C: grid({r}, C), {color}({r}, C), C <= {c} }}, not grid(_, Ml).\n'
    rule += f'opia({r}, {c}, Mr - {c}, "{Direction.RIGHT}") :- Mr = #min {{ C: grid({r}, C), {color}({r}, C), C >= {c} }}, grid(_, Mr).\n'
    rule += f'opia({r}, {c}, {lmt}, "{Direction.RIGHT}") :- Mr = #min {{ C: grid({r}, C), {color}({r}, C), C >= {c} }}, not grid(_, Mr).\n'

    rule += f'opia_all({r}, {c}) :- opia({r}, {c}, N1, "{Direction.TOP}"), opia({r}, {c}, N2, "{Direction.BOTTOM}"), opia({r}, {c}, N3, "{Direction.LEFT}"), opia({r}, {c}, N4, "{Direction.RIGHT}"), {cmp}.\n'
    rule += f":- not opia_all({r}, {c}).\n"
    return rule


class PentopiaSolver(Solver):
    """The Pentopia solver."""

    name = "Pentopia"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VRfb9MwEH/Pp0B+9kP8J46TtzJWXgoD0mmqoqrKQqZWdEpJGkCu+t05n9MFWL0VpDEhIcd3l7vL7+58zrWfu6KpKAvtIzQFDksyjZtrhTvs13S1XVfpCzrqtsu6AYHSi/GY3hTrtgry3mse7EySmhE1r9OcMEIJh83InJr36c68Sc2MmgxMhErQTZwTB/F8EK/QbqUzp2QhyG97GcQZiEXT1F8XZVO3rVO+S3MzpcSGeokAViS39ZeK9KnY97K+vV5ZxXWxhXra5WrTW9ruY/2pI4coe2pGLuPskDEfMhZDxuIuY3E8Y95nXK6acl0tJk+QbjLf7+HkP0DCizS3uV8Ooh7ELN3tbV6WMqSzdEdECDB9B9mh3xDi1yMmUjtHNrgdd9R3iOxhRBYy6/kToM9TDMEfwYwd5qP1MKFO9ZTi1IpkfOIhMRUN0R/whC6NsVcc6RRaSY1A+gppiDRCOkGfc6RXSM+QSqQKfWJ7GU68LkRIkkpKRITMFseBJfimOL4phSxOkGmGNq0ci5ElDiVxKCwMe+4AGIsc5w6CyV4v3WcsinsOF1Dev8FPdEK5ONy2H1f07+nmQU6yrrkpygqmR7YsNhWBSb0PyDeCOxd28P8f3s83vG0Xwj8e4c8zInI4XfiVqbmgZNMtikVZr4mdYNag4+N6+Jd9Bu0xSPmbXySeDzTzAIXcY2DRcUOcHNcr5avBF4F7kLQPyVu0J1XhOQzpCSw8ONLTN3W/sr9+T2FWz4Pv",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(avoid_same_omino_adjacent(5, color="black", adj_type="x"))

        self.add_program_line(all_shapes("omino_5", color="black"))
        for i, o_shape in enumerate(OMINOES[5].values()):
            self.add_program_line(general_shape("omino_5", i, o_shape, color="black", adj_type=4))
            self.add_program_line(count_shape(("le", 1), name="omino_5", _id=i, color="black"))

        for (r, c, d, label), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(label, "multiple")
            symbol, style = symbol_name.split("__")
            style = int(style)
            validate_type(symbol, "arrow_cross")
            self.add_program_line(f"not black({r}, {c}).")

            # direction order: top, left, bottom, right
            mask = [bool(style & 64), bool(style & 128), bool(style & 16), bool(style & 32)]
            self.add_program_line(opia_constraint(r, c, mask, max(puzzle.row, puzzle.col) + 1, color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
