"""The Moon-or-Sun solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, defined, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_adjacent, area_border
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import count_area_pass, single_route
from noqx.rule.variety import classify_area


def moon_sun_rule(color: str = "white") -> str:
    """Genearate a constraint to make moon and sun areas appear in a sequence."""
    extra = f"area_pass_moon(A) :- area(A, R, C), moon(R, C), {color}(R, C).\n"
    extra += f"area_pass_sun(A) :- area(A, R, C), sun(R, C), {color}(R, C).\n"
    extra += ":- area(A, _, _), not area_pass_moon(A), not area_pass_sun(A).\n"

    constraint = ":- area_adj_line(A1, A2), sun_area(A1), sun_area(A2).\n"
    constraint += ":- area_adj_line(A1, A2), moon_area(A1), moon_area(A2).\n"
    return extra + constraint


class MoonSunSolver(Solver):
    """The Moon-or-Sun solver."""

    name = "Moon-or-Sun"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VdNTxsxEL3nVyCfffDnrr03SqGXFNpCVaFVFAVIS9SEUEIqtFH+e5+9s11QB1GqCqlStaz3ZcYzfn7+ZPVtPbmZSq3Snw0SXzxOh/yaUORX0XMyu51Pqx25u769XN4ASHl0cCA/T+ar6aCmWqPBpolVsyubN1UtjJD51WIkm/fVpnlbNaeyOYZLSA3bEEgLaQD3e/gp+xPaa41aAR8SBjwFXK2vxovl8qq1vKvq5kSK1M6rHJ2gWCy/T0Ubln+fLxdns2Q4m9yiM6vL2TV5VuuL5de16JrYyma3pTtk6Nqerv1J1/J0zd+gO59dTe84pnG03ULxD+A6rupE+2MPQw+Pq802UUqlzuVptRFWI42RD7kJa1irZ60FrPoXa+CszrHWkrN6y7XmI1e3UKyV7UXJMgusDqFgrSVr5fOyfCPLN2rWyvYisupEVt/oOatWLAmtWCW0MnxtlodWjjc/woSdQloFPklkzZrtuzbsAGir2CT8xNeW7w4/9bXjkzh2+WjPjrr27KLQ/EzXBT9oheVrM93BfnCQdwWTyxNsGrKxuXydS5VLn8thrrOP/cNoK40BV6QzGqdFEjbjCGxbbEppnG6xVcCOMGIdxTotjfeEHXAgjNiCYr0HjoRxOpWmxQViS4ot0G6gdkuTTi/CiA0UG9BupHZxullFnEMEpthYSqvbduEHdoQtcBsLv7TGE3bAgTBiLcUaDxwJB2ldyxl+YIq1aNe37cIPXBBGrCfOqGMc8XSq1zPpRjnxBSb+zvY6Jz1dpy10cKSJK+7pn8ao0xzauk4r5A+UP5he26RhoPwB+QPlD77XPN8eOp2RP1D+EO6NBfoVqV8R/YqdbtDZkObG9TonPQ3pYzB2NPfw7fVPOptOc2hLcxLfflyS/rYbC2ie5+o2neRpau/l0uWyyFO+TKfoH5+zz11dwhlwiwGHo7EEnExrwmaURtO2S/BJzrVtL3UPH//v2UaDWgxxDdo5XN4sJnNchvYvvtz7dXw5uZ4KXD+3A3En8lvbdJv9fyN9+RtpUl+92Hr5zaXwBJ0awtI6k82RFNfr8WR8vsTcgnadE0uPdxb4h4l1YC0/O8I+EmGf4XhxdbHXjAY/AA==",
        },
        {
            "url": "http://pzv.jp/p.html?moonsun/15/15/928i4h492940i814g28h2h25248g0h01208g0h01200000000vvv0000003vvs00000fvvg0000vvv0000001800jn33l000f6ig100109inb6i4003a3f00600fclh01i0910032f31ii290003631lk5ai100",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?moonsun/36/20/j4i9h8gikma8oi9sq9i8jcjq9j9j4s59i9jcsq9qojssi9qlriciaqbreak5a9q6d3jidp69ijid94fijj594hiikk94uijna9khii9i94oj9mi9p6kklj556b4pj4t6ccpj44294p3c0gc18ge7jr3no0guoe49vj1bs0301gfbuvf1fge70fe5403rr02vvvaeabgadtogs0ft007g1q1gho0fqg7nfvo1fs4mu21c05no0ve3uqsecuekivsrgtfvg1t00u0001fof03rg69n3j35i96013j16filk3ajffofbm57a76862kbi26b69bc9c340kb6a6jk04k7475fqk9398klk3k153l693cg4743f6a7n8ca8j26nkp83k2745olk3ap333fc9j13k7oik08glfmkc3d3660cb2f776443n5a415bj73ih60iin3cb3j52nf14a5k6a3fd27gfbk53ba5b9938kacgl6jp88g1i6239a60c832aalaj8a",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="moon"))
        self.add_program_line(defined(item="sun"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        fail_false(len(rooms) % 2 == 0, "The number of areas should be even.")
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            self.add_program_line(count_area_pass(1, _id=i))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "sun_moon__1":
                self.add_program_line(f"moon({r}, {c}).")
            if symbol_name == "sun_moon__2":
                self.add_program_line(f"sun({r}, {c}).")

        self.add_program_line(area_adjacent(adj_type="line"))
        self.add_program_line(classify_area([("moon", "white"), ("sun", "white")]))
        self.add_program_line(moon_sun_rule(color="white"))

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
