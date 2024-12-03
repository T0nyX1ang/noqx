"""The Choco Banana solver."""

from typing import List, Tuple, Optional, Union

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_cc
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import all_rect, no_rect
# from noqx.rule.reachable import grid_src_color_connected, count_reachable_src
from noqx.rule.helper import tag_encode, target_encode
from noqx.solution import solver


def grid_src_same_color_connected(
    src_cell: Tuple[int, int],
    color_list: List,
    include_cells: Optional[List[Tuple[int, int]]] = None,
    exclude_cells: Optional[List[Tuple[int, int]]] = None,
    adj_type: Union[int, str] = 4,
) -> str:
    """
    Generate a constraint to check the reachability of same color cells starting from a source.

    An adjacent rule and a grid fact should be defined first.
    """

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type)

    r, c = src_cell
    initial = f"{tag}({r}, {c}, {r}, {c}).\n"

    if include_cells:
        initial += "\n".join(f"{tag}({r}, {c}, {inc_r}, {inc_c})." for inc_r, inc_c in include_cells) + "\n"

    if exclude_cells:
        initial += "\n".join(f"not {tag}({r}, {c}, {exc_r}, {exc_c})." for exc_r, exc_c in exclude_cells) + "\n"

    propagation = ""
    for color in color_list:
        propagation += f"{tag}({r}, {c}, R, C) :- {color}({r}, {c}), {tag}({r}, {c}, R1, C1), grid(R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1).\n"
    return initial + propagation.strip()


def count_reachable_src(
    target: Union[int, Tuple[str, int]],
    src_cell: Tuple[int, int],
    main_type: str = "grid",
    adj_type: Union[int, str] = 4,
):
    """
    Generate a constraint to count the reachable cells starting from a source.

    A grid_src_color_connected or bulb_src_color_connected should be defined first.
    """

    src_r, src_c = src_cell

    tag = tag_encode("reachable", main_type, "src", "adj", adj_type)
    rop, num = target_encode(target)

    return f":- {{ {tag}({src_r}, {src_c}, R, C) }} {rop} {num}."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_cc(["gray", "white"]))
    solver.add_program_line(adjacent())

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(grid_src_same_color_connected(src_cell=(r, c), color_list=["gray", "white"]))
        solver.add_program_line(count_reachable_src(target=int(num), src_cell=(r, c)))

    for (r0, c0), num0 in puzzle.text.items():
        for (r1, c1), num1 in puzzle.text.items():
            if (r0, c0) < (r1, c1) and num0 != num1:
                tag = tag_encode("reachable", "grid", "src", "adj", 4)
                solver.add_program_line(f"not {tag}({r0}, {c0}, {r1}, {c1}).")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(all_rect(color="gray"))
    solver.add_program_line(no_rect(color="white"))
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Choco Banana",
    "category": "shade",
    "aliases": ["cbanana"],
    "examples": [
        {
            "data": "m=edit&p=7VRNb+IwFLznV1Q++xDH+fSNpdALZUthhVAUIaBZERWUXUKqlaP8d957iRqDuPSwWyqtjCfDePwysRMXv8vVIeXCxp8MOVyhuSKk7oQ+dbtts+y4S9Ud75XHbX4Awvn34ZD/XO2K1IpbV2JVOlJ6wvWDiplgnDnQBUu4nqhKPyo95noKQ4wL0EaNyQE66OicxpH1G1HYwMctB7oAuskOm126HDXKk4r1jDO8zzeajZTt87eUtTnw/ybfrzMU1qsjPEyxzX61I0X5kr+WrVckNde9Ju70SlzZxUXaxEV2JS4+xV+OGyV1Dcv+DIGXKsbsPzoadnSqKsCxqpgUONWFLM3eMOmj4BtChELYCW6AQtAJvnPh8KmGUTSgGoYQXt5F2GSJDEWQB16ad8UhjzlLSlQ8Q3HDizDCozrSVKiOWdl3zxRYHEFLtCAcEjqEM1hBriXhPaFN6BGOyDMgnBP2CV1CnzwB7sGHdukfxIll88mfN+/raYkVw8lTW+wPox5LPMj+H0afdBjhFti39rLfWhz4/BLrBA==",
        },
    ],
}
