"""The Rassi Silai solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Point, Puzzle
from noqx.rule.common import area, count, defined, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_border, avoid_same_color_adjacent
from noqx.rule.reachable import area_color_connected
from noqx.rule.route import count_area_pass, single_route


class RassiSilaiSolver(Solver):
    """The Rassi Silai solver."""

    name = "Rassi Silai"
    category = "route"
    aliases = ["rassisilai"]
    examples = [
        {
            "data": "m=edit&p=7VZrT9tIFP3Or0DztSOtZ+zED2k/hDRh2w0hFBBLrCgywYCpjVk/gDXiv/fMwyR2TNvtaqv9sLIyOj73zuMeXx8n/7MMspA6uEyHGpThMi0uf9xw5c/Q10lUxKG3SwdlcZNmAJQejsf0KojzkH48v5kM08Hj+8EfD04xn7N9o/xgnN2Ob999Sn7/EJkZG0+d2cHsIOLXg9+Ge0f90bv+rMxPi/DhKGF7t6fzk6vZ2bXL/xpN51Y1PzR6H+dXvzwMTn/d8fUZFjvPletVA1rtez7hhMofIwtaHXnP1YFXjWh1jBChbEFJUsZFtErjNCM1V02AGKEccLSGZzIu0FCRzACeagx4DriKslUcLieKmXl+dUKJ2HtPzhaQJOlDKDbDNHm/SpOLSBBZkOdRHsVxEBFqIpKXl+nnUueyxQutBqqEyfeUYMlF6hIEVCUI1FGCqOxfLsFdvLzg8XxCEUvPF/WcrqGzhsfeM3EZ8SzgqfeMkcnxXI5jOXI5nmACrUw5vpejIceeHCcyZ4TVmI3GdTjxOHrB7gHbGveBHYUdTplraWwC9zRGvqvzHRvY1dhB8xsKuxZwX2JwlDO1FzhgtT44yrlaHxzlpprLOfJNnc+RY+ocbgKrMyCXckvnmMixdI7ZA1ZnQ5zynj6/qNeGhBLjlbXr2lGjbWqMGu063wLW9Qp9bFWL1MGpNUGOo3NQ76s+rtBEa+g6r/rIGlmNYRS8rlfooM4ga6w14dCQ1/UKHXSOKXSo60VOrYkFbNVY6KD1t6C51oS5wIY4GxrhTLbDUI6WHPuyTWzRdd/Zl9sdSRhDXT6jJH1a7uv39G/1KLGEYlCOCPXEaqZq22+e2edo38aFR/cz7xc7Pjkus6tgFcIKJtFduDtNsySIcTe6vN64G6bJfZpHRUjg0CRP42Wu5i3Dp2BVEE99JDYjDe6uTC5CONwGFafpfYwtO1aoQw0yur5Ls7AzJMgQ531jKRHqWOoizS5bZ3oM4rhZi/x8NijlsA2qyGCfG/dBlqWPDSYJipsGcREU+NjmN9F9c6XwriVmETSPGHwOWrslazledsgTkT8fb514wP9/Tv/Tn1PxqIwfNq8f+5z+Uy/10TSv1kyrQ0ruy2WwhOgEf+DoN8PnwiVbAejt40HWFto9re90zergobVfHW/z1ht8T+0OI9/a+KdrL1/pNPuKv66DbbrDZcF+xWg3ol38G566EW3zWwYqDrvtoWA7bBRs20lBbZspyC0/BfeGpYpV264qTtU2VrHVlreKrTbtVb/Uu3ir8VIvdr4A"
        },
        {"url": "https://puzz.link/p?rassi/10/10/40a74aa64cki6kd0800u700v30oc3if00u3v00010100000000000000", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="dead_end"))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="grid", path=True))
        self.add_program_line("ox_G__1(R, C) :- dead_end(R, C).")
        self.add_program_line(area_color_connected(color="grid", adj_type="line"))
        self.add_program_line(avoid_same_color_adjacent(color="dead_end", adj_type=8))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            self.add_program_line(count_area_pass(0, _id=i))

            if len(ar) == 1:
                fail_false(
                    puzzle.surface.get(Point(ar[0][0], ar[0][1], "center", "normal")) in Color.DARK,
                    "Single-cell area must be a hole.",
                )  # compatible with puzz.link
            else:
                self.add_program_line(count(2, color="dead_end", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(symbol_name, "ox_G__1")
            self.add_program_line(f"dead_end({r}, {c}).")

        for (r, c, d, _), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="ox_G__1", size=2))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
