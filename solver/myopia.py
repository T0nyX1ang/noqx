"""The Myopia solver."""

from typing import List

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import direction, display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import convert_direction_to_edge, single_loop


def opia_constraint(r: int, c: int, mask: List[bool], lmt: int) -> str:
    """Generate a constraint for opia-like puzzles."""
    m_t, m_l, m_b, m_r = mask
    cmp = f"N {'=' if m_t else '<'} N1, N {'=' if m_b else '<'} N2, N {'=' if m_l else '<'} N3, N {'=' if m_r else '<'} N4"

    top = f"top({r}, {c}, {r} - Mt) :- Mt = #max {{ R: grid(R, {c}), edge_top(R, {c}), R <= {r} }}, grid(Mt, _).\n"
    top += f"top({r}, {c}, {lmt}) :- Mt = #max {{ R: grid(R, {c}), edge_top(R, {c}), R <= {r} }}, not grid(Mt, _).\n"

    bottom = f"bottom({r}, {c}, Mb - {r}) :- Mb = #min {{ R: grid(R, {c}), edge_top(R + 1, {c}), R >= {r} }}, grid(Mb, _).\n"
    bottom += f"bottom({r}, {c}, {lmt}) :- Mb = #min {{ R: grid(R, {c}), edge_top(R + 1, {c}), R >= {r} }}, not grid(Mb, _).\n"

    left = f"left({r}, {c}, {c} - Ml) :- Ml = #max {{ C: grid({r}, C), edge_left({r}, C), C <= {c} }}, grid(_, Ml).\n"
    left += f"left({r}, {c}, {lmt}) :- Ml = #max {{ C: grid({r}, C), edge_left({r}, C), C <= {c} }}, not grid(_, Ml).\n"

    right = f"right({r}, {c}, Mr - {c}) :- Mr = #min {{ C: grid({r}, C), edge_left({r}, C + 1), C >= {c} }}, grid(_, Mr).\n"
    right += f"right({r}, {c}, {lmt}) :- Mr = #min {{ C: grid({r}, C), edge_left({r}, C + 1), C >= {c} }}, not grid(_, Mr).\n"

    rule = top + bottom + left + right
    rule += f"opia({r}, {c}) :- top({r}, {c}, N1), bottom({r}, {c}, N2), left({r}, {c}, N3), right({r}, {c}, N4), {cmp}.\n"
    rule += f":- not opia({r}, {c}).\n"
    return rule


class MyopiaSolver(Solver):
    """The Myopia solver."""

    name = "Myopia"
    category = "loop"
    examples = [
        {
            "data": "m=edit&p=7VVRb9owEH7Pr6j8fA92HCDxG+tgLx3dBlOFrChKaTbQQGEJ2SYj/nvPF0O0rSVRq3V7mEw+fdgf9nfnO1J+rdIigwiHDIGDwCFDTk8Y2A93Y7barTN1AcNqt8wLJADX4zF8Stdl5mmnir29iZQZgnmjNJMMmMDHZzGY92pv3iozBzPFJQYC566QocBHOmroDa1bdllPCo584jjSOdK0KPLvyaLIy7KefKe0mQGzR72iDSxlm/xbxupf0vdFvrld2YnbdIfxlMvV1q2U1V3+pXJaER/ADGvHowccy8axpbVjyx5wbAP5846j+HDA5H9Az4nS1v7HhoYNnao94oRQEM7VnvkRboOXaK9fHK8cj/jVM5OBFdaS88JeR2HgdjyJHhW6HVuF/cHx6JZgBv5xxzYhHd0hPaHs6DHqNx7PCgXnHbcUXHRWUobqs8/GI7grjNZcCkGnd1FKSvtPuseUVBudlKcCPhsRlvuYit4nnGFPgJGErwk5YY/wijQjwhvCS8KAsE+age2qJ/fd0+ywXoAZjEIMO5QgbCnJVovaD135NqP3b83Enmaju8/ZxSQvNuka/+Wmy3SbMXypHDz2g9GjMWII/r9n/up7xl4Ef+Gqf24TakzwqWHAXAPbVkmaLHIsNMzi85exK39bePEcYKPH3j0=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(direction("lurd"))
        self.add_program_line(shade_c(color="myopia"))
        self.add_program_line(fill_line(color="myopia"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="myopia", adj_type="loop"))
        self.add_program_line(single_loop(color="myopia"))
        self.add_program_line(convert_direction_to_edge())

        for (r, c, d, label), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(label, "multiple")
            symbol, style = symbol_name.split("__")
            style = int(style)
            validate_type(symbol, "arrow_cross")

            # direction order: top, left, bottom, right
            mask = [bool(style & 64), bool(style & 128), bool(style & 16), bool(style & 32)]
            self.add_program_line(opia_constraint(r, c, mask, max(puzzle.row, puzzle.col) + 1))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_top", size=2))
        self.add_program_line(display(item="edge_left", size=2))

        return self.program
