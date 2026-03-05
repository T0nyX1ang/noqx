"""The Nurimaze solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, display, fill_line, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_same_color
from noqx.rule.reachable import border_color_connected, grid_color_connected
from noqx.rule.route import single_route
from noqx.rule.shape import avoid_rect


class NurimazeSolver(Solver):
    """The Nurimaze solver."""

    name = "Nurimaze"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZbfbyI3EMff+StOfvbD2mOvvbyl1/ReuFzb5FSdEIoIxzWoUFIC1Wkj/vd+xzvDBoX7lUpVK1WEzRfvd+wZmI/X93/sppu5dRX/Ubb4j1dwubx9rsu7ktfVYrucD1/Ys932dr2BsPbNhf0wXd7P7WAsrsngoW2G7ZltXw3HxhlrPN7OTGz70/ChfT1sz217iVvG5ok1q91yu5itl+uNKWMOvlEX6CHPe/lLuc/qZTfoKugL0ZDvIGeLzWw5vx51Iz8Ox+2VNbz2dyWapVmt/5wbyY0/z9armwUP3Ey3KPD+dnFnLOHG/e79+red0RX2tj3rKhhpBf7zFVBfAR0qoNMV+OMKXj+rguXi9/nHE8k3k/0ev8vPSP96OOZK3vYy9/Jy+LDnjB5Mzhx6iSy6H8+4KvHIKx2BzxX3O7ipxj2MbzeL3Z3kbmLuBo8qMimfsDoKp0ZDODWDi6dWc3V8Morsfig5+nK9QpG2pXL9vlyrco3lOiqec1TjnbfeYxGP5nUEnUQH6Cw6QjeiwQlVohO0Ew2GyItuoKnTHv4gfg9/EL+HP4jfwx/ETxV0EO2go2jkGSRPQp5B8iTkGSTPgNgosQGxUWID/FH8Af6oftQVpa6APGvJMyDPWvKM8NTiifAk8UR4knpQS5JaImpJUkuNfJLkUyOfJPnUqCVJLTXvPRKb4M/iT/Bn8SfPe5No1JKlloTcsuSW4WnEk+FpxJNRbyP1Zvgb9deWKqklJ2ipJWdoySc30FJLg02zktwaxDqJbRDrJLZBrJPYBrGui8U60EG0g46iPXQtmqCT6ADd5Uy8WXuJRa+S9CrmhhY/epW8+pGb9Cfmg+5ywxzQ4vERuhENT1AP8peeJPQkSU9iPmjJAT1J0pOEniTpScxtKUosITZKLHqSpCexDrTEBsRGiUV/kvQn1oGWPNGfJP2JdSxpf/rYM8t8KbPMlzLLfCmzzJRyykwpp8yUcspMkXKHniHlrun5Zb6UX+ZL+Q2+55dZU36ZL2WW+VJmA7OvTFHPbAw9s8ydfD+FO+WXWVNmmS/llPmqfc9XrQwyy7lnTVlm1pRfZk35Zb6U2RR6Zpk1ZTa7nlnmLlPPnfLL3Cm/zJ3yW84ZyiZyy8pmfsQyvvNG+UKejfKVepaZL+G38CX8Fr6E38JUpdyhryrlrjnwW/gSfvH/wG9hTfll1pRfZk35xXPhwC9zp/wydwd+eU9Q1pjT2DOoLKOHDywzg179Tc8yc0fKF3IjZTP1XDN30quFO+WauVOumTvlmllTlpmv0p97Przw4/FluYZyrctjM/HJ4SvPFkYg4L7K3UHj8THiWx/XmM7ytkDdc/uLSY6pO98ev+J/b2wywNFst/kwnc1xAhzh0PfiYr1ZTZf4dP7+10efLnarm/mm/3x5O72bG5zR9wPz0ZT3GIDylP8f2/+dx3b+japvOrz/Haa+EqUvpDNuL0Gmbd9Yc7e7nl7jey5fFY8D2uNx+sR46MafzBO7cRwAj8frT8xT1h3ZGjvq8Y2qC8AOeTKhJ+PhsxONrOxHz7oZLR7gz7p5etp/vCGwvU4GfwE="
        },
        {
            "url": "https://puzz.link/p?nurimaze/10/10/vvvvvtv6rtlrvrvvvuvtvrvvvvvvrnvv7fvve3m3845394c3c2k4946371a46",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false("S" in puzzle.text.values() and "G" in puzzle.text.values(), "S and G squares must be provided.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(colors=["gray", "white", "empty"]))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(area_same_color(color="gray"))
        self.add_program_line(border_color_connected(puzzle.row, puzzle.col, color="gray", adj_type=8))
        self.add_program_line(avoid_rect(2, 2, color="gray"))
        self.add_program_line(avoid_rect(2, 2, color="not gray"))
        self.add_program_line(grid_color_connected(color="not gray", adj_type=4))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(single_route(color="white", path=True))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if clue == "S":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"dead_end({r}, {c}).")

            if clue == "G":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"dead_end({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__1":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"white({r}, {c}).")

            if symbol_name == "triup_M__1":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"not white({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="gray"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
