"""Utility for reachable things and connectivity tests."""

from typing import Tuple, Union

from .helper import tag_encode


def validate_type(_type: Union[int, str], target_type: Tuple[Union[int, str]]) -> None:
    """Validate any matching type."""
    if _type not in target_type:
        raise ValueError(f"Invalid type '{_type}'.")


def grid_color_connected(color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells.

    An adjacent rule and a grid fact should be defined first.
    """
    validate_type(adj_type, (4, 8, "loop", "loop_directed"))
    tag = tag_encode("reachable", "grid", "adj", adj_type, color)
    initial = f"{tag}(R, C) :- (R, C) = #min{{ (R1, C1): grid(R1, C1), {color}(R1, C1) }}."
    propagation = f"{tag}(R, C) :- {tag}(R1, C1), grid(R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
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
