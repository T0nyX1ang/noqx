"""The Look Air solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import all_rect
from noqx.solution import solver


def square_size(color: str = "black") -> str:
    rule = (
        f"square_size(R, C, N) :- upleft(R, C), MC = #min{{ C0: grid(R, C0 - 1), not {color}(R, C0), C0 > C }}, N = MC - C.\n"
    )
    rule += f"square_size(R, C, N) :- grid(R, C), {color}(R, C), square_size(R, C - 1, N).\n"
    rule += f"square_size(R, C, N) :- grid(R, C), {color}(R, C), square_size(R - 1, C, N).\n"
    return rule.strip()


def avoid_same_size_square_see(color: str = "black") -> str:
    left_c = f"#max{{ C0: grid(R, C0), {color}(R, C0), not {color}(R, C0 + 1), C0 < C }}"
    rule = f":- upleft(R, C), MC = {left_c}, square_size(R, C, N), square_size(R, MC, N).\n"
    rule += f":- left(R, C), MC = {left_c}, square_size(R, C, N), square_size(R, MC, N).\n"

    up_c = f"#max{{ R0: {color}(R0, C), not {color}(R0 + 1, C), R0 < R }}"
    rule += f":- upleft(R, C), MR = {up_c}, square_size(R, C, N), square_size(MR, C, N).\n"
    rule += f":- up(R, C), MR = {up_c}, square_size(R, C, N), square_size(MR, C, N).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(all_rect(color="gray", square=True))
    solver.add_program_line(square_size(color="gray"))
    solver.add_program_line(avoid_same_size_square_see(color="gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(
            f":- #count{{ (R, C): gray(R, C), adj_4({r}, {c}, R, C) }} = N0, #count{{ 1: gray({r}, {c}) }} = N1, N0 + N1 != {num}."
        )

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Look Air",
    "aliases": ["Rukkuea"],
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VRRb5swEH7nV0z3fA/YBtL6LeuavWTpOjJFkYUQZVRFpaKFME1G/PeeDzKqrdO0Sev2MJ3u05fPZ+fzOZf2ocuaAiMKdYI+CgoZRZwiCDj9KbbloSr0K1x2h5u6IYJ4sVrhdVa1hWemqsTr7am2l2jfagMSkFNAgvZS9/adthu0MS0BCtLWxASgJHo+0x2vO3Y2isInvpk40T3RvGzyqkjXo/JeG7tFcN/zmnc7Cnf15wLGbfw5r++uSidcZQe6THtT3k8rbfepvu2mWpEMaJej3fgZu2q26+ho17Fn7Lpb/GG7p8kwUNs/kOFUG+f940xPZhrrnnCje5DSbVXkZXwbUN8J4TdCsDg2ZxJC5QR63aMQseA/EfiMJxULrvh6BpkRbGnPuGKUjFtyjFYxvmH0GUPGNdecM+4YzxgDxohrFu7Ov9SVF7BjpOQRGyP8fZ54BuKuuc7yAmjkBg++AKdRtBz8n8K/NIXuCfx/7Vf3EzuGuisV2guE+y7N0ryugP7I8Qf6i7unsYGqrm+zsoHEewQ="
        },
        {"url": "https://puzz.link/p?lookair/9/9/g2a2b4d2i2y1i3d4b1a1g", "test": False},
        {"url": "https://pzplus.tck.mn/p?lookair/20/10/1b2f12b1c3d2l2zzg2a1b4a3zzg2l4d2c1b32f3b2", "test": False},
    ],
}
