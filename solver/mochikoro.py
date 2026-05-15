"""The Mochikoro solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, invert_c, shade_c
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, grid_color_connected
from noqx.rule.shape import all_rect, avoid_rect, count_rect_size


class MochikoroSolver(Solver):
    """The Mochikoro solver."""

    name = "Mochikoro"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVNb5tAEL3zK6I5z4H9AJO9VM6He3GdtnYVRQhZmBLFKhYuNlW1Fv+9swMxceRIjVq5UhXBPr15u8y+Hdhl871OqxyFcLeK0EdiqIOQmxCSm99ds+W2yM0ZDuvtQ1kRQbwZjfA+LTa5F3ejEm9nz40don1vYhCAIKkJSNB+Mjv7wdgJ2il1AWrSxu0gSfS6p7fc79hlKwqf+KTjRO+IZssqK/L5uFU+mtjOENw8F/y0o7Aqf+TQ+XBxVq4WSycs0i0tZvOwXHc9m/pr+a2GxykatMPW7vSIXdXbVXu76rhd+VfsFuvymNHzpGmo4J/J6tzEzvWXnkY9nZpd4xztIPDpUXq37TuBQB2GoUusYS+ELLzrhUFEgt6HwhcUqz6W6jDWzzOKMDqYUgxchuhJrJ/E5Fqw9zvGEaNknNHS0CrGK0afMWAc85hrxlvGS0bNGPKYgSvOb5YPlASjERStT7a1PIG3WEneks+v4P9VEy+GaV3dp1lOX/ykXi3y6mxSVqu0ADpcGg9+Ajf+yvTbeXPy88YV33/VqfPvd3FMdaW9ZG8Q1vU8nWdlAfSzQtbVC/pL41+b58/zn7yadPQk3i8=",
        },
        {
            "url": "https://puzz.link/p?mochikoro/22/13/4l2k4m3w4p5h1n2x2v4i2h4k2h5p2k4m5j4q2t2u3n4g4l3o4o2n2j2zk2g1n1o",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(invert_c(color="black", invert="white"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="not black", adj_type=8, grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="black"))
        self.add_program_line(all_rect(color="white"))

        all_src: List[Tuple[int, int]] = []
        tag = tag_encode("reachable", "bulb", "src", "adj", 4, "not black")
        fail_false(len(puzzle.text) > 0, "No clues found.")
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="not black"))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_rect_size(num, (r, c), color="not black"))

            all_src.append((r, c))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
