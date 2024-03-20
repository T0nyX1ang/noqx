"""The Haisu solver."""

from typing import List, Tuple

from . import utils
from .utils.encoding import Encoding
from .utils.regions import full_bfs
from .utilsx.fact import area, direction, display, grid
from .utilsx.loop import fill_path, connected_path, directed_loop
from .utilsx.rule import adjacent
from .utilsx.solution import solver


def area_border(_id: int, ar: list) -> str:
    """Generates a fact for the border of an area."""
    borders = []
    for r, c in ar:
        for dr, dc, d in ((0, -1, "l"), (-1, 0, "u"), (0, 1, "r"), (1, 0, "d")):
            r1, c1 = r + dr, c + dc
            if (r1, c1) not in ar:
                borders.append(f'area_border({_id}, {r}, {c}, "{d}").')
    rule = "\n".join(borders)
    return rule


def fully_reachable_path(color: str) -> str:
    """Generate a fully-propagated reachable path."""
    initial = f"fully_reachable_path(R, C, R, C) :- grid(R, C), {color}(R, C).\n"
    propagation = f"fully_reachable_path(R0, C0, R, C) :- fully_reachable_path(R0, C0, R1, C1), grid(R, C), {color}(R, C), adj_loop(R, C, R1, C1).\n"
    return initial + propagation


def haisu_count(target: int, _id: int, dest: Tuple[int, int]) -> str:
    """
    Generate a rule that counts the number that a path passes through an area.

    A direction fact and a grid_in should be defined first.
    """
    dest_r, dest_c = dest
    constraint = f":- #count {{ R, C: area_border({_id}, R, C, D), grid_in(R, C, D), fully_reachable_path(R, C, {dest_r}, {dest_c}) }} != {target}."
    return constraint


def encode(string: str) -> Encoding:
    return utils.encode(string, has_borders=True, clue_encoder=lambda x: int(x) if x.isnumeric() else x)


def solve(E: Encoding) -> List:
    if not ("S" in E.clues.values() and "G" in E.clues.values()):
        raise ValueError("S and G squares must be provided.")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("haisu(R, C) :- grid(R, C).")
    solver.add_program_line(fill_path(color="haisu", directed=True))
    solver.add_program_line(adjacent(_type="loop_directed"))
    solver.add_program_line(directed_loop(color="haisu", path=True))

    clue_index = {}
    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(area_border(i, ar))
        for r, c in ar:
            if (r, c) in E.clues:
                clue_index[(r, c)] = i

    for (r, c), clue in E.clues.items():
        if clue == "S":
            sr, sc = r, c
        elif clue == "G":
            gr, gc = r, c
        else:
            solver.add_program_line(haisu_count(int(clue), _id=clue_index[(r, c)], dest=(r, c)))

    solver.add_program_line("test(R, C, D) :- area_border(0, R, C, D), grid_in(R, C, D), fully_reachable_path(R, C, 2, 2).")

    solver.add_program_line(connected_path((sr, sc), (gr, gc), color="haisu", directed=True, only_one=True))
    solver.add_program_line(fully_reachable_path("haisu"))

    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
