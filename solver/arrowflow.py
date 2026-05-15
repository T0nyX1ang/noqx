"""The Arrow Flow solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, shade_cc
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected


def arrow_flow_adjacent() -> str:
    """Generate a rule to define the adjacency for arrow flow."""

    # the definition is designed to be compatible with the reachable propagation
    rule = "adj_line_directed(R, C, R, C + 1) :- grid_all(R, C), grid_all(R, C + 1), arrow_N_W__5(R, C).\n"
    rule += "adj_line_directed(R, C, R, C - 1) :- grid_all(R, C), grid_all(R, C - 1), arrow_N_W__1(R, C).\n"
    rule += "adj_line_directed(R, C, R + 1, C) :- grid_all(R, C), grid_all(R + 1, C), arrow_N_W__7(R, C).\n"
    rule += "adj_line_directed(R, C, R - 1, C) :- grid_all(R, C), grid_all(R - 1, C), arrow_N_W__3(R, C)."
    return rule


class ArrowFlowSolver(Solver):
    """The Arrow Flow solver."""

    name = "ArrowFlow"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VVfb5swEH/nU1T37AeMwQG/TG3X7KWj65IpqhBCJKNKNBAZCdvkiO++80FCPVVTVanrJk2Oz/fP5n539mX3tc2bgnHX/ETIcMXh85CmF0qa7jDmm31ZqDN23u7XdYMMYzfTKbvPy13BnGRwS52DjpS+ZfqdSoADAw8nh5TpW3XQ75WOmZ6hCZifMqjacr9Z1WXdAOk4+l33Gz1kr0Z2QXbDXfZK7iIfDzyyd8jmTVN/z+Lsold9UImeMzAfv6DthoWq/lbAEJyRV3W13BjFMt8jxN16swUm0LBrP9dfWjh+omP6vIdwd4TAfw9BjBDECYJ4HIL3C4TF8yCU2/qR4KO067AwHzH8TCUGyaeRDUd2pg4QclA+g0j0i08LDySunYn2AAI9Eh+vCtUVBLokYhQnKIYnUbqWsxSWszTO5gIOcigtcxihODmJkWdZuWsO8x7I8lisk8YcwPmo8EJUBKMsPPsIEZgj3jw4IjA75ChLGz2XBv7xC5ghrg6dKSVm0iWLfSvRNiUPj+gcE8+0IPqWqEs0IHpNPldEF0QvifpEJflMTOmeWNy+gFaQwqWE2PfuhYJMRN9i7BH8e7rUSWDWNvf5qsAXGLfVsmjO4rqp8hLl2TrfFoCdsHPgB9DEW+uZbf+b41/aHE2R3Ge/otd51AnmGl+UvmGwbbM8wzwD/gMzo8de+HTDH8eFrSB1fgI=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_cc(colors=["arrow_N_W__1", "arrow_N_W__3", "arrow_N_W__5", "arrow_N_W__7"]))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(arrow_flow_adjacent())
        self.add_program_line(avoid_unknown_src(adj_type="line_directed", color="grid"))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__1", adj_type=4))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__3", adj_type=4))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__5", adj_type=4))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__7", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(grid_src_color_connected((r, c), adj_type="line_directed", color="grid"))
            self.add_program_line(f"hole({r}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num + 1, (r, c), adj_type="line_directed", color="grid"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            fail_false(
                symbol_name.startswith("arrow_N") and symbol_name.split("__")[1] in ["1", "3", "5", "7"],
                f"Invalid symbol at ({r}, {c}).",
            )
            self.add_program_line(f"{symbol_name.replace('B', 'W')}({r}, {c}).")

        self.add_program_line(display(item="arrow_N_W__1", size=2))
        self.add_program_line(display(item="arrow_N_W__3", size=2))
        self.add_program_line(display(item="arrow_N_W__5", size=2))
        self.add_program_line(display(item="arrow_N_W__7", size=2))

        return self.program
