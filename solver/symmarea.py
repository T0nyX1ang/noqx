"""Solve Symmetry Area puzzles."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import count_reachable_src, grid_src_color_connected
from noqx.solution import solver


def fillomino_constraint() -> str:
    """Generate the Fillomino constraints."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")

    # propagation of number
    rule = f"number(R, C, N) :- number(R0, C0, N), {tag}(R0, C0, R, C).\n"
    # this is a huge optimization
    rule += ":- grid(R, C), number(R, C, N1), number(R, C, N2), N1 < N2.\n"

    # same number, adjacent cell, no line
    rule += ":- number(R, C, N), number(R, C + 1, N), edge_left(R, C + 1).\n"
    rule += ":- number(R, C, N), number(R + 1, C, N), edge_top(R + 1, C).\n"

    # different number, adjacent cell, have line
    rule += ":- number(R, C, N1), number(R, C + 1, N2), N1 != N2, not edge_left(R, C + 1).\n"
    rule += ":- number(R, C, N1), number(R + 1, C, N2), N1 != N2, not edge_top(R + 1, C).\n"

    # special case for 1
    mutual = ["edge_top(R, C)", "edge_top(R + 1, C)", "edge_left(R, C)", "edge_left(R, C + 1)"]
    rule += f"{{ {'; '.join(mutual)} }} = 4 :- number(R, C, 1).\n"
    rule += f"number(R, C, 1) :- {', '.join(mutual)}.\n"
    rule += ":- number(R, C, 1), number(R1, C1, 1), adj_4(R, C, R1, C1).\n"

    return rule.strip()


def fillomino_filtered(fast: bool = True) -> str:
    """Generate the Fillomino filtered connection constraints."""
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")
    rule = ""
    tag1 = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    rule += f"have_numberx(R, C) :- grid(R, C), not {tag1}(_, _, R, C).\n"

    rule += f"{tag}(R, C, R, C) :- grid(R, C), have_numberx(R, C).\n"
    rule += f"{tag}(R, C, R0, C0) :- grid(R0, C0), grid(R, C), {tag}(R, C, R1, C1), have_numberx(R0, C0), have_numberx(R, C), adj_edge(R0, C0, R1, C1).\n"

    if fast:
        rule += "{ numberx(R, C, 1..5) } = 1 :- grid(R, C), have_numberx(R, C).\n"
        rule += f":- numberx(R, C, N), #count{{ R1, C1: {tag}(R, C, R1, C1) }} != N.\n"
    else:
        rule += f"{{ numberx(R, C, N) }} = 1 :- grid(R, C), have_numberx(R, C), #count{{ R1, C1: {tag}(R, C, R1, C1) }} = N.\n"
    rule += ":- number(R, C, N), numberx(R1, C1, N), adj_4(R, C, R1, C1)."

    rule += ":- numberx(R, C, N), numberx(R, C + 1, N), edge_left(R, C + 1).\n"
    rule += ":- numberx(R, C, N), numberx(R + 1, C, N), edge_top(R + 1, C).\n"
    rule += (
        ":- have_numberx(R, C), have_numberx(R, C + 1), numberx(R, C, N), not numberx(R, C + 1, N), not edge_left(R, C + 1).\n"
    )
    rule += (
        ":- have_numberx(R, C), have_numberx(R + 1, C), numberx(R, C, N), not numberx(R + 1, C, N), not edge_top(R + 1, C).\n"
    )

    return rule.strip()


