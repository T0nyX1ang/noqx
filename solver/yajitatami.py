"""The Yajitatami solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, count_reachable_src
from noqx.rule.shape import all_rect_region, avoid_edge_crossover


def yaji_region_count(target: int, src_cell: Tuple[int, int], arrow_direction: str) -> str:
    """Generates a constraint for counting the number of {color} cells in a row / col."""
    src_r, src_c = src_cell
    rule = ""

    if arrow_direction == Direction.LEFT:
        rule += f':- not edge({src_r}, {src_c}, "{Direction.LEFT}").\n'
        rule += f':- #count {{ C1 : edge({src_r}, C1, "{Direction.LEFT}"), C1 <= {src_c} }} != {target}.'

    if arrow_direction == Direction.RIGHT:
        rule += f':- not edge({src_r}, {src_c + 1}, "{Direction.LEFT}").\n'
        rule += f':- #count {{ C1 : edge({src_r}, C1, "{Direction.LEFT}"), C1 > {src_c} }} != {target}.'

    if arrow_direction == Direction.TOP:
        rule += f':- not edge({src_r}, {src_c}, "{Direction.TOP}").\n'
        rule += f':- #count {{ R1 : edge(R1, {src_c}, "{Direction.TOP}"), R1 <= {src_r} }} != {target}.'

    if arrow_direction == Direction.BOTTOM:
        rule += f':- not edge({src_r + 1}, {src_c}, "{Direction.TOP}").\n'
        rule += f':- #count {{ R1 : edge(R1, {src_c}, "{Direction.TOP}"), R1 > {src_r} }} != {target}.'
    return rule


def rect_constraint() -> str:
    """Generate a cell relevant constraint for rectangles with the width/height of 1."""

    rule = f':- rect(R, C, "{Direction.TOP_LEFT}"), rect(R + 1, C, "{Direction.LEFT}"), rect(R, C + 1, "{Direction.TOP}").\n'
    rule += f':- grid(R, C), rect(R, C, "{Direction.TOP_LEFT}"), #count {{ R1, C1: adj_edge(R, C, R1, C1) }} = 0.'
    return rule


class YajitatamiSolver(Solver):
    """The Yajitatami solver."""

    name = "Yajitatami"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VRNj9MwEL33V6x8noM/0ubjVpaWS+kCu2i1iqKo7Qa2olWWtkHIVf/7vhmnBNSVEALKBVmePD+Px2/Gsbefm9mmogTNJaTJoLnISrc6la7bdrPcrarsgobN7qHeABBdjcf0YbbaVr289Sp6e59mfkj+VZYrq0i6UQX5t9nev878lPw1phQZcBMgo8gCjjp4K/OMLgNpNPA0BORld4CL5WaxqspJYN5kub8hxfu8kNUM1br+UqkQQsaLej1fMjGf7ZDM9mH52M5sm/v6U9P6muJAfhjkjp6R6zq5DINcRs/I5Sz+sty0OBxQ9ncQXGY5a3/fwaSD19kedprtlY15qSu5nHxCiNjXgXIdNeifeMWDE6+4jfU9lQRKd1RyumOanlBG28BxEY+caWV845CEkVTuxI7FWrE3yJS8E/tSrBbbFzsRnxEKYGJHJkFgiw2SPjASEzwAhlbGMfNHHBHGLcbaOGr9E/ggkRZbjTIC40vWIBnGBnfJuIBtRNaGOIJd2BdfshHKxjhCnIhjQuytSL4UG4kdSCoxH+kvHfofqJozyDpNfiort6jiDw2VPOe46OVqdP+xupjWm/VshUszbdbzanMc45U69NRXJT3HcVL0/+H6Rw8XH4E+85/8uxcrR3VxGchfkXpsylm5qPGT6eLsMnHXit4T",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(rect_constraint())
        self.add_program_line(avoid_edge_crossover())

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))
            fail_false(isinstance(clue, int) and label.startswith("arrow"), "Please set all NUMBER to arrow sub.")
            arrow_direction = label.split("_")[1]
            self.add_program_line(count_reachable_src(int(clue), (r, c), main_type="bulb", color=None, adj_type="edge"))
            self.add_program_line(yaji_region_count(int(clue) + 1, (r, c), arrow_direction))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
