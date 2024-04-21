"""The Haisu solver."""

from typing import Dict, Iterable, List, Tuple

from .core.common import area, direction, display, fill_path, grid
from .core.encoding import Encoding
from .core.helper import full_bfs
from .core.loop import directed_loop
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


def adj_before() -> str:
    """Generate a rule to constrain adjacent connectivity."""
    adj = 'adj_before(R, C-1, R, C) :- grid(R, C), grid_in(R, C, "l").\n'
    adj += 'adj_before(R-1, C, R, C) :- grid(R, C), grid_in(R, C, "u").\n'
    adj += 'adj_before(R, C+1, R, C) :- grid(R, C), grid_in(R, C, "r").\n'
    adj += 'adj_before(R+1, C, R, C) :- grid(R, C), grid_in(R, C, "d").\n'
    return adj.strip()


def connected_directed_path(color: str = "white") -> str:
    """
    Generate a directed path rule to constrain connectivity.

    A grid fact, a loop/path fact and an adjacent loop rule should be defined first.
    """
    initial = "reachable_path(R, C) :- path_start(R, C).\n"
    propagation = f"reachable_path(R, C) :- {color}(R, C), reachable_path(R1, C1), adj_before(R1, C1, R, C).\n"
    constraint = f":- grid(R, C), {color}(R, C), not reachable_path(R, C)."
    return initial + propagation + constraint


def connected_destpath(color: str = "white") -> str:
    """
    Generate a path rule to constrain connectivity.

    A grid fact, a loop/path fact and an adjacent loop rule should be defined first.
    """
    tag = "reachable_destpath"
    initial = f"{{ {tag}(R0, C0, R, C) }} :- clue(R, C), grid(R0, C0).\n"
    initial = f"not {tag}(R0, C0, R, C) :- path_start(R0, C0), clue(R, C).\n"
    initial += f"{tag}(R, C, R, C) :- clue(R, C).\n"
    propagation = f"not {tag}(R0, C0, R, C) :- grid(R0, C0), clue(R, C), (R0, C0) != (R, C), adj_before(R1, C1, R0, C0), not {tag}(R1, C1, R, C).\n"
    propagation += f"{tag}(R0, C0, R, C) :- grid(R0, C0), clue(R, C), (R0, C0) != (R, C), adj_before(R1, C1, R0, C0), {tag}(R1, C1, R, C).\n"
    return initial + propagation.strip()


def haisu_rules() -> str:
    """
    Generate constriants for haisu
    """
    rule = "clue(R, C) :- num(R, C, _).\n"
    rule += "clue_area(A) :- clue(R, C), area(A, R, C).\n"
    rule += "area_max_num(A, N) :- clue_area(A), #max { N0 : area(A, R, C), num(R, C, N0) } = N.\n"
    rule += "area_possible_num(A, 0..N) :- clue_area(A), area_max_num(A, N).\n"
    return rule.strip()


def haisu_count_x() -> str:
    rule = "haisu_count(R, C, A, 0) :- path_start(R, C), clue_area(A).\n"
    rule += "area_in(A, R, C) :- area_border(A, R, C, D), grid_in(R, C, D).\n"
    rule += "haisu_count(R, C, A, N) :- clue_area(A), area_possible_num(A, N), grid(R, C), adj_before(R1, C1, R, C), haisu_count(R1, C1, A, N), not area_in(A, R, C).\n"
    rule += "haisu_count(R, C, A, N) :- clue_area(A), area_possible_num(A, N), grid(R, C), adj_before(R1, C1, R, C), haisu_count(R1, C1, A, N-1), area_in(A, R, C).\n"
    rule += ":- clue_area(A), grid(R, C), haisu_count(R, C, A, N1), haisu_count(R, C, A, N2), N1 < N2.\n"
    rule += ":- num(R, C, N), area(A, R, C), not haisu_count(R, C, A, N).\n"
    # rule += ":- area_in(A, R, C), area(A, R1, C1), clue(R1, C1), not reachable_destpath(R, C, R1, C1), not haisu_count(R, C, A, _).\n"
    # rule += ":- area_in(A, R, C), area(A, R1, C1), num(R1, C1, N1), not reachable_destpath(R, C, R1, C1), haisu_count(R, C, A, N0), N0 > N1.\n"
    return rule.strip()


def solve(E: Encoding) -> List[Dict[str, str]]:
    if not ("S" in E.clues.values() and "G" in E.clues.values()):
        raise ValueError("S and G squares must be provided.")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("haisu(R, C) :- grid(R, C).")
    solver.add_program_line(fill_path(color="haisu", directed=True))
    solver.add_program_line(directed_loop(color="haisu", path=True))
    solver.add_program_line(connected_directed_path(color="haisu"))
    solver.add_program_line(haisu_rules())
    solver.add_program_line(adj_before())
    solver.add_program_line(haisu_count_x())
    # solver.add_program_line(connected_destpath(color="haisu"))

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
            solver.add_program_line(f"path_start({r}, {c}).")
        elif clue == "G":
            solver.add_program_line(f"path_end({r}, {c}).")

    for (r, c), clue in E.clues.items():
        if clue not in ("S", "G"):
            solver.add_program_line(f"num({r}, {c}, {clue}).")

    solver.add_program_line(display(item="loop_sign", size=3))
    # print(solver.program)
    solver.solve()

    return solver.solutions
