"""Variety rules and constraints which are not catagorized in other files."""

from typing import Tuple


def nori_adjacent(color: str = "gray", adj_type: int = 4) -> str:
    """
    Generates a constraint for Norinori puzzles.

    A grid rule and an adjacent rule should be defined first.
    """
    return f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }} != 1."


def yaji_count(
    target: int, src_cell: Tuple[int, int], arrow_direction: int, color: str = "black", unshade_clue: bool = True
) -> str:
    """
    Generates a constraint for counting the number of {color} cells in a row / col.

    A grid fact should be defined first.
    """
    src_r, src_c = src_cell
    op = "<" if arrow_direction in [0, 1] else ">"

    shade_clue = "" if unshade_clue else f" not {color}({src_r}, {src_c}),"
    if arrow_direction in [1, 2]:  # left, right
        return f":-{shade_clue} #count {{ C1 : {color}({src_r}, C1), C1 {op} {src_c} }} != {target}."

    if arrow_direction in [0, 3]:  # up, down
        return f":-{shade_clue} #count {{ R1 : {color}(R1, {src_c}), R1 {op} {src_r} }} != {target}."

    raise ValueError("Invalid direction.")
