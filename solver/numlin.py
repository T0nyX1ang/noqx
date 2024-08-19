"""The Numberlink solver."""

from typing import Dict, List, Tuple, Union

from .core.common import direction, display, fill_path, grid, shade_c
from .core.penpa import Puzzle
from .core.loop import single_loop
from .core.neighbor import adjacent
from .core.reachable import avoid_unknown_src, grid_src_color_connected
from .core.solution import solver


def no_2x2_path() -> str:
    """
    Generate a rule that no 2x2 path is allowed.

    A reachable path rule should be defined first.
    """
    points = ((0, 0), (0, 1), (1, 0), (1, 1))
    return f":- { ', '.join(f'reachable_grid_src_adj_loop_numlin(R0, C0, R + {r}, C + {c})' for r, c in points) }."


def solve(puzzle: Puzzle) -> List[str]:
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

    for n, pair in locations.items():
        r0, c0 = pair[0]
        r1, c1 = pair[1]
        solver.add_program_line(f"numlin({r0}, {c0}).")
        solver.add_program_line(f"dead_end({r0}, {c0}).")
        solver.add_program_line(f"numlin({r1}, {c1}).")
        solver.add_program_line(f"dead_end({r1}, {c1}).")

        excluded = []
        for n1, pair1 in locations.items():
            if n1 != n:
                excluded.append(pair1[0])
                excluded.append(pair1[1])

        solver.add_program_line(
            grid_src_color_connected(
                (r0, c0), include_cells=[(r1, c1)], exclude_cells=excluded, color="numlin", adj_type="loop"
            )
        )

    solver.add_program_line(avoid_unknown_src(color="numlin", adj_type="loop"))
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
