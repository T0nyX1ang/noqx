"""Utility for general clingo rules."""

from typing import Tuple, Union

from .encoding import reverse_op, tag_encode


def adjacent(_type: Union[int, str] = 4) -> str:
    """
    Generates a rule for getting the adjacent neighbors.
    If _type = 4, then only orthogonal neighbors are considered.
    If _type = x, then only diagonal neighbors are considered.
    If _type = 8, then both orthogonal and diagonal neighbors are considered.
    If _type = edge, then only the neighbors on unblocked edges are considered.
    If _type = loop, then only the neighbors on the loop are considered.
    If _type = loop_directed, then only the neighbors on the directed loop are considered.

    A grid fact should be defined first.
    """
    if _type == 4:
        return "adj_4(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1."

    if _type == "x":
        return "adj_x(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."

    if _type == 8:
        res = "adj_8(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1.\n"
        res += "adj_8(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."
        return res

    if _type == "edge":
        adj = "adj_edge(R, C, R, C + 1) :- grid(R, C), grid(R, C + 1), not vertical_line(R, C + 1).\n"
        adj += "adj_edge(R, C, R + 1, C) :- grid(R, C), grid(R + 1, C), not horizontal_line(R + 1, C).\n"
        adj += "adj_edge(R, C, R1, C1) :- adj_edge(R1, C1, R, C)."
        return adj

    if _type == "loop":
        adj = 'adj_loop(R0, C0, R, C) :- R = R0, C = C0 + 1, grid(R, C), grid(R0, C0), grid_direction(R, C, "l").\n'
        adj += 'adj_loop(R0, C0, R, C) :- R = R0 + 1, C = C0, grid(R, C), grid(R0, C0), grid_direction(R, C, "u").\n'
        adj += "adj_loop(R0, C0, R, C) :- adj_loop(R, C, R0, C0)."
        return adj

    if _type == "loop_directed":
        adj = 'adj_loop_directed(R0, C0, R, C) :- R = R0, C = C0 + 1, grid(R, C), grid(R0, C0), grid_in(R, C, "l").\n'
        adj += 'adj_loop_directed(R0, C0, R, C) :- R = R0 + 1, C = C0, grid(R, C), grid(R0, C0), grid_in(R, C, "u").\n'
        adj += 'adj_loop_directed(R0, C0, R, C) :- R = R0, C = C0 + 1, grid(R, C), grid(R0, C0), grid_out(R, C, "l").\n'
        adj += 'adj_loop_directed(R0, C0, R, C) :- R = R0 + 1, C = C0, grid(R, C), grid(R0, C0), grid_out(R, C, "u").\n'
        adj += "adj_loop_directed(R0, C0, R, C) :- adj_loop_directed(R, C, R0, C0)."
        return adj

    raise ValueError("Invalid adjacent type.")


def avoid_adjacent(color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generates a constraint to avoid adjacent {color} cells based on adjacent definition.

    An adjacent rule should be defined first.
    """
    return f":- {color}(R, C), {color}(R1, C1), adj_{adj_type}(R, C, R1, C1)."


def area_adjacent(adj_type: Union[int, str] = 4, color: str = None) -> str:
    """
    Generate a rule for getting the adjacent areas.

    An adjacent rule should be defined first.
    """
    area_adj = f"area(A, R, C), area(A1, R1, C1), adj_{adj_type}(R, C, R1, C1), A < A1"
    if color:
        area_adj += f", {color}(R, C), {color}(R1, C1)"
        return f"{tag_encode('area_adj', adj_type, color)}(A, A1) :- {area_adj}."

    return f"area_adj_{adj_type}(A, A1) :- {area_adj}."


def avoid_area_adjacent(color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generates a constraint to avoid same {color} cells on the both sides of an area.

    An adjacent rule and an area fact should be defined first.
    """
    area_adj = area_adjacent(adj_type, color)
    return area_adj[area_adj.find(":-") :]


def count_adjacent(
    target: int, src_cell: Tuple[int, int], op: str = "eq", color: str = "black", adj_type: Union[int, str] = 4
) -> str:
    """
    Generates a constraint for counting the number of {color} cells adjacent to a cell.

    An adjacent rule should be defined first.
    """
    src_r, src_c = src_cell
    op = reverse_op(op)
    return f":- #count {{ R, C: {color}(R, C), adj_{adj_type}(R, C, {src_r}, {src_c}) }} {op} {target}."


def count_adjacent_edges(target: int, src_cell: Tuple[int, int], op: str = "eq") -> str:
    """
    Return a rule that counts the adjacent lines around a cell.

    An edge rule should be defined first.
    """
    src_r, src_c = src_cell
    op = reverse_op(op)
    v_1 = f"vertical_line({src_r}, {src_c})"
    v_2 = f"vertical_line({src_r}, {src_c + 1})"
    h_1 = f"horizontal_line({src_r}, {src_c})"
    h_2 = f"horizontal_line({src_r + 1}, {src_c})"
    return f":- {{ {v_1}; {v_2}; {h_1}; {h_2} }} {op} {target}."
