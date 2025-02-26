"""The Canal View solver."""

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        solver.add_program_line(f"not black({r}, {c}).")
        if isinstance(num, int):
            solver.add_program_line(bulb_src_color_connected((r, c), color="black"))
            solver.add_program_line(count_reachable_src(num + 1, (r, c), main_type="bulb", color="black"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")
        else:
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display())

    return solver.program


__metadata__ = {
    "name": "Canal View",
    "category": "shade",
    "aliases": ["canalview"],
    "examples": [
        {
            "data": "m=edit&p=7VRNj5swEL3zK6I5+4CNSYgvVbrd9JLSj6RarRBaEcpqUUnZkrCtHPHfMzOw66TKoVKlVQ6V46f3Zib4eQze/myzphBTHEEkfCFxBJHPM9L084exKndVYUZi1u4e6gaJEB/nc3GfVdvCS4aq1NvbqbEzYd+bBCQIUDglpMJ+Nnv7wdhY2CWmQGiMLfoihfTa0RvOE7vqg9JHHg8c6S3SvGzyqrhb9JFPJrErAbTOW/43UdjUTwUMPkjn9WZdUmCd7XAz24fycchs22/193aolWkn7Ky3uzxjN3B2ifZ2iZ2xS7v4d7vVY33O6DTtOmz4F7R6ZxJy/dXRyNGl2UOowWgBYQhGYSjGkIrwOSEeOB8QBArl2MkxyuBFasoeycmJnFBWvcjIP3lUhGsn8Ab3/hyglV1+erqUVPIPTXntNDs9yrNVtxGpaflnjZuVZo94yzhnVIwrbI+wAeM7Rp8xZFxwzTXjDeMVo2Ycc82EGvyXR9B3/RXsJCri7/h4UDcuKJJ6CSzb5j7LC3yx43azLppRXDebrAK8QzoPfgNPPmb9/1p59WuFmu9f2pt9aXbwW4M8+5FVo6ey+AWpdwA=",
        },
        {
            "url": "https://puzz.link/p?canal/17/17/r11q33h33m31h13m31h16q42q16u81z14u21q21u43z16u31q31q62h41m54h31m12h15q21r",
            "test": False,
        },
    ],
}
