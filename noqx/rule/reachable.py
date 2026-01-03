"""Generate rules for reachable things and connectivity tests.

Note:
    Every connectivity rule consists of three parts: **initialization**, **propagation** and **constraint** (optional). This structure is similar to the flood-fill algorithm, and it is recommended by the [Clingo](https://potassco.org/clingo/) documentation.
"""

from typing import List, Optional, Tuple, Union

from noqx.rule.helper import tag_encode, target_encode, validate_type


def grid_color_connected(
    color: str = "black", adj_type: Union[int, str] = 4, grid_size: Optional[Tuple[int, int]] = None
) -> str:
    """A rule to ensure all the color cells are connected in the grid.

    * This is the most efficient connectivity checker in this module, since it only considers a global
    constraint. If the problem can be modelled to use this rule, don't hesitate to use it.

    Args:
        color: The color to be checked.
        adj_type: The type of adjacency (accepted types: `4`, `8`, `x`, `loop`, `loop_directed`).
        grid_size: The size of the grid in (`rows`, `columns`). If provided, the propagation
                   starts from the middle of the grid to increase the speed potentially.
    """
    validate_type(adj_type, (4, 8, "x", "loop", "loop_directed"))
    tag = tag_encode("reachable", "grid", "adj", adj_type, color)

    if grid_size is None:
        initial = f"{tag}(R, C) :- (R, C) = #min{{ (R1, C1): grid(R1, C1), {color}(R1, C1) }}."
    else:
        R, C = grid_size
        initial = (
            f"{tag}(R, C) :- (_, R, C) = #min{{ (|R1 - {R // 2}| + |C1 - {C // 2}|, R1, C1): grid(R1, C1), {color}(R1, C1) }}."
        )

    propagation = f"{tag}(R, C) :- {tag}(R1, C1), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    constraint = f":- grid(R, C), {color}(R, C), not {tag}(R, C)."
    return initial + "\n" + propagation + "\n" + constraint


