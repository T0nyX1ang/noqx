"""The Haisu solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, defined, display, fill_line, grid
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_border
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import directed_route


def haisu_rules() -> str:
    """Generate constriants for haisu."""
    rule = "clue(R, C) :- number(R, C, _).\n"
    rule += "clue_area(A) :- clue(R, C), area(A, R, C).\n"
    rule += "area_max_num(A, N) :- clue_area(A), #max { N0 : area(A, R, C), number(R, C, N0) } = N.\n"
    rule += "area_possible_num(A, 0..N) :- clue_area(A), area_max_num(A, N).\n"
    return rule


def haisu_count() -> str:
    """Partial sum method for haisu."""
    rule = "haisu_count(R, C, A, 0) :- path_start(R, C), clue_area(A).\n"
    rule += "area_in(A, R, C) :- area_border(A, R, C, D), line_in(R, C, D).\n"
    rule += "haisu_count(R, C, A, N) :- clue_area(A), area_possible_num(A, N), grid(R, C), adj_line_directed(R, C, R1, C1), haisu_count(R1, C1, A, N), not area_in(A, R, C).\n"
    rule += "haisu_count(R, C, A, N) :- clue_area(A), area_possible_num(A, N), grid(R, C), adj_line_directed(R, C, R1, C1), haisu_count(R1, C1, A, N - 1), area_in(A, R, C).\n"
    rule += ":- clue_area(A), grid(R, C), haisu_count(R, C, A, N1), haisu_count(R, C, A, N2), N1 < N2.\n"
    rule += ":- number(R, C, N), area(A, R, C), not haisu_count(R, C, A, N).\n"
    return rule


class HaisuSolver(Solver):
    """The Haisu solver."""

    name = "Haisu"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VbBjtMwEL33K1Y+zyF27CTOBS1L2UvpArsIVVFVddvARqRkSRsEqfrv++y4TQoF1LICDsjN6NkzE78Xj0ddfqqmZUohhh+RRxzD96R9As/8tuMmW+VpfEbn1equKAGIrob0bpovU+olLmrcW9c6rs+pvowTJhjZh7Mx1a/idf0irvtUX8PFiGNtAMQZCcB+C99av0EXzSL3gIcOA44AZ1k5y9PJoFl5GSf1DTGzz1ObbSBbFJ9T1qTZ+axY3GZm4Xa6gpjlXXbvPMtqXnyo2G4LtqjyVTYr8qJkju2G6nMrwb3mgA6/1eHvdPiHdYjH0JFnH9N5VtpN9jXowxo2OJ/XUDGJEyPoTQujFl7H643huWZ+gExTEvYImR9h6u+m0kzZNdstKG/Pr4xf7KaB8bInbXgg9sJDby88NF522YZHYs8fyQ438OWW9cja59YKa28gimrf2mfWetYqawc2pg+t3FfEJQQLvBF3gUvdYBkQV6HDmrjRYbAKgaMG457wkDuM3NDlhiBoeFuMXO1yI+jQfoO1R8JzudoHlhZjjQQXDktg5fYFT+V4qg43w0c5PgoclOOgOpwNz2DLE9wCxy1CfOTiow5PcON6yw3x2sXrLn8coZYOS2DDc2PK33zaC2ultYH95KGpsqPqsHu6TASmKANiqH00rzxbfbW3CdWJD5GE3zqOLQcmjHgdob45N6Cpj18KSoS03XM71OPPxr2EDaDubFiUi2mObtCfv+/MhtXiNi3b+UWxuC+W2Spl6MubHvvC7GPvnPzfqv/1Vm3Oyjv5opzWBn/33ib1gHBDqb4idl9NphOIYvhfQD9xjH6cgTt9lGN0guN4Vo8m8K9ujgy094MOdL7vHH+80NBSx70H",
        },
        {
            "url": "https://puzz.link/p?haisu/9/9/199103msp7vvv4pre00bs6poj0068sr1ugp2g2g2g2u2g2k2k2g2u2g2g2g2p",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?haisu/13/9/5948l0l2la55d8220gg44110000vg305c0cc00000000fvol3t1k3h25g5y5r6i7jao5zq",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false("S" in puzzle.text.values() and "G" in puzzle.text.values(), "S and G squares must be provided.")
        self.add_program_line(defined(item="number", size=3))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="line_directed"))
        self.add_program_line(fill_line(color="grid", directed=True))
        self.add_program_line(directed_route(color="grid", path=True))
        self.add_program_line(grid_color_connected(color="grid", adj_type="line_directed"))
        self.add_program_line(haisu_rules())
        self.add_program_line(haisu_count())

        s_index = []
        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))

            for r, c in ar:
                if puzzle.text.get(Point(r, c, Direction.CENTER, "normal")) == "S":
                    s_index = ar

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if clue == "S":
                self.add_program_line(f"path_start({r}, {c}).")

            if clue == "G":
                self.add_program_line(f"path_end({r}, {c}).")

            if isinstance(clue, int):
                self.add_program_line(f"number({r}, {c}, {clue - 1 if (r, c) in s_index else clue}).")  # special case

        for (r, c, d, label), draw in puzzle.line.items():
            if label == "normal" and not draw:
                self.add_program_line(f':- line_in({r}, {c}, "{d}").')
                self.add_program_line(f':- line_out({r}, {c}, "{d}").')

            if label in ["in", "out"] and draw:
                self.add_program_line(f':-{" not" * draw} line_{label}({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_in", size=3))
        self.add_program_line(display(item="line_out", size=3))

        return self.program
