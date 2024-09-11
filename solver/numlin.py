"""The Numberlink solver."""

from math import log2
from typing import Dict, List, Tuple, Union

from .core.common import direction, display, fill_path, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.loop import single_loop
from .core.neighbor import adjacent
from .core.helper import tag_encode
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


def clue_bit(r: int, c: int, _id: int, nbit: int) -> str:
    """Assign clues with bit ids instead of numerical ids."""
    rule = f"clue({r}, {c}).\n"
    for i in range(nbit):
        if _id >> i & 1:
            rule += f"clue_bit({r}, {c}, {i}).\n"
    return rule.strip()


def grid_bit_color_connected(nbit: int, color: str = "grid", adj_type: Union[int, str] = "loop") -> str:
    """Generate a constraint to check the reachability of {color} cells starting from a source (bit version)."""
    if type(adj_type) is int:
        adj_type = str(adj_type)
    tag = tag_encode("reachable", "grid", "bit", "adj", adj_type)
    rule = f"{{ {tag}(R, C, B) }} :- grid(R, C), {color}(R, C), bit_range(B).\n"
    rule += f"{tag}(R, C, B) :- clue_bit(R, C, B).\n"
    rule += f"not {tag}(R, C, B) :- grid(R, C), {color}(R, C), bit_range(B), clue(R, C), not clue_bit(R, C, B).\n"
    rule += f"{tag}(R, C, B) :- {tag}(R1, C1, B), grid(R, C), bit_range(B), {color}(R, C), adj_{adj_type}(R, C, R1, C1).\n"
    rule += f"not {tag}(R, C, B) :- not {tag}(R1, C1, B), grid(R, C), grid(R1, C1), bit_range(B), {color}(R, C), {color}(R1, C1), adj_{adj_type}(R, C, R1, C1).\n"
    return rule.strip()


def num_binary_range(num):
    """Generate a rule restricting number represented by bits between 0 and num."""
    nbit = int(log2(num)) + 1
    rule = f"bit_range(0..{nbit - 1}).\n"
    rule += "binary(0..1).\n"
    return rule.strip(), nbit


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

    tag = tag_encode("reachable", "grid", "bit", "adj", "loop")
    solver.add_program_line("numlin(R, C) :- clue(R, C).")
    solver.add_program_line("dead_end(R, C) :- clue(R, C).")
    solver.add_program_line(grid_bit_color_connected(nbit=nbit, adj_type="loop"))
    solver.add_program_line(f":- grid(R, C), not {tag}(R, C, _).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
