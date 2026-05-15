"""The Anglers solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected
from noqx.rule.route import single_route


class AnglersSolver(Solver):
    """The Anglers solver."""

    name = "Anglers"
    category = "route"
    aliases = ["anglerfish"]
    examples = [
        {
            "data": "m=edit&p=7VRNj9MwEL33V6zmPIc4TpqPCyrLlkvoAu1qtYqqKg1ZNSLZlHwg5Kr/nfEkbSpSxFLBigOyPHp+E8dvZuypvjRRmaBLQ7pooKAhLZOnaXg8jW4s0jpL/CucNPWmKAkg3k6n+BhlVYKjUPBmsRztlOerCaq3fggmIE8BS1Qf/J1656sHVHNyAVrEBYQEoEnwpof37NfouiWFQXjWYYIPBOvkqa7a5Xs/VAsEfchr3qoh5MXXBNo9vI6LfJ1Cv5PJqvlUfG7g+GvIm6xO4yIrSuBfieUe1aSVHhyki066BSh76fIoXZ6XbnbS47SMs2QVXKR+HdVUiGqTbs+F4J0PYU9l+UhBrPxQx3PXQ7eHc38HtgW+tdeKCYtDXtoKwtiCtqgHwnE0IXvCM6BNy4EQhtSMfcKIsWZeHRg6TPi7vc7MDqRHPoknxQVbDqjxkHLsIeUOKNf5gaJjp3y4yXZBiUAl2b5ha7C12Qb8zQ3be7bXbC22Y/7G0al8ZrLbNJ/G/7tyQJoUkeciWK7sgGe3wBao8ySfKTmUHorjcC7Hy1EI86Z8jOKELmiQPiVXs6LMo4xWsyZfJ2W/nm+ibQLUM/Yj+AY8qTyCWsP/NvJvthFdIuPF7vefeW4hZZw6C1I/Q3WLsG1W0YoCA6Sk/trZPqRLnH/nTHrz5x3UA37i8OyB48VrRC1mOfoO",
        },
        {
            "data": "m=edit&p=7VRNj5swEL3zK1ZzngO2IQEuVbrd9ELTj6RaRQitCPUqqLBs+agqR/nvHYZ02YVcWqlSKlXGT8/PHvuZ0bj+1iaVRiG7T3loo6Dm+A53NXe526e2yZpcB1e4aJt9WRFBfL9c4n2S1xqtSHCwiK2D8QOzQPM2iEACchcQo/kYHMy7wGzRrGkK0CEtJCYAJdGbgd7yfMeue1HYxFcnTnRLtNEPTd0PPwSR2SB0h7zm0I5CUX7X0MfwOC2LXQZDJIt1+6X82sLT1lC0eZOlZV5WwFuJ+Ihm0VsPf1kXg3U1WFdP1tV56/JkPc2qNNd34R+53yUNJaLeZ4/nruCfv8KR0vKJLnEXRN19Pg/UG+g6OBw7rwdQXhf5ikL73IEjR4I3FoR0x4ozGyvz8b7C80eKFC+jyJFgX1vy5To0p/BZ7sH1JpKnJpIvJpKQ082EP5to0rbPaOMjyOCSbUrGDf1RNIrxDaPN6DKGvOaG8ZbxmtFhnPGaeZeT38ra8z/1l+xE7qnMX7T5v6fFVgTrtrpPUk1VFGYP+mpVVkWS02jVFjtdDeP1PnnUQA/b0YIfwJ1STw/l/7fuQt+6LkX2pdXOpdmhao6tnw==",
        },
        {
            "data": "m=edit&p=7VRNb6MwEL3zK6o5z8HG5Itb+pFe2Oy2SVVFCFWEugpaKF0+VpWj/PeOh7S0SS6tVCkrrYyfnh8M84bBrv40calRuvZSQxQoaXgjj6ca9HiK7Zindab9Exw39aooiSD+nEzwIc4qjU4oOVhGztqMfDNGc+mH4ALylBChufLX5odvFmhmdAvQIy0gJgFdohcdveX7lp21ohTEp1tOdEG01o911S5/+aGZI9gkpxxqKeTFXw1tDK+TIl+m0EWyWDX3xe8G3l4NeZPVaVJkRQn8Khlt0Ixb68GrddlZV5119WZdHbbubq0naZlk+i74kvtlXFMjqlX6dKiE0eESNtSWayrizg9tPTcdHXZ05q831usa1MhGuoJi2+aB5+4qUok9yevvSq5UHyXKIDnPgvIMbR6F73oJUvT3NaX2tZ7Y1wa7GuWZcDaXcU6FolGM54yCsccY8DMXjLeMZ4weY5+fGdhP9amP+b7gb7IT9ra778MY/Hta5IQwa8qHONH0cwfpoz6ZFmUeZ7SaNvlSl916toqfNNB5s3HgGXhS6+n8+n8EHekRZFskjm3vHJsd2s2R8wI=",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.symbol) > 0, "No clues found.")
        fail_false(len(puzzle.text) == len(puzzle.symbol), "Unmatched clues.")
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="grid", path=True))
        self.add_program_line(avoid_unknown_src(color="grid", adj_type="line"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(symbol_name, "tents__3")
            self.add_program_line(f"dead_end({r}, {c}).")

        tag = tag_encode("reachable", "grid", "src", "adj", "line", "grid")
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if not (0 <= r < puzzle.row and 0 <= c < puzzle.col):  # coordinations out of bounds
                self.add_program_line(f"grid({r}, {c}).")

            self.add_program_line(f"dead_end({r}, {c}).")
            self.add_program_line(grid_src_color_connected((r, c), color="grid", adj_type="line"))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num + 1, (r, c), color="grid", adj_type="line"))

            for (r1, c1, _, _), _ in puzzle.text.items():
                if (r1, c1) != (r, c):
                    self.add_program_line(f":- {tag}({r}, {c}, {r1}, {c1}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
