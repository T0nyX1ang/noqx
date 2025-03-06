"""The Tasquare solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import (
    count_reachable_src,
    grid_color_connected,
    grid_src_color_connected,
)
from noqx.rule.shape import all_rect


class TasquareSolver(Solver):
    """The Tasquare solver."""

    name = "Tasquare"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVBj9o8EL3zK5DPc4gTJ4Tc6H5LL5RtG6oViiIUaFaggsIHpKqM+O87M07XdGParqrlUFXg0cyzPX5+Hsf7/+tiV4KU9A9i8AA9UGHETUqfm9f8JqvDuky6MKgPy2qHDsDdcAgPxXpfdrJmVN456n6iB6DfJpmQAoSPTYoc9IfkqN8legw6xS4BCrGRGeSje2vde+4n78aA0kN/3PjoTtE15Gcjg7xPMj0BQeu84dnkik31tRQND4oX1Wa+ImBeHHAz++Vq2/Ts68/Vl7oZK/MT6IGhmzroBpYuuYYueQ66tIs/p7veVi6i/fx0QsE/ItVZkhHrT9aNrZsmR7Tj5CiCmKZ2kYU5FaH8Z0BEQGjDCEMshibseRiqp7CvMAxsSNntXOlRLjta+hRjVT3FlNxOlwFlP4tDSm8XlyHlP+tnrmf54+ebkTGtYBFUQbIW0+9aIP7D0RhBWiiv1EYpewtljVooS9VGnRyMcG2Y9XPAThpGzTbMojpgNxP3xo3SDtjBBNUesuY+2wmWJOiA7X9sPbYh2xGPuWV7z/aGrWIb8ZgeFfVvlr1QuC2FJ4Wb9s0dOK+BV+KWBVTk7R9djb8UzTuZSOvdQ7Eo8Us1rjfzctcdV7tNscY4XRbbUuDjcOqIb4Ib32P17724+ntB4nsvejWucGN+QSfTUwhC0HcgtvWsmC0qrCpU7We46r8mnoKKL+A9Nx4EF3DfjUfqhfkv5HGse/XTxU+iOBSmpkXeeQQ=",
        },
        {
            "url": "https://puzz.link/p?tasquare/21/15/g.k..k4k.x.h.i8j2q.u4i2l2jar.2l.h.zhak8i8h9j2.x1m.n2g.h.l.j2h3g1k2g4r.o1i3h.i.j.l1zj2g4i..g.i.h./",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(all_rect(color="black", square=True))

        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color="black"))
                self.add_program_line(count_reachable_src(num + 1, (r, c), color="black"))
            else:
                self.add_program_line(count_adjacent(("gt", 0), (r, c), color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"black({r}, {c}).")
            else:
                self.add_program_line(f"not black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
