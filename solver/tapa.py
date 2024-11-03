"""The Tapa solver."""

import itertools
from typing import List, Tuple, Union

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def parse_shading(shading: List[bool]) -> List[int]:
    """
    Returns the Tapa clue that a ring of 8 cells corresponds to, digits sorted in increasing order.
    For example, shading = [T,F,T,T,T,F,F,T] should output [2, 3].
    As a special case, outputs [0] if shading is all False.
    """
    if all(shading):  # shading is all True
        return [8]

    # rotate so that the first spot is False
    idx = shading.index(False)
    shading = shading[idx:] + shading[:idx]

    # now `clue` is the lengths of consecutive runs of `True` in shading
    clue = []
    curr_num = 0
    for b in shading:
        if b:  # shaded, add to shaded string
            curr_num += 1
        else:  # unshaded, end current shaded string
            if curr_num > 0:
                clue.append(curr_num)
            curr_num = 0
    if curr_num > 0:  # add last string
        clue.append(curr_num)

    if not clue:
        clue = [0]
    return sorted(clue)


def generate_patterns(pattern: List[Union[int, str]]) -> List[Tuple[int]]:
    """Generate patterns given numbers and '?'."""
    result = [pattern]
    num_max = 9 - len(pattern) * 2
    for i, patt in enumerate(pattern):
        if patt == "?":  # replace '?' with all possible number combinations
            old_result = result
            result = []
            for patt in old_result:
                new_patt: List[List[int]] = []
                for num in range(1, num_max + 1):
                    tmp = patt.copy()
                    tmp[i] = num
                    new_patt.append(tmp)  # type: ignore
                result.extend(new_patt)
    new_result: List[Tuple[int]] = [tuple(sorted(patt)) for patt in result if sum(patt) + len(patt) <= 8]  # type: ignore
    return list(set(new_result))


def color_to_num(r: int, c: int, color: str = "black") -> str:
    "Map the color to a number."
    rule = f"num(R, C, N) :- -1 <= R, R <= {r}, -1 <= C, C <= {c}, not grid(R, C), N = 0.\n"
    rule += f"num(R, C, N) :- grid(R, C), not {color}(R, C), N = 0.\n"
    rule += f"num(R, C, N) :- grid(R, C), {color}(R, C), N = 1."
    return rule


def tapa_rules() -> str:
    "Generate tapa rules."
    valid_tapa: List[str] = []
    for shading in itertools.product([True, False], repeat=8):
        tapa_clue = parse_shading(list(shading))
        tapa_var = ", ".join(map(str, tapa_clue))
        shading_var = ", ".join(map(str, map(int, shading)))
        valid_tapa.append(f"valid_tapa({tapa_var}, {shading_var}).")
    return "\n".join(valid_tapa)


def valid_tapa_pattern(r: int, c: int, patterns: List[Tuple[int]]) -> str:
    "Generate valid tapa patterns."
    valid_pattern, num_str, num_constrain = [], [], []
    for i, (dr, dc) in enumerate(((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))):
        num_str.append(f"N{i}")
        num_constrain.append(f"num({r + dr}, {c + dc}, N{i})")
    num_str = ", ".join(num_str)
    num_constrain = ", ".join(num_constrain)
    for pattern in patterns:
        clue_str = ", ".join(map(str, pattern))
        rule = f"not valid_tapa({clue_str}, {num_str})"
        valid_pattern.append(rule)
    valid_pattern = ", ".join(valid_pattern)
    return f":- {valid_pattern}, {num_constrain}."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(color_to_num(puzzle.row, puzzle.col, color="black"))
    solver.add_program_line(tapa_rules())
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), clue in puzzle.text.items():
        assert isinstance(clue, list), "Please set all NUMBER to tapa sub."
        patterns = generate_patterns(clue)
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(valid_tapa_pattern(r, c, patterns))

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Tapa",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVda9swFH3Pryh6vg/6sBzbLyPtmr1k2UcySjGmOJlLwxKcOfEYCvnvvbryZtkJY2NQ+hCMDyfH50rnKrK1+17nVQFSgAhARcABGUQqBD1ELoR0wJtrvtqvi+QKRvX+qayQAHwYj+ExX++KQdq4ssHBxIkZgXmXpEwwYBJvwTIwn5KDeZ+YKZgZPmIQoDZxJon0tqV39NyyGycKjnyKPECO9B7pclUt18XDxCkfk9TMgdl5rqnaUrYpfxSsyWF/L8vNYmWFRb7HZnZPq23zZFd/Lb/VjVdkRzAjF3d2Jq5q41rq4lp2Jq7t4v/jrrfluaBxdjzign/GqA9JalN/aWnU0llyQJwmB6ZDW/oGUwCmw/F0ZAX8k34JEQmqFWLREwRXpPiSoCrcL54mqVBKbzahGs2XApI6paGb058hJFt3hmE/vIhPo8XUsqdI7hSvTvK4n0uqocvlS+TCHlpJn6aXmmxe2zKksfwMIXn8qmF/nWXkEnihFKfp7GvwW6FmfI8gj59SCRqpo7iGfUnp/kgBlXmNKO3W11Nca/44Ee9XRVTlr5E62WYqpuk7Sndo3MKCNvI94ZhQEs5xn4NRhG8JOaEmnJDnlvCO8IYwIAzJM7Rvyj+9Sy8QJ9X4Df7LS1+cF+efrmyQslldPebLAs+Sab1ZFNXVtKw2+ZrhsX0csJ+M7lShPbic5C9+ktvF56/tG/Ta4uBXke3zbc6ywTM=",
        },
    ],
}
