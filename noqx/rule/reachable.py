"""Utility for reachable things and connectivity tests."""

from math import log2
from typing import List, Optional, Tuple, Union

from noqx.rule.helper import tag_encode, target_encode, validate_type


def grid_color_connected(
    color: str = "black", adj_type: Union[int, str] = 4, grid_size: Optional[Tuple[int, int]] = None
) -> str:
    """
    Generate a constraint to check the reachability of {color} cells.

    An adjacent rule and a grid fact should be defined first.
    """
    validate_type(adj_type, (4, 8, "x", "loop", "loop_directed"))
    tag = tag_encode("reachable", "grid", "adj", adj_type, color)

    if grid_size is None:
        initial = f"{tag}(R, C) :- (R, C) = #min{{ (R1, C1): grid(R1, C1), {color}(R1, C1) }}."
    else:
        # propagation from the middle of the grid to increase the speed
        R, C = grid_size
        initial = (
            f"{tag}(R, C) :- (_, R, C) = #min{{ (|R1 - {R // 2}| + |C1 - {C // 2}|, R1, C1): grid(R1, C1), {color}(R1, C1) }}."
        )

    propagation = f"{tag}(R, C) :- {tag}(R1, C1), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    constraint = f":- grid(R, C), {color}(R, C), not {tag}(R, C)."
    return initial + "\n" + propagation + "\n" + constraint


def border_color_connected(rows: int, cols: int, color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells connected to borders.

    An adjacent rule and a grid fact should be defined first.
    """
    validate_type(adj_type, (4, 8, "x"))
    tag = tag_encode("reachable", "border", "adj", adj_type, color)
    borders = [(r, c) for r in range(rows) for c in range(cols) if r in [0, rows - 1] or c in [0, cols - 1]]
    initial = "\n".join(f"{tag}({r}, {c}) :- {color}({r}, {c})." for r, c in borders)
    propagation = f"{tag}(R, C) :- {tag}(R1, C1), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    constraint = f":- grid(R, C), {color}(R, C), not {tag}(R, C)."
    return initial + "\n" + propagation + "\n" + constraint


def area_color_connected(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells.

    An adjacent rule and an area fact should be defined first.
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
    """
    Generate a constraint to check the reachability of {color} cells starting from a source.

    An adjacent rule and a grid fact should be defined first.
    If adj_type is "edge", an edge fact should be defined first.
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
    """
    Generate a constraint to check the reachability of {color} cells starting from a bulb.

    An adjacent rule and a grid fact should be defined first.
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
    """
    Generate a constraint to count the reachable cells starting from a source.

    A grid_src_color_connected or bulb_src_color_connected should be defined first.
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


def count_rect_src(
    target: Union[int, Tuple[str, int]],
    src_cell: Tuple[int, int],
    color: Optional[str] = None,
    adj_type: Union[int, str] = 4,
) -> str:
    """
    Generate a constraint to count the reachable rectangular area starting from a source.

    A bulb_src_color_connected rule should be defined first.
    """
    if color is None:
        validate_type(adj_type, ("edge",))

    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)
    rop, num = target_encode(target)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {count_r}, {count_c}, CR * CC {rop} {num}."


def avoid_unknown_src(color: Optional[str] = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generate a constraint to avoid cells starting from unknown source.

    Use this constraint with grid_src_color_connected, and adj_type cannot be "edge".
    """
    if color is None:
        validate_type(adj_type, ("edge",))
        tag = tag_encode("reachable", "grid", "src", "adj", adj_type)
        return f":- grid(R, C), not {tag}(_, _, R, C)."

    validate_type(adj_type, (4, 8, "loop", "loop_directed"))
    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)

    return f":- grid(R, C), {color}(R, C), not {tag}(_, _, R, C)."


def clue_bit(r: int, c: int, _id: int, nbit: int) -> str:
    """Assign clues with bit ids instead of numerical ids."""
    rule = f"clue({r}, {c}).\n"
    for i in range(nbit):
        if _id >> i & 1:
            rule += f"clue_bit({r}, {c}, {i}).\n"
    return rule.strip()


def num_binary_range(num: int) -> Tuple[str, int]:
    """Generate a rule restricting number represented by bits between 0 and num."""
    nbit = int(log2(num)) + 1
    rule = f"bit_range(0..{nbit - 1}).\n"
    return rule.strip(), nbit


def grid_bit_color_connected(color: str = "black", adj_type: Union[int, str] = "loop") -> str:
    """Generate a constraint to check the reachability of {color} cells starting from a source (bit version)."""
    validate_type(adj_type, (4, 8, "x", "loop", "loop_directed"))

    tag = tag_encode("reachable", "grid", "bit", "adj", adj_type)
    rule = f"{{ {tag}(R, C, B) }} :- grid(R, C), {color}(R, C), bit_range(B).\n"
    rule += f"{tag}(R, C, B) :- clue_bit(R, C, B).\n"
    rule += f"not {tag}(R, C, B) :- grid(R, C), {color}(R, C), bit_range(B), clue(R, C), not clue_bit(R, C, B).\n"
    rule += f"{tag}(R, C, B) :- {tag}(R1, C1, B), grid(R, C), bit_range(B), {color}(R, C), adj_{adj_type}(R, C, R1, C1).\n"
    rule += f"not {tag}(R, C, B) :- not {tag}(R1, C1, B), grid(R, C), grid(R1, C1), bit_range(B), {color}(R, C), {color}(R1, C1), adj_{adj_type}(R, C, R1, C1).\n"
    return rule.strip()


def avoid_unknown_src_bit(color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generate a constraint to avoid cells starting from unknown source (bit version).

    Use this constraint with grid_bit_color_connected, and adj_type cannot be "edge".
    """
    tag = tag_encode("reachable", "grid", "bit", "adj", adj_type)
    return f":- grid(R, C), {color}(R, C), not {tag}(R, C, _)."


def grid_branch_color_connected(color: Optional[str] = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells with branches.

    An adjacent rule and a grid fact should be defined first.
    If adj_type is "edge", an edge fact should be defined first.
    Unless no initial cells are given, please consider using grid_src_color_connected.
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
