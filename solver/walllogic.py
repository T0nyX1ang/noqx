"""The Wall Logic solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, bulb_src_color_connected, count_reachable_src


class WallLogicSolver(Solver):
    """The Wall Logic  solver."""

    name = "Wall Logic "
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VZfb9MwEH/vp5j87If4bCd2XtAYLS+jA1Y0TVFVdV1gFaky2gahVP3unK9r04s2YBsaPFROTvfznX1/7WTxrRrPc6mS8GgnI6lwxM7QCxDRux2D6bLI0yN5XC1vyjkyUp71evLzuFjkspPdqQ07q9qn9bGs36aZACHpVWIo6w/pqn6X1n1Zn6NISDWUYlYVy+mkLMq52M7Vp8gpIQHZbsNekDxwJ5tJFSHfv+ORvUR2Mp1Pinx0upl5n2b1QIpg+zWtDqyYld9zsVlGeFLOrqZh4mq8xAgXN9NbITUKFtV1+bUSWwtrWR9vIuj+YQS6iUDvItD3RwB/JYLitrzHdz9cr7EsH9H7UZqFQD41rGvY83S1Dg6thDG41GAzUOWEjRDqBgap3cE4YsoJV05ihPEOugDFK9FMeJyAHfTcsvdstYqAba4UcLlyXA6ebad0zFxXRiNWDbaKeaOs5frW8/1jzeWJ4XIH3L4P+6s9A96xACDiyYQoQewarLhBUIY5DJSAJiAAaGGeAICEOQyalwt0wvWN5fom5pgStGcvDvb9HrZcnrTsu1b81C97+o4XFDxvH035U3tYs/11ZFty11rf2k/x+mhorde8wNrws6ENb0gd83romNdDx47vl7T2dzz/2rX0qcG2/YKnWdGZviTaIwpEB3jkZa2JviEaEbVET0mnS/SC6AlRQzQmnSRcGo+6Vp7vTjjA2DDehTvJShth9vRvfcyMoS/br4Y9aBw0Hh7DTia611/yo345n40L/PD2q9lVPt9i/O1Zd8QPQS+eTzj8Cf23f0KhRNELX1zPvUczTHW4+2R9JsVtNRqPMNECm0w+VbK7QP+B2KP0ke4+YcnDTrx4cfEbNOz8BA==",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num + 1, (r, c), main_type="bulb", color=None, adj_type="edge"))

        tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
        self.add_program_line(f":- adj_edge(R, C, R1, C1), {tag}(R0, C0, R, C), not {tag}(R0, C0, R1, C1).")
        self.add_program_line(avoid_unknown_src(color=None, main_type="bulb", adj_type="edge"))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
