"""The Choco Banana solver."""

from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_cc
from noqx.rule.helper import tag_encode, target_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import all_rect, no_rect
from noqx.solution import solver


def grid_src_same_color_connected(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to check the reachability of same color cells starting from a source.

    An adjacent rule and a grid fact should be defined first.
    """

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)

    r, c = src_cell
    initial = f"{tag}({r}, {c}, {r}, {c}).\n"
    propagation = f"{tag}({r}, {c}, R, C) :- {color}({r}, {c}), {tag}({r}, {c}, R1, C1), grid(R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1).\n"
    return initial + propagation.strip()


def bulb_src_same_color_connected(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells starting from a bulb.

    An adjacent rule and a grid fact should be defined first.
    """

    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)

    r, c = src_cell
    initial = f"{tag}({r}, {c}, {r}, {c})."
    bulb_constraint = f"{color}(R, C), adj_{adj_type}(R, C, R1, C1), (R - {r}) * (C - {c}) == 0"
    propagation = f"{tag}({r}, {c}, R, C) :- {color}({r}, {c}), {tag}({r}, {c}, R1, C1), {bulb_constraint}."
    return initial + "\n" + propagation


def count_reachable_src(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4):
    """
    Generate a constraint to count the reachable cells starting from a source.

    A grid_src_same_color_connected should be defined first.
    """
    src_r, src_c = src_cell

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    rop, num = target_encode(target)

    return f":- {color}({src_r}, {src_c}), {{ {tag}({src_r}, {src_c}, R, C) }} {rop} {num}."


def count_rect_src(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a cell-relevant constraint for shikaku.

    A bulb_src_color_connected rule should be defined first.
    """
    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {color}({src_r}, {src_c}), {count_r}, {count_c}, CR * CC != {target}."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_cc(["gray", "white"]))
    solver.add_program_line(adjacent())
    solver.add_program_line(all_rect(color="gray"))
    solver.add_program_line(no_rect(color="white"))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(grid_src_same_color_connected(src_cell=(r, c), color="white"))
        solver.add_program_line(count_reachable_src(num, src_cell=(r, c), color="white"))
        solver.add_program_line(bulb_src_same_color_connected(src_cell=(r, c), color="gray"))
        solver.add_program_line(count_rect_src(num, src_cell=(r, c), color="gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Choco Banana",
    "category": "shade",
    "aliases": ["chocobanana"],
    "examples": [
        {
            "data": "m=edit&p=7VRNb+IwFLznV1Q++xDH+fSNpdALZUthhVAUIaBZERWUXUKqlaP8d957iRqDuPSwWyqtjCfDePwysRMXv8vVIeXCxp8MOVyhuSKk7oQ+dbtts+y4S9Ud75XHbX4Awvn34ZD/XO2K1IpbV2JVOlJ6wvWDiplgnDnQBUu4nqhKPyo95noKQ4wL0EaNyQE66OicxpH1G1HYwMctB7oAuskOm126HDXKk4r1jDO8zzeajZTt87eUtTnw/ybfrzMU1qsjPEyxzX61I0X5kr+WrVckNde9Ju70SlzZxUXaxEV2JS4+xV+OGyV1Dcv+DIGXKsbsPzoadnSqKsCxqpgUONWFLM3eMOmj4BtChELYCW6AQtAJvnPh8KmGUTSgGoYQXt5F2GSJDEWQB16ad8UhjzlLSlQ8Q3HDizDCozrSVKiOWdl3zxRYHEFLtCAcEjqEM1hBriXhPaFN6BGOyDMgnBP2CV1CnzwB7sGHdukfxIll88mfN+/raYkVw8lTW+wPox5LPMj+H0afdBjhFti39rLfWhz4/BLrBA==",
        },
    ],
}
