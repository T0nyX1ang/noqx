"""The Moon-or-Sun solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, defined, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs, validate_direction
from noqx.rule.loop import count_area_pass, single_loop
from noqx.rule.neighbor import adjacent, area_adjacent, area_border
from noqx.rule.reachable import grid_color_connected


def moon_sun_area() -> str:
    """
    Genearate a constraint to determine the area of the moon or sun.
    A sun area should only contain sun cells, and a moon area should only contain moon cells.
    A sun area should be adjacent to a moon area, and vice versa.

    A grid fact and an area adjacent rule should be defined first.
    """
    rule = "{ sun_area(A) } :- area(A, _, _).\n"
    rule += ":- sun_area(A), area(A, R, C), sun(R, C), not moon_sun(R, C).\n"
    rule += ":- sun_area(A), area(A, R, C), moon(R, C), moon_sun(R, C).\n"
    rule += ":- not sun_area(A), area(A, R, C), sun(R, C), moon_sun(R, C).\n"
    rule += ":- not sun_area(A), area(A, R, C), moon(R, C), not moon_sun(R, C).\n"

    extra = "area_pass_moon(A) :- area(A, R, C), moon(R, C), moon_sun(R, C).\n"
    extra += "area_pass_sun(A) :- area(A, R, C), sun(R, C), moon_sun(R, C).\n"
    extra += ":- area(A, _, _), not area_pass_moon(A), not area_pass_sun(A).\n"

    constraint = ":- area_adj_loop(A1, A2), sun_area(A1), sun_area(A2).\n"
    constraint += ":- area_adj_loop(A1, A2), not sun_area(A1), not sun_area(A2).\n"
    return rule + extra + constraint


class MoonSunSolver(Solver):
    """The Moon-or-Sun solver."""

    name = "Moon-or-Sun"
    category = "loop"
    examples = [
        {
            "data": "m=edit&p=7Vddb9s2FH33rzD4zAfxQxKlt6xL9uKl25KhCATDcFpvMeZEWRwPhYL8955zRc8tfIu2GxBgwGCLOr4kLw8P7yXp7Z+75cPKuoLfkCze+ESX5PGpkqfIn8v142bVTu3J7vGmfwCw9vXZmf1tudmuJl1uNZ88DU07nNjhh7Yz3lh5nJnb4ef2afixHa7scIEqYx1sMyBnrAc8PcA3Uk/0ajS6Avg8Y8ArwO3ubnHb93ej5ae2Gy6t4TjfSW9Cc9v/tTJjN/n9tr+9XtNwvXzEZLY36/tcs9296//Y5bZu/myHk5HuTKEbDnQJR7pECl3O4l/T3azvVu81ps38+RmK/wKui7Yj7V8PMB3gRfuE8lxKJ+VV+2SCgxtPlx9xM8Gr1lK1VrC6I2vSrDGq1lqzlkEbrWy0tlWhWtVZ1CqzpOqQOLdjK/keW3W/Kt9G5duQw7FVnUWjqtOo+jZctyOrK1QSrlCVcAVpKK1VHq4gEcX8GSZqCLmCiipOKOmx2alzd15dABc4+WMneuC7oE9HD30XdSdRTR9XqqvuSjUpnB7prtIXreLqKK2V6WA/OJNdwUt5iU3DDkHK76UspCylnEmbU+wf3gXrPbjCnXc4LSis4AYYwxP72voIhsShAMb4gtGXyU8cnfUlFBIcgbH4gtGXsyMuS2Csp2CcTjWEJq7Qt859K4yb8ri15+mVMfoyGYkTxm3yuDjdAjNBcAOc+za1DW4cF/XAI2fUA499UW+DH8dFPfDIGfU2cGMl9iXwOC7qbWBwEAf0ZUQIxrjc7oijBx45ox44c0YbHzPPSA2zJtQt+8QbOPOP1DbrTD3zWHgDZ00i1utv/blGe82hbdxrBf8p+0/UM/unhin7T/Cfsv9EnbN/uT3sdYZ/bpGCebPY+8e8uB2K5pgXN0HRCjr7rLmntlkr6umzPh5rl2MP74P+1Jl5Lxja5pjE+7Au1J/ZLhiaS6wiqN9IaL+SMkpZScjXPEX/8Tn7rdlloge3JuFw9CAmIFrmRBDE1QxjCn6Rc4dp81L36af879nmk87McA2anvcPt8sNLkOn737/6NfFzfJ+ZXD9fJ6Y90aeLvA2+/+N9OVvpFS/eLF8+cpU+AKdDsLmPLPDa2vud4vl4m2P2IJ2+0qknl5Z4Q+TWoFc/uYe4TM9cGR+dcWLq4u9BuHS3037hylCy8wnHwA=",
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
        self.add_program_line(direction("lurd"))
        self.add_program_line(shade_c(color="moon_sun"))
        self.add_program_line(fill_path(color="moon_sun"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="moon_sun", adj_type="loop"))
        self.add_program_line(single_loop(color="moon_sun"))

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

        self.add_program_line(area_adjacent(adj_type="loop"))
        self.add_program_line(moon_sun_area())

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_direction", size=3))

        return self.program
