"""Generate neighbor- and area-relevant rules for the solver."""

from typing import Dict, Iterable, List, Optional, Tuple, Union

from noqx.puzzle import Direction, Point
from noqx.rule.helper import tag_encode, target_encode


def adjacent(_type: Union[int, str] = 4) -> str:
    """A rule to define the adjacent neighbors in a grid.

    * The adjacency is based on a "wider" grid with all holes, and both points should be located on the "wider" grid, named by the predicate `grid_all(R, C)`.

    * The following adjacency types are allowed:
        * If _type = `4`, then only orthogonal neighbors are considered.
        * If _type = `x`, then only diagonal neighbors are considered.
        * If _type = `8`, then both orthogonal and diagonal neighbors are considered.
        * If _type = `edge`, then only the neighbors on unblocked edges are considered.
        * If _type = `line`, then only the neighbors on the line are considered.
        * If _type = `line_directed`, then only the neighbors on the directed line are considered.

    Args:
        _type: The type of adjacency.

    Raises:
        ValueError: If the adjacency type is invalid.

    Warning:
        The `line_directed` is not symmetric. If cell A is adjacent to cell B, cell B may not be adjacent to cell A. Be careful in the reachable propagation. If you want to have a symmetric adjacency with directed lines, you may need to add extra rules to make it symmetric.

    Success:
        This rule will generate a predicate named `adj_{_type}(R, C, R1, C1)`.
    """
    rule = ""

    if _type == 4:
        rule += "adj_4(R, C, R1, C1) :- grid_all(R, C), grid_all(R1, C1), |R - R1| + |C - C1| == 1."
        return rule

    if _type == "x":
        rule += "adj_x(R, C, R1, C1) :- grid_all(R, C), grid_all(R1, C1), |R - R1| == 1, |C - C1| == 1."
        return rule

    if _type == 8:
        rule += "adj_8(R, C, R1, C1) :- grid_all(R, C), grid_all(R1, C1), |R - R1| + |C - C1| == 1.\n"
        rule += "adj_8(R, C, R1, C1) :- grid_all(R, C), grid_all(R1, C1), |R - R1| == 1, |C - C1| == 1."
        return rule

    if _type == "edge":
        rule += f'adj_edge(R, C, R, C + 1) :- grid_all(R, C), grid_all(R, C + 1), not edge(R, C + 1, "{Direction.LEFT}").\n'
        rule += f'adj_edge(R, C, R + 1, C) :- grid_all(R, C), grid_all(R + 1, C), not edge(R + 1, C, "{Direction.TOP}").\n'
        rule += "adj_edge(R, C, R1, C1) :- adj_edge(R1, C1, R, C)."
        return rule

    if _type == "line":
        rule += f'adj_line(R, C, R, C + 1) :- grid_all(R, C), grid_all(R, C + 1), line_io(R, C, "{Direction.RIGHT}").\n'
        rule += f'adj_line(R, C, R + 1, C) :- grid_all(R, C), grid_all(R + 1, C), line_io(R, C, "{Direction.BOTTOM}").\n'
        rule += "adj_line(R, C, R1, C1) :- adj_line(R1, C1, R, C)."
        return rule

    if _type == "line_directed":
        rule += (
            f'adj_line_directed(R, C, R, C + 1) :- grid_all(R, C), grid_all(R, C + 1), line_in(R, C, "{Direction.RIGHT}").\n'
        )
        rule += (
            f'adj_line_directed(R, C, R + 1, C) :- grid_all(R, C), grid_all(R + 1, C), line_in(R, C, "{Direction.BOTTOM}").\n'
        )
        rule += (
            f'adj_line_directed(R, C + 1, R, C) :- grid_all(R, C), grid_all(R, C + 1), line_out(R, C, "{Direction.RIGHT}").\n'
        )
        rule += (
            f'adj_line_directed(R + 1, C, R, C) :- grid_all(R, C), grid_all(R + 1, C), line_out(R, C, "{Direction.BOTTOM}").\n'
        )
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
    target: Union[int, Tuple[str, int]],
    src_cell: Tuple[int, int],
    color: str = "black",
    adj_type: Union[int, str] = 4,
    include_self: bool = False,
) -> str:
    """A rule to compare the number of adjacent cells having the same color as the source cell to a specified target.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        src_cell: The source cell as a tuple of (`row`, `col`).
        color: The color to be checked.
        adj_type: The type of adjacency.
        include_self: Whether to include the source cell itself in the count.
    """
    src_r, src_c = src_cell
    rop, num = target_encode(target)
    if include_self:
        return f":- #count {{ R, C: {color}(R, C), adj_{adj_type}(R, C, {src_r}, {src_c}); R, C: {color}(R, C), R = {src_r}, C = {src_c} }} {rop} {num}."

    return f":- #count {{ R, C: {color}(R, C), adj_{adj_type}(R, C, {src_r}, {src_c}) }} {rop} {num}."