def border_color_connected(rows: int, cols: int, color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """A rule to ensure all the color cells are connected to the borders of the whole grid.

    * Similar to `grid_color_connected`, this is also a global constraint. The difference is that the propagation starts from the borders of the grid. Moreover, the color cells do not need
    to be connected *inside* the grid.

    Args:
        rows: The number of rows in the grid.
        cols: The number of columns in the grid.
        color: The color to be checked.
        adj_type: The type of adjacency (accepted types: `4`, `8`, `x`).
    """
    validate_type(adj_type, (4, 8, "x"))
    tag = tag_encode("reachable", "border", "adj", adj_type, color)
    borders = [(r, c) for r in range(rows) for c in range(cols) if r in [0, rows - 1] or c in [0, cols - 1]]
    initial = "\n".join(f"{tag}({r}, {c}) :- {color}({r}, {c})." for r, c in borders)
    propagation = f"{tag}(R, C) :- {tag}(R1, C1), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    constraint = f":- grid(R, C), {color}(R, C), not {tag}(R, C)."
    return initial + "\n" + propagation + "\n" + constraint


def area_color_connected(color: str = "black", adj_type: int = 4) -> str:
    """A rule to ensure all the color cells are connected in every area.

    * The complexity of this rule is based on the number of areas instead of the whole grid.

    Args:
        color: The color to be checked.
        adj_type: The type of adjacency (accepted types: `4`, `8`, `x`).
    """
    validate_type(adj_type, (4, 8, "x"))
    tag = tag_encode("reachable", "area", "adj", adj_type, color)
    initial = f"{tag}(A, R, C) :- area(A, _, _), (R, C) = #min{{ (R1, C1): area(A, R1, C1), {color}(R1, C1) }}."
    propagation = f"{tag}(A, R, C) :- {tag}(A, R1, C1), area(A, R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    constraint = f":- area(A, R, C), {color}(R, C), not {tag}(A, R, C)."
    return initial + "\n" + propagation + "\n" + constraint


def grid_src_color_connected(
    src_cell: Tuple[int, int],
    include_cells: Optional[List[Tuple[int, int]]] = None,
    exclude_cells: Optional[List[Tuple[int, int]]] = None,
    color: Optional[str] = "black",
    adj_type: Union[int, str] = 4,
) -> str:
    """A rule to collect all the color cells that are reachable to a source cell in a grid.

    * This rule is a local definition, and only does the collection part. To further utilize the rule, a `count_reachable_src` rule may be applied to count the size of the whole connected region.

    * This rule does not ensure that every cell belongs to the connected part of the source cell, an `avoid_unknown_src` rule may be applied to ensure this constraint.

    * The complexity of this cell is mainly based on the size of cells connected to the source cell.

    Args:
        src_cell: The source cell in (`row`, `col`).
        include_cells: The list of cells to be included as reachable cells to the source cell.
        exclude_cells: The list of cells to be excluded from reachable cells to the source cell.
        color: The color to be checked. If it is `None`, only the `edge` adjacency is accepted.
        adj_type: The type of adjacency (accepted types: `4`, `8`, `x`, `edge`, `loop`, `loop_directed`).
    """
    if color is None:
        validate_type(adj_type, ("edge",))
    else:
        validate_type(adj_type, (4, 8, "x", "edge", "loop", "loop_directed"))

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)

    r, c = src_cell
    initial = f"{tag}({r}, {c}, {r}, {c})."

    if include_cells:
        initial += "\n" + "\n".join(f"{tag}({r}, {c}, {inc_r}, {inc_c})." for inc_r, inc_c in include_cells)

    if exclude_cells:
        initial += "\n" + "\n".join(f"not {tag}({r}, {c}, {exc_r}, {exc_c})." for exc_r, exc_c in exclude_cells)

    if adj_type == "edge":
        propagation = f"{tag}({r}, {c}, R, C) :- {tag}({r}, {c}, R1, C1), grid(R, C), adj_edge(R, C, R1, C1)."

        # edge between two reachable grids is forbidden.
        constraint = f":- {tag}({r}, {c}, R, C), {tag}({r}, {c}, R, C + 1), edge_left(R, C + 1).\n"
        constraint += f":- {tag}({r}, {c}, R, C), {tag}({r}, {c}, R + 1, C), edge_top(R + 1, C)."
        return initial + "\n" + propagation + "\n" + constraint

    propagation = f"{tag}({r}, {c}, R, C) :- {tag}({r}, {c}, R1, C1), grid(R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    return initial + "\n" + propagation


def bulb_src_color_connected(src_cell: Tuple[int, int], color: Optional[str] = "black", adj_type: Union[int, str] = 4) -> str:
    """A rule to collect all the color cells that are orthogonally connected to a source cell in a grid.

    * The rule behaves like a **bulb**. It starts from the source cell and spread orthogonally until it hits a cell without a specified color or the border of the grid, which like a **wall** in reality.

    * Since the connection pattern is limited in this rule, it is more efficient than `grid_src_color_connected` with constraints. A typical use-case is to calculate the size of a rectangle: instead of spreading from the source cell to the whole grid, it is possible to get the height and width of the rectangle only, which greatly simplifies the grounding process.

    Args:
        src_cell: The source cell in (`row`, `col`).
        color: The color to be checked. If it is `None`, only the `edge` adjacency is accepted.
        adj_type: The type of adjacency (accepted types: `4`, `edge`).
    """
    if color is None:
        validate_type(adj_type, ("edge",))
    else:
        validate_type(adj_type, (4, "edge"))

    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)

    r, c = src_cell
    initial = f"{tag}({r}, {c}, {r}, {c})."

    bulb_constraint = ""
    if adj_type == 4:
        bulb_constraint = f"{color}(R, C), adj_{adj_type}(R, C, R1, C1), (R - {r}) * (C - {c}) == 0"

    if adj_type == "edge":
        bulb_constraint = f"adj_{adj_type}(R, C, R1, C1), (R - {r}) * (C - {c}) == 0"

    propagation = f"{tag}({r}, {c}, R, C) :- {tag}({r}, {c}, R1, C1), {bulb_constraint}."
    return initial + "\n" + propagation


