"""The Yajirushi 2 solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, invert_c, shade_cc
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected


def yajirushi_pair(color: str) -> str:
    """Generate a rule to create Yajirushi pairs and constraints."""
    rule = "{ pair(R, C1, R, C2) } :- arrow_N_W__5(R, C1), arrow_N_W__1(R, C2), C2 > C1 + 1.\n"
    rule += f":- pair(R, C1, R, C2), grid_all(R, C), C1 < C, C < C2, not {color}(R, C).\n"
    rule += "{ pair(R1, C, R2, C) } :- arrow_N_W__7(R1, C), arrow_N_W__3(R2, C), R2 > R1 + 1.\n"
    rule += f":- pair(R1, C, R2, C), grid_all(R, C), R1 < R, R < R2, not {color}(R, C).\n"

    # every arrow symbol should belong to a pair
    rule += ":- arrow_N_W__1(R, C), not pair(_, _, R, C).\n"
    rule += ":- arrow_N_W__3(R, C), not pair(_, _, R, C).\n"
    rule += ":- arrow_N_W__5(R, C), not pair(R, C, _, _).\n"
    rule += ":- arrow_N_W__7(R, C), not pair(R, C, _, _).\n"

    return rule


class Yajirushi2Solver(Solver):
    """The Yajirushi 2 solver."""

    name = "Yajirushi 2"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VVLb5tAEL7zK6I5zwF21+Zxc1K7l5S0tSMrQghhl8hWQbjYtNFa/PfOzuJiWVEVVX3kUK2Z+fh21jvf7IP9lzZvCgypyQBd9KjJwOUnUObn9m2xPZRFdIWT9rCpGwKId7MZPublvkAn6cNS56jDSE9Qv40S8ABB0ONBivpDdNTvIh2jnlMXoEoRqrY8bNd1WTfAnEdxt3agIDgd4JL7DbqxpOcSji32CT4QzJum/pbF2bX9p/dRohcIZvJrHm4gVPXXAvrkzPu6rlZbQ6zyA0ncb7Y7QEkd+/ZT/bntQ720Qz2xEh5OEoKfS5CDBPlDgnxegriQsPz9EsK062h5PpKILEqMnvsBBgOcR0dQAiKFoJR1Y+sCdmPrfNc6G+nbyLB3dkBoIz3Xhnri5EXvVe9NeGdqYWc2Qn27bXhSTl/1xJgJNRC+uCTUxZCQCTEQnEkC7jnDMfLEUDZedOzMohg7YyvYLqhMqCXbN2xdtiO2txwzZbtke8NWsR1zjG8K/cKlsGU5TwfkiFL18GKvUJl94gOE+imb9jv2T+SdiIDvifM2el1M6iQwb5vHfF3QEYnbalU0V3HdVHlJ7/NNviuArqrOgSfgJ5EozLD/t9ervr3MUrm/fHD+zTlOqOJ0NFHfIezaLM+o3EBfSjQdcvQ8r8SL+b8ul26A1PkO",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_cc(colors=["ox_E__8", "arrow_N_W__1", "arrow_N_W__3", "arrow_N_W__5", "arrow_N_W__7"]))
        self.add_program_line(yajirushi_pair(color="ox_E__8"))
        self.add_program_line(adjacent())
        self.add_program_line(invert_c(color="ox_E__8", invert="arrow_all"))
        self.add_program_line(grid_color_connected(color="ox_E__8"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="arrow_all"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name.startswith("arrow_N") and symbol_name.split("__")[1] in ["1", "3", "5", "7"]:
                self.add_program_line(f"{symbol_name.replace('B', 'W')}({r}, {c}).")

            if symbol_name == "ox_E__8":
                self.add_program_line(f"ox_E__8({r}, {c}).")

        self.add_program_line(display(item="arrow_N_W__1", size=2))
        self.add_program_line(display(item="arrow_N_W__3", size=2))
        self.add_program_line(display(item="arrow_N_W__5", size=2))
        self.add_program_line(display(item="arrow_N_W__7", size=2))
        self.add_program_line(display(item="ox_E__8", size=2))

        return self.program
