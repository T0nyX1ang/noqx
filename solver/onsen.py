"""The Onsen-Meguri solver."""

from typing import Iterable, List, Tuple, Union

from .core.common import area, direction, display, fill_path, grid, shade_c
from .core.penpa import Puzzle
from .core.helper import full_bfs
from .core.loop import single_loop
from .core.neighbor import adjacent
from .core.solution import solver


def area_border(_id: int, ar: Iterable[Tuple[int, int]]) -> str:
    """Generates a fact for the border of an area."""
    borders = []
    for r, c in ar:
        for dr, dc, d in ((0, -1, "l"), (-1, 0, "u"), (0, 1, "r"), (1, 0, "d")):
            r1, c1 = r + dr, c + dc
            if (r1, c1) not in ar:
                borders.append(f'area_border({_id}, {r}, {c}, "{d}").')
    rule = "\n".join(borders)
    return rule


def onsen_rule(target: Union[int, str], _id: int, area_id: int, r: int, c: int) -> str:
    """
    Generates a rule for an Onsen-Meguri puzzle.

    An area fact, a grid direction fact and an area border fact should be defined first.
    """
    mutual = "area_border(A, R, C, D), grid_direction(R, C, D)"

    rule = f"onsen({_id}, {r}, {c}).\n"
    rule += f"onsen({_id}, R, C) :- grid(R, C), adj_loop(R, C, R1, C1), onsen({_id}, R1, C1).\n"

    if target != "?":
        num = int(target)
        rule += f":- area(A, R, C), onsen({_id}, R, C), #count {{ R1, C1: area(A, R1, C1), onsen({_id}, R1, C1) }} != {num}."
    else:
        anch = f"#count {{ R1, C1: area({area_id}, R1, C1), onsen({_id}, R1, C1) }} = N"  # set anchor number for clue
        rule += (
            f":- area(A, R, C), onsen({_id}, R, C), {anch}, #count {{ R1, C1: area(A, R1, C1), onsen({_id}, R1, C1) }} != N."
        )

    # any area, go through border at least twice
    rule += f":- area(A, _, _), #count {{ R, C, D: grid(R, C), {mutual} }} < 2.\n"

    # any area, any onsen area, go through border at most twice
    rule += f":- area(A, _, _), onsen(O, _, _), #count {{ R, C, D: onsen(O, R, C), {mutual} }} > 2.\n"

    rule += ":- onsen_loop(R, C), not onsen(_, R, C).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="onsen_loop"))
    solver.add_program_line(fill_path(color="onsen_loop"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(single_loop(color="onsen_loop"))

    onsen_id = 0
    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(area_border(i, ar))

        for rc in ar:
            if rc in puzzle.text:
                r, c = rc
                data = puzzle.text[rc]
                solver.add_program_line(f"onsen_loop({r}, {c}).")
                solver.add_program_line(onsen_rule(data if isinstance(data, int) else "?", onsen_id, i, r, c))

                onsen_id += 1  # fix multiple onsen clues in an area, onsen_id and area_id may be different now

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
