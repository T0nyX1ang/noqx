"""Utility for reachable things and connectivity tests."""

from typing import List, Optional, Tuple, Union

from .helper import tag_encode


def validate_type(_type: Union[int, str], target_type: Tuple[Union[int, str]]) -> None:
    """Validate any matching type."""
    if _type not in target_type:
        raise ValueError(f"Invalid type '{_type}'.")


def grid_color_connected(
    color: str = "black", adj_type: Union[int, str] = 4, initial_cells: Optional[List[Tuple[int, int]]] = None
) -> str:
    """
    Generate a constraint to check the reachability of {color} cells.

    An adjacent rule and a grid fact should be defined first.
    """
    validate_type(adj_type, (4, 8, "loop", "loop_directed"))
    tag = tag_encode("reachable", "grid", "adj", adj_type, color)

    if not initial_cells:
        initial = f"{tag}(R, C) :- (R, C) = #min{{ (R1, C1): grid(R1, C1), {color}(R1, C1) }}."
    else:
        initial = "\n".join(f"{tag}({r}, {c})." for r, c in initial_cells)

    propagation = f"{tag}(R, C) :- {tag}(R1, C1), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    constraint = f":- grid(R, C), {color}(R, C), not {tag}(R, C)."
    return initial + "\n" + propagation + "\n" + constraint


def border_color_connected(rows: int, cols: int, color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells connected to borders.

    An adjacent rule and a grid fact should be defined first.
    """
    validate_type(adj_type, (4,))
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
    validate_type(adj_type, (4, 8))
    tag = tag_encode("reachable", "area", "adj", adj_type, color)
    initial = f"{tag}(A, R, C) :- area(A, _, _), (R, C) = #min{{ (R1, C1): area(A, R1, C1), {color}(R1, C1) }}."
    propagation = f"{tag}(A, R, C) :- {tag}(A, R1, C1), area(A, R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    constraint = f":- area(A, R, C), {color}(R, C), not {tag}(A, R, C)."
    return initial + "\n" + propagation + "\n" + constraint


def grid_src_color_connected(
    src_cell: Tuple[int, int],
    include_cells: Optional[List[Tuple[int, int]]] = None,
    exclude_cells: Optional[List[Tuple[int, int]]] = None,
    color: str = "black",
    adj_type: Union[int, str] = 4,
) -> str:
    """
    Generate a constraint to check the reachability of {color} cells starting from a source.

    An adjacent rule and a grid fact should be defined first.
    If adj_type is "edge", an edge fact should be defined first.
    """
    validate_type(adj_type, (4, 8, "edge", "loop", "loop_directed"))
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
        constraint = f":- {tag}({r}, {c}, R, C), {tag}({r}, {c}, R, C + 1), vertical_line(R, C + 1).\n"
        constraint += f":- {tag}({r}, {c}, R, C), {tag}({r}, {c}, R + 1, C), horizontal_line(R + 1, C).\n"

        return initial + "\n" + propagation + "\n" + constraint

    propagation = f"{tag}({r}, {c}, R, C) :- {tag}({r}, {c}, R1, C1), grid(R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    return initial + "\n" + propagation


def bulb_src_color_connected(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells starting from a bulb.

    An adjacent rule and a grid fact should be defined first.
    """
    validate_type(adj_type, (4, 8))
    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)

    r, c = src_cell
    initial = f"{tag}({r}, {c}, {r}, {c})."

    if adj_type == 4:
        bulb_constraint = f"adj_4(R, C, R1, C1), (R - {r}) * (C - {c}) == 0"
    elif adj_type == 8:
        bulb_constraint = f"adj_8(R, C, R1, C1), (R - {r}) * (C - {c}) * (R - {r} - C + {c}) * (R - {r} + C - {c}) == 0"
    else:
        raise ValueError("Invalid adjacent type, must be one of '4', '8'.")

    propagation = f"{tag}({r}, {c}, R, C) :- {tag}({r}, {c}, R1, C1), {color}(R, C), {bulb_constraint}."
    return initial + "\n" + propagation


def grid_branch_color_connected(color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells with branches.

    An adjacent rule and a grid fact should be defined first.
    Unless no initial cells are given, please consider using grid_src_color_connected.
    """
    validate_type(adj_type, (4, 8))
    tag = tag_encode("reachable", "grid", "branch", "adj", adj_type, color)

    initial = f"{tag}(R, C, R, C) :- grid(R, C), {color}(R, C)."
    propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    return initial + "\n" + propagation


def avoid_unknown_src(color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generate a constraint to avoid cells starting from unknown source.

    Use this constraint with grid_src_color_connected, and adj_type cannot be "edge".
    """
    validate_type(adj_type, (4, 8, "loop", "loop_directed"))
    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)

    return f":- grid(R, C), {color}(R, C), not {tag}(_, _, R, C)."
