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
            "data": "m=edit&p=7VZrb9pIFP3Or6jma69Uj8dvKR9IQipFhIaFLJtYCE3ABCcGp34kkaP89955ULCBtOpqq9VqZfnOmXPH9zHGZ8i/ljyLgJpADWAeGEDxsnwLLOoBM115G/oaxkUSBR+gXRaLNEMA8OXsDOY8ySM4v74/Pn1oP3faf32ybxi76s0/3p/2r+5noz9p34g/ZUYv8VYXl6fHycfP1c3Fov0UdSLnMk+niyTiM17djM5fktWZd7eY05PzxYk35ysj/+oN/afj/tFRK9SFjFuvlR9Ubag+ByExCcibkjFU/eC1ugiqAVQDdBGwx0CWZVLE0zRJMyI5iuu6iCgBE2FnA0fSL9CJIqmBuKcxwmuE0zibJtGkq5jLIKyGQETuY/m0gGSZPkUiGT4m59N0eRsL4pYXuIf5In4kwNCRl7P0odRL6fgNqrbqoLvuAJO81wEGWXcgoOpAoD0diMb+2Q788dsbvpw/sIdJEIp2rjbQ28BB8EpsSgIbiG2qwVaDJwfHVYOauWqlq5ZQw9CjnlM9mioSZevR0qOKQi0VlNr6eV0A1amp7ajR0c+5ep1OT10RF4vvBa9oqbTX0p5Ja0o7xA6hYtKeSmtIa0vblWs62L5p2WA6GNrEn6/rgukziZlhAzOwFIFNxJZawyz8Qr9jhhjLFNh1gPlYmuTxg3V0HGYCYwqbPvJ0g00ft0Rg28AaRC4saiRLO5HWktaRJbvilf3kS/37u0M82yeB7+F+ex5QDydM7D3TWO3eD8sNmSWlbPey/5v8uBWSQZnN+TTCL7Ybr6IPvTRb8gRnndnd9xlqJ8nTZJKrtZPohU8LEigN3/bUuFW5vI1QfLaoJE0fE0yzJ8LaVSPju1WaRXtdgoywxgOhhGtPqNs0mzVqeuZJUu9Fnm81SolfjSoyVLatOc+y9LnGLHmxqBFbKliLFK0am1nweon8gTeyLTfb8dYiL0TeIQM8k/8/6P7VB514UcZvU8afVL4flBPihuM5AXgIQvUFyGM54RPccYJ/q2DtZPavOg+HpZ6LEu79mhsPhYPPqVPikFsfHDvu3/5a5LeeZu8I78bZpPfIL7LvKPCWdx9/QGy3vE1+R1lFsbviiuwefUW2KbFI7aoskjtCi9wBrRVRm3Irqmoqrki1I7oi1bbuhuPWNw==",
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
