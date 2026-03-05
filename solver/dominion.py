"""The Dominion solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected
from noqx.rule.variety import nori_adjacent


class DominionSolver(Solver):
    """The Dominion solver."""

    name = "Dominion"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VQ9T8MwEN3zK5DnG2I731sJLUsplBZVKIpQWoKIaBVIGoRc5b9zvgQCURcGoENl+enl3dl+OctXvlRJkQKXwF2QHpjAcdhSgONZqHk0zXbMs+06DU5gUG0f8wIJwOVoBA/JukyNqM2KjZ3yAzUFdR5EjDNgAidnMahpsFMXgZqAmmGIAUdt3CQJpMOOLiiuWdiI3EQ+aTnSW6SrrFit07txo1wFkZoD0+ec0mpN2SZ/TVnrQ3+v8s0y08Iy2eLPlI/Zcxspq/v8qWIfR9SgBo3d2R67srMrP+3K/XbF79v147rGsl+j4bsg0t5vOup1dBbsau1rxyyul4bopbkbZkstnHWCY2vhtBNcyhh8EfxeBjfdvsJl7xzu8N423Be9VUL23QlL9OwJ19PK6IviOX3Fp32GnSK5+KZgNTjV5JZwRCgI51gyUJLwjNAktAnHlDMkXBCGhBahQzmuLvqPruUP7ETSoTe+b9jHyCFHYiNis6p4SFYpNoEw3zznZbZNGXbc2mBvjGaErRysYxP+pyasr8A8tDd/aHawC8XGOw==",
            "test": False,
        },
        {
            "data": "m=edit&p=7ZRdT8IwFIbv9yvIue7F2g6E3hhA0AvEj2GIWRYycEYiZDqYMSX7755zNh0QLrzxKzGjLy9PD927du3qOYvSWEiXProp8BsvTza5qWaDm1teo/l6EZuaaGfrhyRFI8RFvy/uo8UqdoKyKnQ2tmVsW9hTE4AEAQqbhFDYK7Ox58YOhfWxC4SHbFAUKbS9yo65n1y3gNJFPyw92lu0s3k6W8STQUEuTWBHAug+Hf43WVgmLzGUOej3LFlO5wSm0RofZvUwfyp7Vtld8pjB+y1yYdtFXP9AXF3F1R9x9eG46uvjtsI8x2m/xsATE1D2m8o2K+ubDWgXjCdASzAqp5CINI1zgsGKhQLd2gMNRaBbgSMGZxVoSQLtCkhX7Q0iXY9IZ4tIJv0tonic3hbx9H5NnWuOt0iRb4d4OwSfVJpNTitB2mdVrCOcG2E16wmry1pnHXBNj3XM2mX1WBtcc0Sz+8n5L6b8G+IEutjMu1f977HQCcDP0vtoFuO7P8yW0zitDZN0GS0AD5vcgVfgFmg6u/7Pnx86f2gJ3N+2C35bHNyXofMG",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(nori_adjacent(color="black"))
        self.add_program_line(avoid_unknown_src(adj_type=4, color="not black"))

        tag = tag_encode("reachable", "grid", "src", "adj", 4, "not black")
        for (r, c, d, label), letter in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            if letter != "?":
                self.add_program_line(grid_src_color_connected((r, c), color="not black"))

            for (r1, c1, _, _), letter1 in puzzle.text.items():
                if (r1, c1) == (r, c) or letter == "?" or letter1 == "?":
                    continue
                if letter1 == letter:
                    self.add_program_line(f":- not {tag}({r}, {c}, {r1}, {c1}).")
                else:
                    self.add_program_line(f":- {tag}({r}, {c}, {r1}, {c1}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
