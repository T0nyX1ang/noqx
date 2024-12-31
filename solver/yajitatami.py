"""The Yajitatami solver."""

from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, edge, grid
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, count_reachable_src
from noqx.rule.shape import all_rect_region, avoid_region_border_crossover
from noqx.solution import solver


def yaji_region_count(target: int, src_cell: Tuple[int, int], arrow_direction: int) -> str:
    """
    Generates a constraint for counting the number of {color} cells in a row / col.

    A grid fact should be defined first.
    """
    src_r, src_c = src_cell
    rule = ""

    if arrow_direction == 1:  # left
        rule += f":- not edge_left({src_r}, {src_c}).\n"
        rule += f":- #count {{ C1 : edge_left({src_r}, C1), C1 <= {src_c} }} != {target}."

    if arrow_direction == 2:  # right
        rule += f":- not edge_left({src_r}, {src_c + 1}).\n"
        rule += f":- #count {{ C1 : edge_left({src_r}, C1), C1 > {src_c} }} != {target}."

    if arrow_direction == 0:  # up
        rule += f":- not edge_top({src_r}, {src_c}).\n"
        rule += f":- #count {{ R1 : edge_top(R1, {src_c}), R1 <= {src_r} }} != {target}."

    if arrow_direction == 3:  # down
        rule += f":- not edge_top({src_r + 1}, {src_c}).\n"
        rule += f":- #count {{ R1 : edge_top(R1, {src_c}), R1 > {src_r} }} != {target}."

    return rule


def rect_constraint() -> str:
    """Generate a cell relevant constraint for rectangles with the width/height of 1."""
    rule = ":- upleft(R, C), left(R + 1, C), up(R, C + 1).\n"
    rule += ":- grid(R, C), upleft(R, C), #count { R1, C1: adj_edge(R, C, R1, C1) } = 0."
    return rule


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)

    assert len(puzzle.text), "No clues found."
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(all_rect_region())
    solver.add_program_line(rect_constraint())
    solver.add_program_line(avoid_region_border_crossover())

    for (r, c), clue in puzzle.text.items():
        solver.add_program_line(f"clue({r}, {c}).")
        solver.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))
        assert isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows."
        num, d = clue.split("_")
        assert num.isdigit() and d.isdigit(), "Invalid arrow or number clue."
        solver.add_program_line(count_reachable_src(int(num), (r, c), main_type="bulb", color=None, adj_type="edge"))
        solver.add_program_line(yaji_region_count(int(num) + 1, (r, c), int(d)))

    for r, c, d in puzzle.edge:
        solver.add_program_line(f":- not edge_{d.value}({r}, {c}).")

    for r, c, d in puzzle.helper_x:
        solver.add_program_line(f":- edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Yajitatami",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VRNj9MwEL33V6x8noM/0ubjVpaWS+kCu2i1iqKo7Qa2olWWtkHIVf/7vhmnBNSVEALKBVmePD+Px2/Gsbefm9mmogTNJaTJoLnISrc6la7bdrPcrarsgobN7qHeABBdjcf0YbbaVr289Sp6e59mfkj+VZYrq0i6UQX5t9nev878lPw1phQZcBMgo8gCjjp4K/OMLgNpNPA0BORld4CL5WaxqspJYN5kub8hxfu8kNUM1br+UqkQQsaLej1fMjGf7ZDM9mH52M5sm/v6U9P6muJAfhjkjp6R6zq5DINcRs/I5Sz+sty0OBxQ9ncQXGY5a3/fwaSD19kedprtlY15qSu5nHxCiNjXgXIdNeifeMWDE6+4jfU9lQRKd1RyumOanlBG28BxEY+caWV845CEkVTuxI7FWrE3yJS8E/tSrBbbFzsRnxEKYGJHJkFgiw2SPjASEzwAhlbGMfNHHBHGLcbaOGr9E/ggkRZbjTIC40vWIBnGBnfJuIBtRNaGOIJd2BdfshHKxjhCnIhjQuytSL4UG4kdSCoxH+kvHfofqJozyDpNfiort6jiDw2VPOe46OVqdP+xupjWm/VshUszbdbzanMc45U69NRXJT3HcVL0/+H6Rw8XH4E+85/8uxcrR3VxGchfkXpsylm5qPGT6eLsMnHXit4T",
        },
    ],
}
