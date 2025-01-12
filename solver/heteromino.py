"""The Heteromino solver."""

from typing import List

from noqx.puzzle import Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false, tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, general_shape
from noqx.solution import solver


def avoid_adj_same_omino(color: str = "black") -> str:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An split by edge rule, an omino rule should be defined first.
    """
    t_be = tag_encode("belong_to_shape", "omino", 3, color)
    constraint = "split_by_edge(R, C, R + 1, C) :- grid(R, C), grid(R + 1, C), edge_top(R + 1, C).\n"
    constraint += "split_by_edge(R, C, R, C + 1) :- grid(R, C), grid(R, C + 1), edge_left(R, C + 1).\n"
    constraint += "split_by_edge(R, C, R1, C1) :- split_by_edge(R1, C1, R, C).\n"
    constraint += f":- grid(R, C), grid(R1, C1), {t_be}(R, C, T, V), {t_be}(R1, C1, T, V), split_by_edge(R, C, R1, C1)."
    return constraint


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)

    fail_false((puzzle.row * puzzle.col - len(puzzle.surface)) % 3 == 0, "The grid cannot be divided into 3-ominoes!")
    solver.add_program_line(defined(item="hole"))
    solver.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(all_shapes("omino_3", color="grid"))
    solver.add_program_line(avoid_adj_same_omino(color="grid"))

    for i, o_shape in enumerate(OMINOES[3].values()):
        solver.add_program_line(general_shape("omino_3", i, o_shape, color="grid", adj_type="edge"))

    for (r, c, _, _), color in puzzle.surface.items():
        solver.add_program_line(f"hole({r}, {c}).")

        for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
            prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
            direc = "left" if c1 != c else "top"
            solver.add_program_line(f"{prefix}edge_{direc}({r2}, {c2}).")

    for (r, c, d, _), draw in puzzle.edge.items():
        solver.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Heteromino",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7ZhBbxs3E4bv/hXBnnlYcsjh7t7c1O7FddraRRAIgqEoSmNUhlLbKoo1/N/D5TyCD5XxtUmb4gMESeQsZ4acd95Zcld3v20XtysX0vSVzrXOl0/fdfUXQ1t/u8/l9f16Nbxwx9v7D5vbIjj36vTUvV+s71ZHM6zmRw9jP4zHbvxumDWhcfXnm7kbfxwexu+H8cKNF0XVuFjGzorkGxeKePIkvq76SXppg74t8jlyEd8UcXl9u1yvrs5s5IdhNl66Zlrnm+o9ic3N5vdVY271erm5eXs9Dbxd3Bcwdx+uP6K5277b/LrF1s8f3Xhs4Z7sCVeewp1EC3eS9oQ7ofiXw+3nj48l7T+VgK+G2RT7z09i9yReDA+Nds0QXaN97bK3Llgn1sXa9abrTden2vlW6W0C71t6M/OB62DePuzGbW4fmCdYHD4wj+An+AnrSLY+oo+7a/ySBesT8yb8EnbKfEocShyKH4nwGb9MXB32vc0TWhsP3uyCZxy8Idh8AXwBXEG4BkcQxqPNH6LFEyL+4AuR9ZLFHxL24A3gDAk78ATFPxMXeEJm3Q49fIbe9NLaOtLaOtLafAKv4i1O8btxW1/gV8AvweYX+BVBL/gLduRFyIfAr0TiAKfAo4BT4FPgU5Q4wC3Ut1DZQjEL+KVjnY54yId0+PWM9/iRp0h+Ymv6SF4i+Yje/CP5iOCP1EEkDxGcEf4j/Ef4j5H1qINInceEH3Ue4T+Sjwj+SD1HbumYGe+wo64j+CP1nVqbP1Hnifs7cX8n+E/gTd7iSB67YPEk8Cb4TvCcqP8E3hSxh+cEzwk8CX6T4g++BJ8pMw6O1LEu21UCl4JL2bcU3hQ8Cg6FP4U/pY6VfUmpS4U3BYfCm3K/KvepJvTgUmUe8Cn7kLLnKrgUvpR6VfhS6lTBpz0bOPWYW9Nn8GXwZe7TzD6V4SeDK8NThqcshiODM4MzgzODM1OXeXeQ1P2znDHnw0NpfW3f1Pa0tqG2l+UgcqPU9tvatrVNtT2rNie1fV3bl7WNtdVqk6ej7C8edv9UOOU0mMqn7+r+WhI1Sb2K6yc2pMh9KHLJlPzPyGdqD1l/55MOHgePg8fB4//DY340ay62t+8Xy1V5Wzl598vqxfnm9maxbsrL4eNR80dTfzMpxvHwvvgfvS9OFLRf+SD90nN9VrJbXu36coSm8nrqxleu+bi9WlwtN+um/PfgdgalCrU88ew3EGnbZzX++Um/bNVi0PXTDJ9t8Flx7x5TnlPz5LJfPT3t7NdMT0R/0nz1aimPU/OjTw==",
        }
    ],
}
