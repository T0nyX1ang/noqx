"""Utility for neighbor-relevant (primary to connected) rules."""

from typing import Dict, Iterable, Optional, Tuple, Union

from noqx.puzzle import Direction, Point
from noqx.rule.helper import tag_encode, target_encode


def adjacent(_type: Union[int, str] = 4, include_self: bool = False) -> str:
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
    rule = f"adj_{_type}(R, C, R, C) :- grid(R, C).\n" if include_self else ""

    if _type == 4:
        rule += "adj_4(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1."
        return rule

    if _type == "x":
        rule += "adj_x(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."
        return rule

    if _type == 8:
        rule += "adj_8(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1.\n"
        rule += "adj_8(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."
        return rule

    if _type == "edge":
        rule += "adj_edge(R, C, R, C + 1) :- grid(R, C), grid(R, C + 1), not edge_left(R, C + 1).\n"
        rule += "adj_edge(R, C, R + 1, C) :- grid(R, C), grid(R + 1, C), not edge_top(R + 1, C).\n"
        rule += "adj_edge(R, C, R1, C1) :- adj_edge(R1, C1, R, C)."
        return rule

    if _type == "loop":
        rule += 'adj_loop(R0, C0, R, C) :- R = R0, C = C0 + 1, grid(R, C), grid(R0, C0), grid_direction(R, C, "l").\n'
        rule += 'adj_loop(R0, C0, R, C) :- R = R0 + 1, C = C0, grid(R, C), grid(R0, C0), grid_direction(R, C, "u").\n'
        rule += "adj_loop(R0, C0, R, C) :- adj_loop(R, C, R0, C0)."
        return rule

    if _type == "loop_directed":
        rule += 'adj_loop_directed(R0, C0, R, C) :- R = R0, C = C0 + 1, grid(R, C), grid(R0, C0), grid_in(R, C, "l").\n'
        rule += 'adj_loop_directed(R0, C0, R, C) :- R = R0 + 1, C = C0, grid(R, C), grid(R0, C0), grid_in(R, C, "u").\n'
        rule += 'adj_loop_directed(R0, C0, R, C) :- R = R0, C = C0 + 1, grid(R, C), grid(R0, C0), grid_out(R, C, "l").\n'
        rule += 'adj_loop_directed(R0, C0, R, C) :- R = R0 + 1, C = C0, grid(R, C), grid(R0, C0), grid_out(R, C, "u").\n'
        rule += "adj_loop_directed(R0, C0, R, C) :- adj_loop_directed(R, C, R0, C0)."
        return rule

    raise ValueError(f"Invalid adjacent type: {_type}.")


def avoid_adjacent_color(color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generates a constraint to avoid adjacent {color} cells based on adjacent definition.

    An adjacent rule should be defined first.
    """
    return f":- {color}(R, C), {color}(R1, C1), adj_{adj_type}(R, C, R1, C1)."


def area_adjacent(adj_type: Union[int, str] = 4, color: Optional[str] = None) -> str:
    """
    Generate a rule for getting the adjacent areas.

    An adjacent rule should be defined first.
    """
    area_adj = f"area(A, R, C), area(A1, R1, C1), adj_{adj_type}(R, C, R1, C1), A < A1"
    if color:
        area_adj += f", {color}(R, C), {color}(R1, C1)"

    return f"{tag_encode('area_adj', adj_type, color)}(A, A1) :- {area_adj}."


def count_adjacent(
    target: Union[int, Tuple[str, int]], src_cell: Tuple[int, int], color: str = "black", adj_type: Union[int, str] = 4
) -> str:
    """
    Generates a constraint for counting the number of {color} cells adjacent to a cell.

    An adjacent rule should be defined first.
    """
    src_r, src_c = src_cell
    rop, num = target_encode(target)
    return f":- #count {{ R, C: {color}(R, C), adj_{adj_type}(R, C, {src_r}, {src_c}) }} {rop} {num}."


def count_adjacent_edges(target: Union[int, Tuple[str, int]], src_cell: Tuple[int, int]) -> str:
    """
    Return a rule that counts the adjacent lines around a cell.

    An edge rule should be defined first.
    """
    src_r, src_c = src_cell
    rop, num = target_encode(target)
    v_1 = f"edge_left({src_r}, {src_c})"
    v_2 = f"edge_left({src_r}, {src_c + 1})"
    h_1 = f"edge_top({src_r}, {src_c})"
    h_2 = f"edge_top({src_r + 1}, {src_c})"
    return f":- {{ {v_1}; {v_2}; {h_1}; {h_2} }} {rop} {num}."


def avoid_num_adjacent(adj_type: Union[int, str] = 4) -> str:
    """
    Generate a constraint to avoid adjacent cells with the same number.

    An adjacent rule should be defined first.
    """
    rule = f":- number(R, C, N), number(R1, C1, N), adj_{adj_type}(R, C, R1, C1)."
    return rule


def area_same_color(color: str = "black") -> str:
    """Ensure that all cells in the same area have the same color."""
    return f":- area(A, R, C), area(A, R1, C1), {color}(R, C), not {color}(R1, C1)."


def area_border(_id: int, src_cells: Iterable[Tuple[int, int]], edge: Dict[Point, bool]) -> str:
    """Generates a fact for the border of an area."""
    edges = set()
    for r, c in src_cells:
        if edge.get(Point(r, c, Direction.TOP)) is True:
            edges.add(f'area_border({_id}, {r}, {c}, "u").')
            if (r - 1, c) in src_cells:
                edges.add(f'area_border({_id}, {r - 1}, {c}, "d").')

        if edge.get(Point(r + 1, c, Direction.TOP)) is True:
            edges.add(f'area_border({_id}, {r}, {c}, "d").')
            if (r + 1, c) in src_cells:
                edges.add(f'area_border({_id}, {r + 1}, {c}, "u").')

        if edge.get(Point(r, c, Direction.LEFT)) is True:
            edges.add(f'area_border({_id}, {r}, {c}, "l").')
            if (r, c - 1) in src_cells:
                edges.add(f'area_border({_id}, {r}, {c - 1}, "r").')

        if edge.get(Point(r, c + 1, Direction.LEFT)) is True:
            edges.add(f'area_border({_id}, {r}, {c}, "r").')
            if (r, c + 1) in src_cells:
                edges.add(f'area_border({_id}, {r}, {c + 1}, "l").')

    rule = "\n".join(edges)
    return rule
