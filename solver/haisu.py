"""The Haisu solver."""

from typing import Iterable, List, Tuple

from .core.common import area, direction, display, fill_path, grid
from .core.helper import full_bfs
from .core.loop import directed_loop
from .core.penpa import Puzzle, Solution
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


def solve(puzzle: Puzzle) -> List[Solution]:
    assert "S" in puzzle.text.values() and "G" in puzzle.text.values(), "S and G squares must be provided."

    solver.reset()
    solver.register_puzzle(puzzle)
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
        solver.add_program_line(area_border(i, ar))

        for r, c in ar:
            if puzzle.text.get((r, c)) == "S":
                s_index = ar

    for (r, c), clue in puzzle.text.items():
        if clue == "S":
            solver.add_program_line(f"path_start({r}, {c}).")
        elif clue == "G":
            solver.add_program_line(f"path_end({r}, {c}).")
        else:
            assert isinstance(clue, int), "Clue should be an integer."
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
            "data": "m=edit&p=7ZRNb9pAEIbv/Ipoz3Pw2l7b6xtNaS6EfkAVRZYVGeIWq1BawFVkxH/PO+MldiSkqkpV5VAZD+98wTO7a+9+1sW2pBhXkJBHGlfghXJHHn9O16zar8r0gob1frnZQhC9n9CXYrUrB5krygeHxqbNkJqrNFNakfJxa5VT8zE9NNdpM6JmipQijdi4LfIhR528kTyryzaoPeiJ05C3kItqu1iVd+M28iHNmhkp/p830s1SrTe/SuU42F9s1vOKA/Nij1l2y+qHy+zq+8232tXq/EjNsMUdn8ENOlyWLS6rM7g8xYtxV9X38uEcqc2PR6z4J7DepRljf+5k0slpeoCdpAcVRGjlPZZNUUECN3hyQ3bVFJAuYLxnecN5/8mN/GfZmIu7bMxZddX9WMKBLp+EPRTgaYG8FftOrC92hhmoCcS+FeuJNWLHUjPCaDowpEPM5+MXcZZ1aFsdRqRN7LQlHYGTtYmhMRFrnHMda6fRG7veGIDMLRq91vUmmMMGrbYe+Z7rtQE0BoNGjHzd9iIGbdz/gtM4TtNjYx5eYdFgMI7B9JiZMzpxgo23QHhQn7j6pMcJNm1PbKi3rt72+bGFtmXGNzRzYlFvZGkvxYZiI1nymA/VHx27l+/ub3EyH+S9C2v8t718kKkxHsWLyWa7LlZ4IEf3X3vepF7Py+3Jx6vwOFAPSm55SsL/b8d//3bk1fde22F9bTh4fNSyqHa1ygeP",
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
