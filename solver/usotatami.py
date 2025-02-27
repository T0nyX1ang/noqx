"""The Uso-tatami solver."""

from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, count_reachable_src
from noqx.rule.shape import all_rect_region, avoid_region_border_crossover
from noqx.solution import solver


def rect_constraint() -> str:
    """Generate a cell relevant constraint for rectangles with the width/height of 1."""
    return ":- upleft(R, C), left(R + 1, C), up(R, C + 1)."


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    fail_false(len(puzzle.text) > 0, "No clues found.")
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(all_rect_region())
    solver.add_program_line(rect_constraint())
    solver.add_program_line(avoid_region_border_crossover())
    solver.add_program_line(f":- {{ upleft(R, C) }} != {len(puzzle.text)}.")

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        solver.add_program_line(f"clue({r}, {c}).")
        solver.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

        if isinstance(num, int):
            solver.add_program_line(count_reachable_src(("ne", num), (r, c), main_type="bulb", color=None, adj_type="edge"))

    for (r, c, d, _), draw in puzzle.edge.items():
        solver.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
    solver.add_program_line(f":- clue(R, C), clue(R1, C1), (R, C) != (R1, C1), {tag}(R, C, R, C1), {tag}(R1, C1, R, C1).")
    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))

    return solver.program


__metadata__ = {
    "name": "Uso-tatami",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VVdb9owFH3Pr6j8fB9i59svE+tgL4xuK1NVRREKNFujgdIRMlVG/Pce36QN0mDVhsReJstHx+fa5vjG19Q/mnxdUIzmxeSSRPN8xV25CXe3a9Nysyz0BQ2azX21BiG6Go3oa76sCyftZmXO1iTaDMi816lQgrhLkZH5pLfmgzYTMtcICZLQxmBSkAId9vSG45ZdtqJ0wScdB70FXZTrxbKYjVvlo07NlIT9nbe82lKxqn4Wol3G40W1mpdWmOcbHKa+Lx+6SN3cVd+bbq7MdmQGrd3hAbteb9fS1q5lB+zaU5xst7j7VtTN/JDXJNvtkPPPcDvTqTX+padxT6/1FjjRW6FCu/QNjLQfRqjICtGeEFsh3BMSKwS94LlW8PcEaQVvT1BWwMd/Ebzn7LIAM5It3TKOGBXjFI7JeIzvGF3GgHHMc4aMN4yXjD5jyHMie+Y/ysrpdpACX+gkxumCmGSEDHmvWkxVyDXXt+C848xJxRC362JSrVf5Ejds0qzmxfp5jHreOeJRcE89LPH/l/i/KHGbf/fMV/rUCkuR2pdqIHNF4qGZ5bNFhXuG/LXhCP86MW7QkXCsSCZ4aI6EgwSbI0dHwiE2j45vHqICIjxafxn+/eavWDvl3Hhqfgmc/dvj9RJNXW3yTb4qReY8AQ=="
        },
        {"url": "https://puzz.link/p?usotatami/8/8/7b23b6b4b2f2d4a21a2b4b3a3e8e5b3b2b32b3", "test": False},
    ],
}
