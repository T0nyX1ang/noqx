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
            "data": "m=edit&p=7VZrT9tIFP2eX1HN1460Hj8f0moV0sC2G0IoIDaJUGSCIW5tzPoBrRH/veeOTf2IYQWtdvfDysnkzLnzOGdmPDfpX7mX+NzCo9lc4QKPpujyayr0eXyOgyz03Td8mGebOAHg/GDKL70w9fmH+WYyiod374Z/3trZYiH2lPy9cvpp99Pbj9Ef7wMtEbtTe7Y/2w/Uq+Hvo51Dc/zWnOXpSebfHkZi59PJ4vhydnrlqF/H04VeLA4U48Pi8pfb4cmvg2Ul4WxwXzhuMeTFnrtkKuPyK9gZLw7d+2LfLca8OEKIcQFuAiQYVwHHNTyVcUKjkhQK8LTCgHPAdZCsQ381KZmZuyyOOaN5dmRvgiyKb31WdpP1dRydB0ScexlWKt0EN1UkzS/iz3nVFgOyKA+zYB2HcUIkcQ+8GEoL1TA9PrTaB8HSB6EeH2Tvh32EwbV/ESRykrYHp9/DA/bnI1ys3CUZOqmhXcMj9x7l1L1nmomedN7kFjLNRlX7XtWpyo4wcEUYSituUFz9XjUpyn6rm5tqq7lF8bq5RVG2Vze3iajjtt7QBr1Cqp7LcleWqiyPYYoXmizfyVKRpSHLiWwzhlehGVzoMKxiRLxoQndKrJtcGFaFHS7IB2HDAoZFwngJhSUqjL5W1deCQNItMfo6VV8bPhytxI7CVaXq62jAMAYMjqui7AsO2KjmhU6j0mk0tJEeWnKJocGoNBgNzaTTfNQJbbQFUg/a21V7u6ET2oTzqA3tnaq909SPLXRKzfgFJp1Y1FO5tCNZ6rI05ZJbdMpedA6bu8tUkw6lyRnOPm7GMMi+yrcJpxMLsbS6gZceB6aSecfG+RZw7tjl+fhbQ0sV3hsPduln184GSzaBuzfTOIm8ELfB+OKqUZvm0bmf1PVRHN3EaZD5DPcyS+NwlebJpbf2V/4Xb50xt0wNzUiLu5bjtagwjm/o1ukZ4THUIoOr6zjxe0NE+tD/xFAU6hnqPE4uOpruvDBse5EZs0WV12yLyhLcoY26lyTxXYuJvGzTIhp5ozWSf91ZzMxrS/Q+e53Zono5HgbsC5NfeRvq/yfR/3oSpb1SXn2FvS5B/eiNuiwmHHcnLw44u8lX3gqmGP6x8WcC86d74LZ9UWD+isDLVf00g//q5OiBxNsbQE7aCvzjB01eYHHyTDapg126J6eAfSatNKJ9/BMZpBHt8lvpgsRuZwywPUkDbDdvgNpOHSC3sge4JxIIjdrNIaSqm0Zoqq1MQlM1k8mSbbwgzdnZ4Bs=",
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
