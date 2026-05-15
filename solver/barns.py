"""The Barns solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.route import crossing_route_connected, single_route
from noqx.rule.variety import straight_at_ice


class BarnsSolver(Solver):
    """The Barns solver."""

    name = "Barns"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VXdb9MwEH/vXzH5+R78GTt5K6PlpWxAi9AURVXWZSwiJSNtEHKV/53zR1ekUTYNMSGELN/9fF/2nePL5ktfdhUwDoyCMECB4ZCpBMkMCK79pHEs6m1TZScw7rc3bYcA4Hw6heuy2VQwyqNZMdrZNLNjsK+ynHACfjJSgH2b7ezrzM7BzlFFQBVA1n2zrVdt03bEyxjazRAxAhzh5AA/eL1Dp0HIKOKziBFeIFzV3aqplrMgeZPldgHE7f3CeztI1u3XigQ3v16168vaCS7LLWa4ualvCQhUbPqr9lNP9jsMYMchg9k+A/brDMQhA3GXgfh5BvyPZ5AWw4CX8w5zWGa5S+f9AZoDnGc7ohjJFBDFA1OBGc8SHVhY6WCpgwmjNPK4ZpHzEImJPZeRhyhMhqBMRf94ABa3ZioJPIl+OtrF7Zl2cQdXzR1S5umFp1NPuacLzBCs8PSlp9RT5enM20wwfS4V8ARDc/x8tQaeCo8FVSBoEjBHLIONkPQHLBDLgHUCIuVRjs8piXEEByEC5inK2QHz1ASsKJ7B7TW4T8cd7dRT6Wnij6zdlT3yUn+/OsSolGSpwXobA8zgQrjai4hD9R48bi6kbzT3h/o35cUoJ/O+uy5XFb7YWf25Ojlru3XZ4Gpy9fFuhb1zGJFvxM9cAHeu/9vpX9xO3UXRZ3t/j3xfDxwnx4JjNwJstWDPgdz2y3KJFSf484a9UqinKo+HZUZjozBPU2PrOeoXetExdWxP99TPfi3Y+YrRdw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="grid", crossing=True))
        self.add_program_line(crossing_route_connected(color="grid"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color == Color.BLUE, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"ice({r}, {c}).")

        self.add_program_line(shade_c(color="crossing", _from="ice"))
        self.add_program_line(straight_at_ice(color="grid"))

        for (r, c, d, _), draw in puzzle.edge.items():
            if d == Direction.TOP and r > 0 and draw:
                self.add_program_line(f':- line_io({r}, {c}, "{Direction.TOP}").')

            if d == Direction.LEFT and c > 0 and draw:
                self.add_program_line(f':- line_io({r}, {c}, "{Direction.LEFT}").')

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
