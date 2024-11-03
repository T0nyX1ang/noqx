"""The Heteromino solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import extract_initial_edges, tag_encode
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


def solve(puzzle: Puzzle) -> List[Solution]:
    shaded = len(puzzle.surface)
    assert (puzzle.row * puzzle.col - shaded) % 3 == 0, "The grid cannot be divided into 3-ominoes!"

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(extract_initial_edges(puzzle.edge, puzzle.helper_x))

    for (r, c), color_code in puzzle.surface.items():
        solver.add_program_line(f"hole({r}, {c}).")

        for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
            prefix = "not " if ((r1, c1), color_code) in puzzle.surface.items() else ""
            direc = "left" if c1 != c else "top"
            solver.add_program_line(f"{prefix}edge_{direc}({r2}, {c2}).")

    for i, o_shape in enumerate(OMINOES[3].values()):
        solver.add_program_line(general_shape("omino_3", i, o_shape, color="grid", adj_type="edge"))

    solver.add_program_line(all_shapes("omino_3", color="grid"))
    solver.add_program_line(avoid_adj_same_omino(color="grid"))
    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Heteromino",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7ZfPbtw2EMbv+xSBzjqInOFQ0s1N7V4c949dBMFiEWycTWPUxrZrb1HI8LuH4vwWvvjQHtqmwEKr4YicGc7Hb0Su7n/fr3ebNqb5J33btaFcQ9/XW2NX78N1dfNwuxlftSf7h8/bXVHa9vuzs/bT+vZ+s1hitVo8TsM4nbTTd+OyiU1b79Cs2unH8XF6M06X7XRZhppWS9950ULTxqKePqtv6/isvfbO0BX9Ar2o74p6fbO7vt28P/eeH8bldNU28zzfVO9Zbe62f2wad6vP19u7Dzdzx4f1QwFz//nmN0bu9x+3v+6xDaundjrxdE9fSFee051VT3fWXkh3RvEPpzusnp7Ksv9UEn4/Lufcf35W+2f1cnxsrG9GbRsbapODN9Eb8UZrM/jY4GNDqk3ojNYDhNDRulmIPEf3DvHQ77FDJE70PEIkjuAn+AnzSPZWGdfDM37Jkw2JuAm/hJ0Rz8jDyMPwYyFCxi+TV4/94HFi5/0xuF0M9IM3Ro8XwRfBFYVncEShXz1+VM8nKv7gi8p8yfOPCXvwRnDGhB14ouGfyQs8MTNvzzh8xsHHpfN5pPN5pPN4Aq8SPE8Jh36fX+BXwC/R4wv8ijAu+At2rIuwHgK/ouQBToFHAafAp8CnGHmAW6hvobKFYhbwS888PfmwHtLjN9A/4Mc6KeujnY8r66Kshwb3V9ZDwa/UgbIOCk6Ff4V/hX9V5qMOlDrXhB91rvCvrIeCX6ln5ZXWTH+PHXWt4FfqO3UeP1Hnifc78X4n+E/gTcHzSAG76Pkk8Cb4TvCcqP8E3qTYw3OC5wSeBL/J8Adfgs+U6QdH6pmX7SqBy8Bl7FsGbwYeA4fBn8GfUcfGvmTUpcGbgcPgzXhfjffUEuPgMiMO+Ix9yNhzDVwGX0a9GnwZdWrgs4ENnHrMnY9n8GXwZd7TzD6V4SeDK8NThqcsjiODM4MzgzODM1OX+XCQ1P2znDEX42ORocp3VZ5VGau8KgdRO0mV31bZVZmqPK82p1W+rfJ1lVqlVZs8H2V/8bD719JZmv9z+jtXOnocPY4eR4//h8dqsWwu97tP6+tN+QQ5/fjL5tXFdne3vm3KF9/TovmzqfdSirEePwL/o4/AmYLuazsdv7Z0ynm9WnwB",
        }
    ],
}
