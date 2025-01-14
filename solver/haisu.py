"""The Haisu solver."""

from typing import List

from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.loop import directed_loop
from noqx.rule.neighbor import area_border
from noqx.solution import solver


def adj_before() -> str:
    """Generate a rule to constrain adjacent connectivity."""
    adj = 'adj_before(R, C - 1, R, C) :- grid(R, C), grid_in(R, C, "l").\n'
    adj += 'adj_before(R - 1, C, R, C) :- grid(R, C), grid_in(R, C, "u").\n'
    adj += 'adj_before(R, C + 1, R, C) :- grid(R, C), grid_in(R, C, "r").\n'
    adj += 'adj_before(R + 1, C, R, C) :- grid(R, C), grid_in(R, C, "d").\n'
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


def haisu_rules() -> str:
    """Generate constriants for haisu."""
    rule = "clue(R, C) :- number(R, C, _).\n"
    rule += "clue_area(A) :- clue(R, C), area(A, R, C).\n"
    rule += "area_max_num(A, N) :- clue_area(A), #max { N0 : area(A, R, C), number(R, C, N0) } = N.\n"
    rule += "area_possible_num(A, 0..N) :- clue_area(A), area_max_num(A, N).\n"
    return rule.strip()


def haisu_count() -> str:
    """Partial sum method for haisu."""
    rule = "haisu_count(R, C, A, 0) :- path_start(R, C), clue_area(A).\n"
    rule += "area_in(A, R, C) :- area_border(A, R, C, D), grid_in(R, C, D).\n"
    rule += "haisu_count(R, C, A, N) :- clue_area(A), area_possible_num(A, N), grid(R, C), adj_before(R1, C1, R, C), haisu_count(R1, C1, A, N), not area_in(A, R, C).\n"
    rule += "haisu_count(R, C, A, N) :- clue_area(A), area_possible_num(A, N), grid(R, C), adj_before(R1, C1, R, C), haisu_count(R1, C1, A, N - 1), area_in(A, R, C).\n"
    rule += ":- clue_area(A), grid(R, C), haisu_count(R, C, A, N1), haisu_count(R, C, A, N2), N1 < N2.\n"
    rule += ":- number(R, C, N), area(A, R, C), not haisu_count(R, C, A, N).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)

    fail_false("S" in puzzle.text.values() and "G" in puzzle.text.values(), "S and G squares must be provided.")
    solver.add_program_line(defined(item="number", size=3))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("haisu(R, C) :- grid(R, C).")
    solver.add_program_line(fill_path(color="haisu", directed=True))
    solver.add_program_line(directed_loop(color="haisu", path=True))
    solver.add_program_line(connected_directed_path(color="haisu"))
    solver.add_program_line(haisu_rules())
    solver.add_program_line(adj_before())
    solver.add_program_line(haisu_count())

    s_index = []
    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))

        for r, c in ar:
            if puzzle.text.get(Point(r, c, Direction.CENTER, "normal")) == "S":
                s_index = ar

    for (r, c, d, pos), clue in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        if clue == "S":
            solver.add_program_line(f"path_start({r}, {c}).")

        if clue == "G":
            solver.add_program_line(f"path_end({r}, {c}).")

        if isinstance(clue, int):
            solver.add_program_line(f"number({r}, {c}, {clue - 1 if (r, c) in s_index else clue}).")  # special case

    solver.add_program_line(display(item="grid_in", size=3))
    solver.add_program_line(display(item="grid_out", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Haisu",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7ZRNb9pAEIbv/Ipoz3Pw2l7b60tFU8iF0g+oosiyIiBusQqlBVxFRvz3vDNeYkdCqqpEVQ6V8fDOFzyzu/buVzXbFhTjChLySOMKvFDuyOPP6ZqW+1WRXlC/2i83WwiiD8MhfZ2tdkUvc1V571DbtO5TfZVmSitSPm6tcqo/pYf6fVoPqJ4gpUgjNmqKfMhBK68lz+qyCWoPeuw05A3kotwuVsXtqIl8TLN6Sor/5610s1Trze9COQ72F5v1vOTAfLbHMLtl+dNldtXd5nvlanV+pLrf4I7O4AYtLssGl9UZXJ7i2bir8kdxf47U5scjVvwzWG/TjLG/tDJp5SQ9wI7TgwoitPImy6aoIIEbPLohu2oCSBcw3pO84bz/6EacVW/a8sh/Uh5zvi2POauu2vKEA20+CTts4NVCfSN2KNYXO8VQVAdi34n1xBqxI6kZYFYdGNIhBvbxizjdOrSNDiPSJnbakuY5WJsYGiOyxsnXsXYavbHrjQHI3KLRa11vgjls0Gjrke+5XhtAYzBoxMjXTS9i0Mb9LziN4zQdNubhJRcNBuMYTIeZOaMTJ9h4C4QH9YmrTzqcYNP2xIZ66+ptlx9baBtmfEMzJxb1Wpb2UmwoNpIlj/mU/dU5fP7u/hEn80HeubDGL+3lvUyN8GxejDfb9WyFJ3Rw963jjav1vNiefLwbjz11r+SWpyT8/7r8969LXn3vtR3W14aDx0ctZ+WuUnnvAQ==",
        },
        {
            "url": "https://puzz.link/p?haisu/9/9/199103msp7vvv4pre00bs6poj0068sr1ugp2g2g2g2u2g2k2k2g2u2g2g2g2p",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?haisu/13/9/5948l0l2la55d8220gg44110000vg305c0cc00000000fvol3t1k3h25g5y5r6i7jao5zq",
            "test": False,
        },
    ],
}
