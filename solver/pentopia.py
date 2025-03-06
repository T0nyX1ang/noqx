"""The Pentopia solver."""

from typing import List

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape


def avoid_adjacent_omino(num: int = 5, color: str = "black") -> str:
    """
    Generates a constraint to avoid adjacent ominos.

    An adjacent rule, an omino rule should be defined first.
    """
    tag = tag_encode("belong_to_shape", "omino", num, color)
    return f":- adj_x(R, C, R1, C1), {tag}(R, C, T, _), {tag}(R1, C1, T1, _), T != T1."


def opia_constraint(r: int, c: int, mask: List[bool], lmt: int, color: str = "black") -> str:
    """Generate a constraint for opia-like puzzles."""
    m_t, m_l, m_b, m_r = mask
    cmp = f"N {'=' if m_t else '<'} N1, N {'=' if m_b else '<'} N2, N {'=' if m_l else '<'} N3, N {'=' if m_r else '<'} N4"

    top = f"top({r}, {c}, {r} - Mt) :- Mt = #max {{ R: grid(R, {c}), {color}(R, {c}), R <= {r} }}, grid(Mt, _).\n"
    top += f"top({r}, {c}, {lmt}) :- Mt = #max {{ R: grid(R, {c}), {color}(R, {c}), R <= {r} }}, not grid(Mt, _).\n"

    bottom = f"bottom({r}, {c}, Mb - {r}) :- Mb = #min {{ R: grid(R, {c}), {color}(R, {c}), R >= {r} }}, grid(Mb, _).\n"
    bottom += f"bottom({r}, {c}, {lmt}) :- Mb = #min {{ R: grid(R, {c}), {color}(R, {c}), R >= {r} }}, not grid(Mb, _).\n"

    left = f"left({r}, {c}, {c} - Ml) :- Ml = #max {{ C: grid({r}, C), {color}({r}, C), C <= {c} }}, grid(_, Ml).\n"
    left += f"left({r}, {c}, {lmt}) :- Ml = #max {{ C: grid({r}, C), {color}({r}, C), C <= {c} }}, not grid(_, Ml).\n"

    right = f"right({r}, {c}, Mr - {c}) :- Mr = #min {{ C: grid({r}, C), {color}({r}, C), C >= {c} }}, grid(_, Mr).\n"
    right += f"right({r}, {c}, {lmt}) :- Mr = #min {{ C: grid({r}, C), {color}({r}, C), C >= {c} }}, not grid(_, Mr).\n"

    rule = top + bottom + left + right
    rule += f"opia({r}, {c}) :- top({r}, {c}, N1), bottom({r}, {c}, N2), left({r}, {c}, N3), right({r}, {c}, N4), {cmp}.\n"
    rule += f":- not opia({r}, {c}).\n"
    return rule.strip()


class PentopiaSolver(Solver):
    """The Pentopia solver."""

    name = "Pentopia"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VZRb9NADH7vr0D3fA+53CW95K2MlZeyAS2aqiiqspCpFZ1Skmagq/rfZ/tSMliOdkhjQkLp2Y7t++w7O1brr01WFVx4+JOaA4dHCU3L1yEtr31mq+26iF/xUbNdlhUInF+Ox/wmW9fFIGm90sHORLEZcfM2TphgnPmwBEu5+RDvzLvYzLmZgolxBbqJdfJBPO/EK7KjdGaVwgP5opVBnIOYVVX5bZFXZV1b5fs4MTPOMNRrAkCR3ZZ3BWtTwfe8vL1eoeI628J56uVq01rq5nP5pWl9RbrnZmQznh4yxozajGWXMYo2Y5R6MsZtmHG+qvJ1sZg8Q7pRut/DzX+EhBdxgrl/6kTdidN4B/SCqCA6j3dMegDTVlAc6g0hfr1iprR1xDY5tEWvo/6B+MC1z1F4Aj1/AnR5yi74EcyhxTx6HiHDUz1VG/34iRRFP+GSRBh00X/jCVUaU618ojMoJTeS6BuiHtGA6IR8zoleET0jqoiG5DPEZjixXZhULFacScgVGB7OBxbRW+jTWwi3CGwISmAaKgo2DUpksAFYZFEiiyI86A/iFkAI0CP3LYRQrV7ZbSKwKCKABlSPO/iZbiiRh257+AT/ni4dJGzaVDdZXsD0mC6zTcFgUu8H7DujlUgc/P+H98sNb6yC98cj/GVGRAK3C58yN5ecbZpFtsjLNcMJhgY97NfDt+wyaIdBqSfuiBwbtHAAeb7DIIJ+wzDq14eh6wyuCL4DCf55PfHQjlSl4zKUI7B04ChH3cLHJ/vrfQqzOh3cAw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(avoid_adjacent_omino(num=5, color="black"))

        self.add_program_line(all_shapes("omino_5", color="black"))
        for i, o_shape in enumerate(OMINOES[5].values()):
            self.add_program_line(general_shape("omino_5", i, o_shape, color="black", adj_type=4))
            self.add_program_line(count_shape(("le", 1), name="omino_5", _id=i, color="black"))

        for (r, c, d, pos), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(pos, "multiple")
            symbol, style = symbol_name.split("__")
            style = int(style)
            validate_type(symbol, "arrow_cross")
            self.add_program_line(f"not black({r}, {c}).")

            # direction order: top, left, bottom, right
            mask = [bool(style & 64), bool(style & 128), bool(style & 16), bool(style & 32)]
            self.add_program_line(opia_constraint(r, c, mask, max(puzzle.row, puzzle.col) + 1, color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"black({r}, {c}).")
            else:
                self.add_program_line(f"not black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