def symmetry_area() -> str:
    """Force central symmetry of areas."""

    tag_number = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    tag_numberx = tag_encode("reachable", "grid", "branch", "adj", "edge")

    # number
    rule = f"min_r(R, C, MR) :- clue(R, C), MR = #min{{ R1: grid(R1, C1), {tag_number}(R, C, R1, C1) }}.\n"
    rule += f"max_r(R, C, MR) :- clue(R, C), MR = #max{{ R1: grid(R1, C1), {tag_number}(R, C, R1, C1) }}.\n"
    rule += f"min_c(R, C, MC) :- clue(R, C), MC = #min{{ C1: grid(R1, C1), {tag_number}(R, C, R1, C1) }}.\n"
    rule += f"max_c(R, C, MC) :- clue(R, C), MC = #max{{ C1: grid(R1, C1), {tag_number}(R, C, R1, C1) }}.\n"
    rule += "symm_coord_sum(R, C, SR, SC) :- clue(R, C), min_r(R, C, MINR), max_r(R, C, MAXR), min_c(R, C, MINC), max_c(R, C, MAXC), SR = MINR + MAXR, SC = MINC + MAXC.\n"

    rule += f":- clue(R0, C0), clue(R1, C1), {tag_number}(R0, C0, R1, C1), symm_coord_sum(R0, C0, SR, SC), not symm_coord_sum(R1, C1, SR, SC).\n"
    rule += (
        f":- clue(R, C), symm_coord_sum(R, C, SR, SC), {tag_number}(R, C, R0, C0), not {tag_number}(R, C, SR - R0, SC - C0).\n"
    )

    # numberx
    # rule += f"have_numberx_root(R, C) :- have_numberx(R, C), edge_left(R, C), edge_top(R, C)."
    rule += (
        f"min_rx(R, C, MR) :- have_numberx(R, C), MR = #min{{ R1: grid(R1, C1), {tag_numberx}(R, C, R1, C1) }}, grid(MR, _).\n"
    )
    rule += (
        f"max_rx(R, C, MR) :- have_numberx(R, C), MR = #max{{ R1: grid(R1, C1), {tag_numberx}(R, C, R1, C1) }}, grid(MR, _).\n"
    )
    rule += (
        f"min_cx(R, C, MC) :- have_numberx(R, C), MC = #min{{ C1: grid(R1, C1), {tag_numberx}(R, C, R1, C1) }}, grid(_, MC).\n"
    )
    rule += (
        f"max_cx(R, C, MC) :- have_numberx(R, C), MC = #max{{ C1: grid(R1, C1), {tag_numberx}(R, C, R1, C1) }}, grid(_, MC).\n"
    )

    rule += "{ symm_coord_sumx(R, C, SR, SC) : grid2(SR, SC) } = 1 :- grid(R, C), have_numberx(R, C).\n"
    rule += "symm_coord_sumx(R, C, SR, SC) :- grid(R, C), have_numberx(R, C), min_rx(R, C, MINR), max_rx(R, C, MAXR), min_cx(R, C, MINC), max_cx(R, C, MAXC), SR = MINR + MAXR, SC = MINC + MAXC.\n"
    # rule += f"symm_coord_sumx(R1, C1, SR, SC) :- have_numberx(R, C), have_numberx(R1, C1), {tag_numberx}(R, C, R1, C1), symm_coord_sumx(R, C, SR, SC).\n"
    rule += f":- have_numberx(R, C), symm_coord_sumx(R, C, SR, SC), not {tag_numberx}(R, C, SR - R, SC - C).\n"

    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(f"grid2(0..{(puzzle.row - 1) * 2}, 0..{(puzzle.col - 1) * 2}).")
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(fillomino_constraint())
    solver.add_program_line(fillomino_filtered(fast=puzzle.param["fast_mode"]))
    solver.add_program_line(symmetry_area())

    numberx_uplimit = puzzle.row * puzzle.col - sum(set(num for (r, c), num in puzzle.text.items()))
    solver.add_program_line(f":- #count{{ R, C: grid(R, C), have_numberx(R, C) }} > {numberx_uplimit}.")

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be an integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")
        solver.add_program_line(f"clue({r}, {c}).")
        solver.add_program_line(grid_src_color_connected(src_cell=(r, c), color=None, adj_type="edge"))
        solver.add_program_line(count_reachable_src(target=int(num), src_cell=(r, c), color=None, adj_type="edge"))

        if num == 1:
            solver.add_program_line(f":- not edge_left({r}, {c}).")
            solver.add_program_line(f":- not edge_top({r}, {c}).")
            solver.add_program_line(f":- not edge_left({r}, {c + 1}).")
            solver.add_program_line(f":- not edge_top({r + 1}, {c}).")

    for r, c, d in puzzle.edge:
        solver.add_program_line(f"edge_{d.value}({r}, {c}).")

    for r, c, d in puzzle.helper_x:
        solver.add_program_line(f":- edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.add_program_line(display(item="number", size=3))
    solver.add_program_line(display(item="numberx", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Symmetry Area",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VRda9swFH33ryh6vg+W5I9Ub12X7CVz1zWjFGGM47qrmT11TjyGQv57r65tHELL2GDZHobQ4fjoKD661s3mW5e3JUQ45Ax84DhEFNHkQUDTH8aq2talOoOLbvtoWiQAV4sFPOT1pvT04Eq9nT1X9hrsO6WZYECTsxTstdrZ98omYG9wiQFHbYmMMxBI5xO9pXXHLnuR+8iTgSO9Q1pUbVGX2bJXPihtV8Dce97QbkdZY76XrN9Gz4Vp1pUT1vkWD7N5rJ6GlU13b750g5ene7AXr8eVU1xH+7iOvRDXneIPxz1P93ss+0cMnCntsn+a6GyiN2qHmKgdE3I8af9tmIiPBEmO6EAgx2wSAuEE/LqjEJIjnISIHPJAiI4cMTkOXhuTIxgFjMsp9B3hglAQrvBMYCXhW0KfMCRckmdOeEt4SRgQRuSJXVV+qW4niKOFoCbsR/j7PPU0m99/Ls8S0zZ5jfcm6Zp12Y7P2Kh7j/1gNLXELcH/3v1Lves+gf+v3cSfxNFYXSGhr9PQvU9dlmeFwcuGRXQG6Qz4J/KqAX/BXr288Vg/+fmxGdlDVdemqb4alnrP",
        },
        {
            "url": "https://pzplus.tck.mn/p?symmarea/10/10/3141592653zp9x2zp5827312384",
        },
        {
            "url": "https://pzplus.tck.mn/p?symmarea/10/10/5o2g3mag5g8lah7g7j5g7h2g1hag5h6g6j2g6halbg1g2m5g1o3",
        },
        {
            "url": "https://pzplus.tck.mn/p?symmarea/10/10/h1i5j4g4g1g1h1g2g1i1h4g4g1g1j4k1h4i9g1h1i4t1j1l1i1j",
        },
    ],
    "parameters": {"fast_mode": {"name": "Fast Mode", "type": "checkbox", "default": False}},
}
