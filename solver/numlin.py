"""The Numberlink solver."""

from math import log2
from typing import Dict, List, Tuple, Union

from .core.common import direction, display, fill_path, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.loop import single_loop
from .core.neighbor import adjacent
from .core.helper import tag_encode
from .core.solution import solver


def no_2x2_path(nbit: int) -> str:
    """
    Generate a rule that no 2x2 path is allowed.

    A reachable path rule should be defined first.
    """
    points = ((0, 0), (0, 1), (1, 0), (1, 1))
    rule = f"bit_feat(R, C, B) :- grid(R, C), bitrange(B), { ', '.join(f'reachable_grid_src_adj_loop_bit(R + {r}, C + {c}, B)' for r, c in points) }.\n"
    rule += f"bit_feat(R, C, B) :- grid(R, C), bitrange(B), { ', '.join(f'not reachable_grid_src_adj_loop_bit(R + {r}, C + {c}, B)' for r, c in points) }.\n"
    rule += f":- grid(R, C), #count{{ B: bitrange(B), bit_feat(R, C, B) }} = {nbit}.\n"
    return rule.strip()


def clue_bit(r: int, c: int, id: int, nbit: int) -> str:
    rule = ""
    for i in range(nbit):
        if id >> i & 1:
            rule += f"clue_bit({r}, {c}, {i}).\n"
    return rule.strip()


def different_area_connected(tag: str, color: str = "grid"):
    tag_decoded = tag.split("_")
    adj_type = tag_decoded[tag_decoded.index("adj") + 1]
    rule = f"{tag}(R, C, B) :- clue_bit(R, C, B).\n"
    rule += f"not {tag}(R, C, B) :- grid(R, C), bitrange(B), clue_bit(R, C, _), not clue_bit(R, C, B).\n"
    rule += f"{tag}(R, C, B) :- {tag}(R1, C1, B), bitrange(B), {color}(R, C), adj_{adj_type}(R, C, R1, C1).\n"
    rule += f"not {tag}(R, C, B) :- not {tag}(R1, C1, B), bitrange(B), {color}(R, C), adj_{adj_type}(R, C, R1, C1).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    locations: Dict[Union[int, str], List[Tuple[int, int]]] = {}
    for (r, c), clue in puzzle.text.items():
        assert isinstance(clue, (int, str)), "Invalid clue."
        locations[clue] = locations.get(clue, []) + [(r, c)]

    # check that puzzle makes sense
    assert len(locations) > 0, "Error: The grid is empty!"
    for n, pair in locations.items():
        assert len(pair) <= 2, f"Error: There are more than two occurrences of {n}."
        assert len(pair) >= 2, f"Error: There is only one occurrence of {n}."

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))

    nbit = int(log2(len(locations.items()))) + 1
    solver.add_program_line(f"bitrange(0..{nbit - 1}).")

    if puzzle.param["visit_all"]:
        solver.add_program_line("numlin(R, C) :- grid(R, C).")
    else:
        solver.add_program_line(shade_c(color="numlin"))

    if puzzle.param["no_2x2"]:
        solver.add_program_line(no_2x2_path(nbit))

    solver.add_program_line(fill_path(color="numlin"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(single_loop(color="numlin", path=True))

    for _id, (n, pair) in enumerate(locations.items()):
        r0, c0 = pair[0]
        r1, c1 = pair[1]
        solver.add_program_line(clue_bit(r0, c0, _id + 1, nbit))
        solver.add_program_line(clue_bit(r1, c1, _id + 1, nbit))

    solver.add_program_line("numlin(R, C) :- clue_bit(R, C, _).")
    solver.add_program_line("dead_end(R, C) :- clue_bit(R, C, _).")
    tag = tag_encode("reachable", "grid", "src", "adj", "loop", "bit")
    solver.add_program_line(different_area_connected(tag))

    solver.add_program_line(f":- grid(R, C), numlin(R, C), not {tag}(R, C, _).")
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
