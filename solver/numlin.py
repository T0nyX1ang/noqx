"""The Numberlink solver."""

from typing import Dict, List, Tuple, Union

from .core.common import direction, display, fill_path, grid, shade_c
from .core.helper import tag_encode
from .core.loop import single_loop
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import avoid_unknown_src_bit, clue_bit, grid_bit_color_connected, num_binary_range
from .core.solution import solver


def no_2x2_path_bit() -> str:
    """
    Generate a rule that no 2x2 path (bit version) is allowed.

    A reachable path rule should be defined first.
    """
    points = ((0, 0), (0, 1), (1, 0), (1, 1))
    tag = tag_encode("reachable", "grid", "bit", "adj", "loop")
    rule = f"bit_same(R, C, B) :- grid(R, C), bit_range(B), { ', '.join(f'{tag}(R + {r}, C + {c}, B)' for r, c in points) }.\n"
    rule += (
        f"bit_no(R, C, B) :- grid(R, C), bit_range(B), { ', '.join(f'not {tag}(R + {r}, C + {c}, B)' for r, c in points) }.\n"
    )
    rule += "bit_same(R, C, B) :- bit_no(R, C, B).\n"
    rule += "no_2x2(R, C) :- grid(R, C), bit_range(B), not bit_same(R, C, B).\n"
    rule += "no_empty(R, C) :- grid(R, C), bit_range(B), not bit_no(R, C, B).\n"
    rule += ":- grid(R, C), no_empty(R, C), not no_2x2(R, C).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    locations: Dict[Union[int, str], List[Tuple[int, int]]] = {}
    for (r, c), clue in puzzle.text.items():
        assert isinstance(clue, (int, str)), "Invalid clue."
        locations[clue] = locations.get(clue, []) + [(r, c)]

    # check that puzzle makes sense
    assert len(locations) > 0, "The grid cannot be empty!"
    for n, pair in locations.items():
        assert len(pair) <= 2, f"There are more than two occurrences of {n}."
        assert len(pair) >= 2, f"There is only one occurrence of {n}."

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))

    rule, nbit = num_binary_range(len(locations.items()))
    solver.add_program_line(rule)

    if puzzle.param["visit_all"]:
        solver.add_program_line("numlin(R, C) :- grid(R, C).")
    else:
        solver.add_program_line(shade_c(color="numlin"))

    if puzzle.param["no_2x2"]:
        solver.add_program_line(no_2x2_path_bit())

    solver.add_program_line(fill_path(color="numlin"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(single_loop(color="numlin", path=True))

    for _id, (n, pair) in enumerate(locations.items()):
        r0, c0 = pair[0]
        r1, c1 = pair[1]
        solver.add_program_line(clue_bit(r0, c0, _id + 1, nbit))
        solver.add_program_line(clue_bit(r1, c1, _id + 1, nbit))

    solver.add_program_line("numlin(R, C) :- clue(R, C).")
    solver.add_program_line("dead_end(R, C) :- clue(R, C).")
    solver.add_program_line(grid_bit_color_connected(adj_type="loop"))
    solver.add_program_line(avoid_unknown_src_bit(adj_type="loop"))

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
