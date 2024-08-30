"""The Numberlink solver."""

from typing import Dict, List, Tuple, Union

from .core.common import direction, display, fill_path, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.loop import single_loop
from .core.neighbor import adjacent
from .core.helper import tag_encode
from .core.solution import solver


def no_2x2_path() -> str:
    """
    Generate a rule that no 2x2 path is allowed.

    A reachable path rule should be defined first.
    """
    points = ((0, 0), (0, 1), (1, 0), (1, 1))
    return f":- { ', '.join(f'reachable_grid_src_adj_loop_numlin(ID, R + {r}, C + {c})' for r, c in points) }."


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

    if puzzle.param["visit_all"]:
        solver.add_program_line("numlin(R, C) :- grid(R, C).")
    else:
        solver.add_program_line(shade_c(color="numlin"))

    if puzzle.param["no_2x2"]:
        solver.add_program_line(no_2x2_path())

    solver.add_program_line(fill_path(color="numlin"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(single_loop(color="numlin", path=True))

    for _id, (n, pair) in enumerate(locations.items()):
        r0, c0 = pair[0]
        r1, c1 = pair[1]
        solver.add_program_line(f"link_end({_id}, {r0}, {c0}).")
        solver.add_program_line(f"link_end({_id}, {r1}, {c1}).")

    tag = tag_encode("reachable", "grid", "src", "adj", "loop", "numlin")
    solver.add_program_line("numlin(R, C) :- link_end(_, R, C).")
    solver.add_program_line("dead_end(R, C) :- link_end(_, R, C).")
    solver.add_program_line(f"{tag}(ID, R, C) :- link_end(ID, R, C).")
    solver.add_program_line(f"{tag}(ID, R, C) :- {tag}(ID, R1, C1), link_end(ID, _, _), grid(R, C), adj_loop(R, C, R1, C1).")

    solver.add_program_line(f":- grid(R, C), numlin(R, C), not {tag}(_, R, C).")
    solver.add_program_line(f":- grid(R, C), numlin(R, C), {tag}(ID, R, C), {tag}(ID1, R, C), ID < ID1.")
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
