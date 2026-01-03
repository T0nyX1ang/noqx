"""The Yajitatami solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, count_reachable_src
from noqx.rule.shape import all_rect_region, avoid_edge_crossover


def yaji_region_count(target: int, src_cell: Tuple[int, int], arrow_direction: int) -> str:
    """Generates a constraint for counting the number of {color} cells in a row / col."""
    src_r, src_c = src_cell
    rule = ""

    if arrow_direction == 1:  # left
        rule += f":- not edge_left({src_r}, {src_c}).\n"
        rule += f":- #count {{ C1 : edge_left({src_r}, C1), C1 <= {src_c} }} != {target}."

    if arrow_direction == 2:  # right
        rule += f":- not edge_left({src_r}, {src_c + 1}).\n"
        rule += f":- #count {{ C1 : edge_left({src_r}, C1), C1 > {src_c} }} != {target}."

    if arrow_direction == 0:  # top
        rule += f":- not edge_top({src_r}, {src_c}).\n"
        rule += f":- #count {{ R1 : edge_top(R1, {src_c}), R1 <= {src_r} }} != {target}."

    if arrow_direction == 3:  # bottom
        rule += f":- not edge_top({src_r + 1}, {src_c}).\n"
        rule += f":- #count {{ R1 : edge_top(R1, {src_c}), R1 > {src_r} }} != {target}."

    return rule


def rect_constraint() -> str:
    """Generate a cell relevant constraint for rectangles with the width/height of 1."""
    rule = ":- topleft(R, C), left(R + 1, C), top(R, C + 1).\n"
    rule += ":- grid(R, C), topleft(R, C), #count { R1, C1: adj_edge(R, C, R1, C1) } = 0."
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
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))
            fail_false(isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows.")
            num, d = clue.split("_")
            fail_false(num.isdigit() and d.isdigit(), f"Invalid arrow or number clue at ({r}, {c}).")
            self.add_program_line(count_reachable_src(int(num), (r, c), main_type="bulb", color=None, adj_type="edge"))
            self.add_program_line(yaji_region_count(int(num) + 1, (r, c), int(d)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
