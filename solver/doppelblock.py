"""The Doppelblock solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import count, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, validate_direction, validate_type


class DoppelblockSolver(Solver):
    """The Doppelblock solver."""

    name = "Doppelblock"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VXBbtpAEL37K6I5z2HXuxjbN5qGXAhpCxGKLAsZxwgUIycGV9Ui/3tnxxRbtImSQ8klWvbp+e0M+2bMLtvnKikzDGgoHwVKGsoXPH1tP+IwputdnoUXOKh2q6Ikgng7HOIyybeZE0nOFbGzN0FoBmiuwwgkILg0JcRovod7cxOaMZoJLQFq0kZNkEv0qqUzXrfsshGlID4+cKL3RNN1mebZfNQo38LITBHsPl8421LYFD8zOPiwz2mxWaytsEh2VMx2tX46rGyrh+Kxgj9b1GgGL9tVrV11tKv+bdf9/3aDuK6p7T/I8DyMrPe7lvotnYT72vragxI21ScvzbsBJfm73I6ireKKjtI7VXST5XUU1yqqFXr6RPD6J4LPXmTQKoFiRbeKFB5L/Y5EGSR1gxRvfqyBapVc8T3jkNFlnFJD0CjGr4yCscc44pgrxhnjJaNm9Dimb1v6xqaDpoJ00/ozmIq0y6e4Hd55n2MngklVLpM0o5/ruNossvJiXJSbJAe6H2oHfgHPSFG4/rwyPujKsK9AvOvi+PgjFZkJKoHmFuGpmifztMiB/nXwNV2rv/SzV0XHMnZ+Aw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row == puzzle.col, "This puzzle must be square.")
        n = puzzle.row
        self.add_program_line(grid(n, n))
        self.add_program_line(fill_num(_range=range(1, n - 1), color="black"))
        self.add_program_line(unique_num(_type="row", color="grid"))
        self.add_program_line(count(2, _type="row", color="black"))
        self.add_program_line(unique_num(_type="col", color="grid"))
        self.add_program_line(count(2, _type="col", color="black"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if r == -1 and 0 <= c < n and isinstance(num, int):
                begin_r = f"Rb = #min {{ R: black(R, {c}) }}"
                end_r = f"Re = #max {{ R: black(R, {c}) }}"
                self.add_program_line(f":- {begin_r}, {end_r}, #sum {{ N, R: number(R, {c}, N), R > Rb, R < Re }} != {num}.")

            if c == -1 and 0 <= r < n and isinstance(num, int):
                begin_c = f"Cb = #min {{ C: black({r}, C) }}"
                end_c = f"Ce = #max {{ C: black({r}, C) }}"
                self.add_program_line(f":- {begin_c}, {end_c}, #sum {{ N, C: number({r}, C, N), C > Cb, C < Ce }} != {num}.")

            if 0 <= c < n and 0 <= r < n:
                fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
                self.add_program_line(f"number({r}, {c}, {num}).")

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"black({r}, {c}).")

        self.add_program_line(display(item="number", size=3))
        self.add_program_line(display(item="black", size=2))

        return self.program