def count_adjacent_edges(target: Union[int, Tuple[str, int]], src_cell: Tuple[int, int]) -> str:
    """A rule to compare the number of the edges around a cell to a specified target.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        src_cell: The source cell as a tuple of (`row`, `col`).
    """
    src_r, src_c = src_cell
    rop, num = target_encode(target)
    v_1 = f'edge({src_r}, {src_c}, "{Direction.LEFT}")'
    v_2 = f'edge({src_r}, {src_c + 1}, "{Direction.LEFT}")'
    h_1 = f'edge({src_r}, {src_c}, "{Direction.TOP}")'
    h_2 = f'edge({src_r + 1}, {src_c}, "{Direction.TOP}")'
    return f":- {{ {v_1}; {v_2}; {h_1}; {h_2} }} {rop} {num}."


def count_covering(
    target: Union[int, Tuple[str, int]], src_cell: Tuple[int, int], direction: str, color: str = "black"
) -> str:
    """A rule to compare the number of cells with the specified color covering the source cell in the given direction to a specified target.

    * If the source cell is on the edge, two cells are required to cover it; if the source cell is on the corner, four cells are required to cover it. Otherwise, only the source cell itself is required to cover it.

    * Due to technical reasons with edges, the color cannot start with `not`, please use the `noqx.rule.common.invert_c` rule for assistance.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        src_cell: The source cell as a tuple of (`row`, `col`).
        direction: The direction to check the covering (acceptable values are Direction.LEFT, Direction.TOP and Direction.TOP_LEFT).
        color: The color to be checked.
    """
    src_r, src_c = src_cell
    rop, num = target_encode(target)

    covers: List[Tuple[int, int]] = [(src_r, src_c)]
    if direction == Direction.LEFT:
        covers.append((src_r, src_c - 1))

    if direction == Direction.TOP:
        covers.append((src_r - 1, src_c))

    if direction == Direction.TOP_LEFT:
        covers.append((src_r - 1, src_c))
        covers.append((src_r, src_c - 1))
        covers.append((src_r - 1, src_c - 1))

    return f":- {{ {'; '.join(f'{color}({r}, {c})' for r, c in covers)} }} {rop} {num}."


def area_border(_id: int, src_cells: Iterable[Tuple[int, int]], edge: Dict[Tuple[int, int, str, str], bool]) -> str:
    """A rule to define the border of an area.

    * This border rule is useful on the rules that limit the crossing time of a line/path in the area. Although it is possible to represent the borders with ASP logic, it is better to calculate the borders with Python for performance consideration.

    Args:
        _id: The ID of the area.
        src_cells: The cells in the area as a list of tuples of (`row`, `col`).
        edge: The edges of the grid stored in a dictionary, the format is the same to the `edge` attribute
              in the `Puzzle` class.

    Success:
        This rule will generate a predicate named `area_border(A, R, C, D)`.

    Note:
        Here is an example to define the border of an area with the help of `noqx.helper.full_bfs` function:
        ```python
            from noqx.rule.neighbor import area_border
            from noqx.rule.helper import full_bfs
            rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
            for i, (ar, rc) in enumerate(rooms.items()):
                self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
        ```
    """
    edges = set()
    src_cells = set(src_cells)
    for r, c in src_cells:
        if edge.get(Point(r, c, Direction.TOP)) is True:
            edges.add(f'area_border({_id}, {r}, {c}, "{Direction.TOP}").')
            if (r - 1, c) in src_cells:
                edges.add(f'area_border({_id}, {r - 1}, {c}, "{Direction.BOTTOM}").')

        if edge.get(Point(r + 1, c, Direction.TOP)) is True:
            edges.add(f'area_border({_id}, {r}, {c}, "{Direction.BOTTOM}").')
            if (r + 1, c) in src_cells:
                edges.add(f'area_border({_id}, {r + 1}, {c}, "{Direction.TOP}").')

        if edge.get(Point(r, c, Direction.LEFT)) is True:
            edges.add(f'area_border({_id}, {r}, {c}, "{Direction.LEFT}").')
            if (r, c - 1) in src_cells:
                edges.add(f'area_border({_id}, {r}, {c - 1}, "{Direction.RIGHT}").')

        if edge.get(Point(r, c + 1, Direction.LEFT)) is True:
            edges.add(f'area_border({_id}, {r}, {c}, "{Direction.RIGHT}").')
            if (r, c + 1) in src_cells:
                edges.add(f'area_border({_id}, {r}, {c + 1}, "{Direction.LEFT}").')

    rule = "\n".join(edges)
    return rule


def area_adjacent(adj_type: Union[int, str] = 4, color: Optional[str] = None) -> str:
    """A rule to define the adjacent areas.

    * The `color` parameter can be used to limit the adjacency check to areas with the specified color. The area is adjacent if there exists at least one pair of adjacent cells with the same color from different areas.

    Args:
        adj_type: The type of adjacency.
        color: The color to be checked.

    Success:
        This rule will generate a predicate named `area_adj_{adj_type}(A, A1)` or `area_adj_{adj_type}_{color}(A, A1)`.

    Warning:
        To simplify the grounding size, the adjacency of the areas is directional, i.e., area `A` is adjacent to area `B` if the ID of area `A` is less than the ID of area `B`, and there share at least one common edge.
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