def count_reachable_src(
    target: Union[int, Tuple[str, int]],
    src_cell: Tuple[int, int],
    main_type: str = "grid",
    color: Optional[str] = "black",
    adj_type: Union[int, str] = 4,
):
    """A rule to compare the number of reachable cells to the source cell with a specified target.

    * This rule is often used together with `grid_src_color_connected` or `bulb_src_color_connected`.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        src_cell: The source cell in (`row`, `col`).
        main_type: The main type of the reachable rule (accepted types: `grid` or `bulb`).
        color: The color to be checked. If it is `None`, only the `edge` adjacency is accepted.
        adj_type: The type of adjacency (accepted types: `4`, `8`, `x`, `edge`, `loop`, `loop_directed`).

    Raises:
        ValueError: If the main type is other than `grid` or `bulb`.
    """
    if color is None:
        validate_type(adj_type, ("edge",))
    elif main_type == "grid":
        validate_type(adj_type, (4, 8, "x", "edge", "loop", "loop_directed"))
    elif main_type == "bulb":
        validate_type(adj_type, (4,))
    else:
        raise ValueError("Invalid main type, must be one of 'grid', 'bulb'.")

    src_r, src_c = src_cell

    tag = tag_encode("reachable", main_type, "src", "adj", adj_type, color)
    rop, num = target_encode(target)

    return f":- {{ {tag}({src_r}, {src_c}, R, C) }} {rop} {num}."


def avoid_unknown_src(color: Optional[str] = "black", main_type: str = "grid", adj_type: Union[int, str] = 4) -> str:
    """A rule to avoid all the cells being unreachable to any source cell.

    * This rule is often used together with `grid_src_color_connected` or `bulb_src_color_connected`.

    Args:
        color: The color to be checked. If it is `None`, only the `edge` adjacency is accepted.
        main_type: The main type of the reachable rule (accepted types: `grid` or `bulb`).
        adj_type: The type of adjacency (accepted types: `4`, `8`, `x`, `edge`, `loop`, `loop_directed`).
    """
    if color is None:
        validate_type(adj_type, ("edge",))
        tag = tag_encode("reachable", main_type, "src", "adj", adj_type)
        return f":- grid(R, C), not {tag}(_, _, R, C)."

    validate_type(adj_type, (4, 8, "loop", "loop_directed"))
    tag = tag_encode("reachable", main_type, "src", "adj", adj_type, color)

    return f":- grid(R, C), {color}(R, C), not {tag}(_, _, R, C)."


def grid_branch_color_connected(color: Optional[str] = "black", adj_type: Union[int, str] = 4) -> str:
    """A rule to collect all the color cells that are connected to any cells in a grid.

    * This rule is similar to `grid_src_color_connected`, but it defines the connected branch for every cell in a grid. Hence, this rule is **very inefficient** compared to other rules. Unless no initial clue cells are given, please consider using `grid_src_color_connected` instead.

    Args:
        color: The color to be checked. If it is `None`, only the `edge` adjacency is accepted.
        adj_type: The type of adjacency (accepted types: `4`, `8`, `x`, `edge`).
    """
    if color is None:
        validate_type(adj_type, ("edge",))
    else:
        validate_type(adj_type, (4, 8, "x", "edge"))

    tag = tag_encode("reachable", "grid", "branch", "adj", adj_type, color)

    if adj_type == "edge":
        initial = f"{tag}(R, C, R, C) :- grid(R, C)."
        propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), grid(R, C), adj_edge(R, C, R1, C1)."

        # edge between two reachable grids is forbidden.
        constraint = f":- {tag}(R, C, R, C + 1), edge_left(R, C + 1).\n"
        constraint += f":- {tag}(R, C, R + 1, C), edge_top(R + 1, C).\n"
        constraint += f":- {tag}(R, C + 1, R, C), edge_left(R, C + 1).\n"
        constraint += f":- {tag}(R + 1, C, R, C), edge_top(R + 1, C)."
        return initial + "\n" + propagation + "\n" + constraint

    initial = f"{tag}(R, C, R, C) :- grid(R, C), {color}(R, C)."
    propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), grid(R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    return initial + "\n" + propagation
