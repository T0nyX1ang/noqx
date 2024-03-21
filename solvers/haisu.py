"""The Haisu solver."""

from typing import List, Tuple

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import area, direction, display, grid
from .utilsx.loop import directed_loop, fill_path
from .utilsx.region import full_bfs
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


def adj_connected() -> str:
    """Generate a rule to constrain adjacent connectivity."""
    adj = 'adj_connected(R0, C0, R, C) :- R=R0, C=C0+1, grid(R, C), grid(R0, C0), grid_in(R, C, "l").\n'
    adj += 'adj_connected(R0, C0, R, C) :- R=R0+1, C=C0, grid(R, C), grid(R0, C0), grid_in(R, C, "u").\n'
    adj += 'adj_connected(R0, C0, R, C) :- R=R0, C=C0-1, grid(R, C), grid(R0, C0), grid_in(R, C, "r").\n'
    adj += 'adj_connected(R0, C0, R, C) :- R=R0-1, C=C0, grid(R, C), grid(R0, C0), grid_in(R, C, "d").\n'
    adj += 'adj_connected(R, C, R0, C0) :- R=R0, C=C0+1, grid(R, C), grid(R0, C0), grid_out(R, C, "l").\n'
    adj += 'adj_connected(R, C, R0, C0) :- R=R0+1, C=C0, grid(R, C), grid(R0, C0), grid_out(R, C, "u").\n'
    adj += 'adj_connected(R, C, R0, C0) :- R=R0, C=C0-1, grid(R, C), grid(R0, C0), grid_out(R, C, "r").\n'
    adj += 'adj_connected(R, C, R0, C0) :- R=R0-1, C=C0, grid(R, C), grid(R0, C0), grid_out(R, C, "d").\n'
    return adj


def connected_directed_path(src_cell: Tuple[int, int], dest_cell: Tuple[int, int], color: str = "white") -> str:
    """
    Generate a directed path rule to constrain connectivity.

    A grid fact, a loop/path fact and an adjacent loop rule should be defined first.
    """
    src_r, src_c = src_cell
    dest_r, dest_c = dest_cell
    initial = f"reachable_path({src_r}, {src_c}).\n"
    initial += f"reachable_path({dest_r}, {dest_c}).\n"
    propagation = f"reachable_path(R, C) :- {color}(R, C), reachable_path(R1, C1), adj_connected(R, C, R1, C1).\n"
    constraint = f":- grid(R, C), {color}(R, C), not reachable_path(R, C)."
    return initial + propagation + constraint


def connected_destpath(src_cell: Tuple[int, int], dest_cell: Tuple[int, int], color: str = "white") -> str:
    """
    Generate a path rule to constrain connectivity.

    A grid fact, a loop/path fact and an adjacent loop rule should be defined first.
    """
    src_r, src_c = src_cell
    dest_r, dest_c = dest_cell
    tag = "reachable_destpath"
    initial = f"{tag}({dest_r}, {dest_c}, {dest_r}, {dest_c}).\n"
    initial += f"{tag}({src_r}, {src_c}, {dest_r}, {dest_c}).\n"
    propagation = (
        f"{tag}(R, C, {dest_r}, {dest_c}) :- {color}(R, C), {tag}(R1, C1, {dest_r}, {dest_c}), adj_connected(R, C, R1, C1)."
    )
    return initial + propagation


def haisu_count(target: int, _id: int, dest: Tuple[int, int]) -> str:
    """
    Generate a rule that counts the number that a path passes through an area.

    A direction fact and a grid_in should be defined first.
    """
    dest_r, dest_c = dest
    tag = "reachable_destpath"
    constraint = (
        f":- #count {{ R, C: area_border({_id}, R, C, D), grid_in(R, C, D), {tag}(R, C, {dest_r}, {dest_c}) }} != {target}."
    )
    return constraint


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True, clue_encoder=lambda x: int(x) if x.isnumeric() else x)


def solve(E: Encoding) -> List:
    if not ("S" in E.clues.values() and "G" in E.clues.values()):
        raise ValueError("S and G squares must be provided.")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("haisu(R, C) :- grid(R, C).")
    solver.add_program_line(fill_path(color="haisu", directed=True))
    solver.add_program_line(adj_connected())
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
            solver.add_program_line(f"dead_out({r}, {c}).")
        elif clue == "G":
            gr, gc = r, c
            solver.add_program_line(f"dead_in({r}, {c}).")

    for (r, c), clue in E.clues.items():
        if clue not in ("S", "G"):
            solver.add_program_line(connected_destpath((sr, sc), (r, c), color="haisu"))
            solver.add_program_line(haisu_count(int(clue), _id=clue_index[(r, c)], dest=(r, c)))

    solver.add_program_line(connected_directed_path((sr, sc), (gr, gc), color="haisu"))
    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
