"""Generate neighbor- and area-relevant rules for the solver."""

from typing import Dict, Iterable, Optional, Tuple, Union

from noqx.puzzle import Direction, Point
from noqx.rule.helper import tag_encode, target_encode


def adjacent(_type: Union[int, str] = 4, include_self: bool = False) -> str:
    """A rule to define the adjacent neighbors in a grid.

    * The adjacency is based on a grid, which means two points should both locate on the grid.

    * The following adjacency types are allowed:
        * If _type = `4`, then only orthogonal neighbors are considered.
        * If _type = `x`, then only diagonal neighbors are considered.
        * If _type = `8`, then both orthogonal and diagonal neighbors are considered.
        * If _type = `edge`, then only the neighbors on unblocked edges are considered.
        * If _type = `loop`, then only the neighbors on the loop are considered.
        * If _type = `loop_directed`, then only the neighbors on the directed loop are considered.

    Args:
        _type: The type of adjacency.
        include_self: Whether to include the cell itself as its neighbor.

    Raises:
        ValueError: If the adjacency type is invalid.
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

    raise ValueError(f"Invalid adjacency type: {_type}.")


def avoid_same_color_adjacent(color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """A rule to avoid two adjacent cells having the same color.

    Args:
        color: The color to be checked.
        adj_type: The type of adjacency.
    """
    return f":- {color}(R, C), {color}(R1, C1), adj_{adj_type}(R, C, R1, C1)."


def avoid_same_number_adjacent(adj_type: Union[int, str] = 4) -> str:
    """A rule to avoid two adjacent cells having the same number.

    Args:
        adj_type: The type of adjacency.
    """
    rule = f":- number(R, C, N), number(R1, C1, N), adj_{adj_type}(R, C, R1, C1)."
    return rule


def count_adjacent(
    target: Union[int, Tuple[str, int]], src_cell: Tuple[int, int], color: str = "black", adj_type: Union[int, str] = 4
) -> str:
    """A rule to compare the number of adjacent cells having the same color as the source cell to a specified target.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        src_cell: The source cell as a tuple of (`row`, `col`).
        color: The color to be checked.
        adj_type: The type of adjacency.
    """
    src_r, src_c = src_cell
    rop, num = target_encode(target)
    return f":- #count {{ R, C: {color}(R, C), adj_{adj_type}(R, C, {src_r}, {src_c}) }} {rop} {num}."


def count_adjacent_edges(target: Union[int, Tuple[str, int]], src_cell: Tuple[int, int]) -> str:
    """A rule to compare the number of the edges around a cell to a specified target.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        src_cell: The source cell as a tuple of (`row`, `col`).
    """
    src_r, src_c = src_cell
    rop, num = target_encode(target)
    v_1 = f"edge_left({src_r}, {src_c})"
    v_2 = f"edge_left({src_r}, {src_c + 1})"
    h_1 = f"edge_top({src_r}, {src_c})"
    h_2 = f"edge_top({src_r + 1}, {src_c})"
    return f":- {{ {v_1}; {v_2}; {h_1}; {h_2} }} {rop} {num}."


def area_border(_id: int, src_cells: Iterable[Tuple[int, int]], edge: Dict[Tuple[int, int, str, str], bool]) -> str:
    """A rule to define the border of an area.

    * This border rule is useful on the rules that limit the crossing time of a loop/path in the area.
    Although it is possible to represent the borders with ASP logic, it is better to calculate the borders
    with Python for performance consideration.

    Note:
        Here is an example to define the border of an area with the help of `noqx.helper.full_bfs` function:
        ```python
            from noqx.rule.neighbor import area_border
            from noqx.rule.helper import full_bfs
            rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
            for i, (ar, rc) in enumerate(rooms.items()):
                self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
        ```

    Args:
        _id: The ID of the area.
        src_cells: The cells in the area as a list of tuples of (`row`, `col`).
        edge: The edges of the grid stored in a dictionary, the format is the same to the `edge` attribute
              in the `Puzzle` class.
    """
    edges = set()
    src_cells = set(src_cells)
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


def area_adjacent(adj_type: Union[int, str] = 4, color: Optional[str] = None) -> str:
    """A rule to define the adjacent areas.

    * The `color` parameter can be used to limit the adjacency check to areas with the specified color.
    The area is adjacent if there exists at least one pair of adjacent cells with the same color from
    different areas.

    Args:
        adj_type: The type of adjacency.
        color: The color to be checked.

    Warning:
        To simplify the grounding size, the adjacency of the areas is directional, i.e., area `A` is adjacent
        to area `B` if the ID of area `A` is less than the ID of area `B`, and there share at least one common edge.
    """
    area_adj = f"area(A, R, C), area(A1, R1, C1), adj_{adj_type}(R, C, R1, C1), A < A1"
    if color:
        area_adj += f", {color}(R, C), {color}(R1, C1)"

    return f"{tag_encode('area_adj', adj_type, color)}(A, A1) :- {area_adj}."


def area_same_color(color: str = "black") -> str:
    """Ensure that all cells in the same area have the same color.

    Args:
        color: The color to be checked.
    """
    return f":- area(A, R, C), area(A, R1, C1), {color}(R, C), not {color}(R1, C1)."
