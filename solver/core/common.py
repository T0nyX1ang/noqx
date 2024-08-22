"""Generating commonly used facts and rules for the solver."""

from typing import Iterable, Optional, Tuple, Union

from .helper import target_encode


def display(item: str = "black", size: int = 2) -> str:
    """Generates a rule for displaying specific items with a certain size."""
    return f"#show {item}/{size}."


def grid(rows: int, cols: int) -> str:
    """Generates facts for a grid."""
    return f"grid(0..{rows - 1}, 0..{cols - 1})."


def area(_id: int, src_cells: Iterable[Tuple[int, int]]) -> str:
    """Generates facts for areas."""
    return "\n".join(f"area({_id}, {r}, {c})." for r, c in src_cells)


def shade_c(color: str = "black") -> str:
    """
    Generate a rule that a cell is either {color} or not {color}.

    A grid fact should be defined first.
    """
    return f"{{ {color}(R, C) }} :- grid(R, C)."


def shade_cc(colors: Iterable[str]) -> str:
    """
    Generates a rule that enforces several different {color} cells.

    A grid fact should be defined first.
    """
    return f"{{ {'; '.join(str(c) + '(R, C)' for c in colors)} }} = 1 :- grid(R, C)."


def edge(rows: int, cols: int) -> str:
    """
    Generates facts for grid edges.
    Note grid borders are set outside.
    """
    fact = f"vertical_range(0..{rows - 1}, 0..{cols}).\n"
    fact += f"horizontal_range(0..{rows}, 0..{cols - 1}).\n"
    fact += "{ edge_left(R, C) } :- vertical_range(R, C).\n"
    fact += "{ edge_top(R, C) } :- horizontal_range(R, C).\n"
    fact += f"edge_left(0..{rows - 1}, 0).\n"
    fact += f"edge_left(0..{rows - 1}, {cols}).\n"
    fact += f"edge_top(0, 0..{cols - 1}).\n"
    fact += f"edge_top({rows}, 0..{cols - 1})."
    return fact


def direction(directions: Union[str, list]) -> str:
    """Generates facts for directions."""
    format_d = map(lambda x: f'"{x}"', tuple(directions))
    return f"direction({';'.join(format_d)})."


def fill_path(color: str = "black", directed: bool = False) -> str:
    """
    Generate a rule that a cell is on a path.

    A grid fact and a direction fact should be defined first.
    """
    if directed:
        rule = f"{{ grid_in(R, C, D): direction(D) }} <= 1 :- grid(R, C), {color}(R, C).\n"
        rule += f"{{ grid_out(R, C, D): direction(D) }} <= 1 :- grid(R, C), {color}(R, C)."
        return rule

    return f"{{ grid_direction(R, C, D): direction(D) }} :- grid(R, C), {color}(R, C)."


def fill_num(_range: Iterable[int], _type: str = "grid", _id: Union[int, str] = "A", color: Optional[str] = None) -> str:
    """
    Generate a rule that a cell numbered within {_range}.
    {_range} should have the format "low..high", or "x;y;z" for a list of numbers.

    A grid fact or an area fact should be defined first.
    """
    color_part = "" if color is None else f"; {color}(R, C)"

    _range = sorted(set(_range))  # canonicize the range
    i, range_seq = 0, []

    while i < len(_range):
        start = i
        while i < len(_range) - 1 and _range[i + 1] - _range[i] == 1:
            i += 1
        end = i
        if start < end:
            range_seq.append(f"{_range[start]}..{_range[end]}")
        else:
            range_seq.append(str(_range[start]))
        i += 1

    range_str = f"{';'.join(range_seq)}"

    if _type == "grid":
        return f"{{ number(R, C, ({range_str})){color_part} }} = 1 :- grid(R, C)."

    if _type == "area":
        return f"{{ number(R, C, ({range_str})){color_part} }} = 1 :- area({_id}, R, C)."

    raise AssertionError("Invalid type, must be one of 'grid', 'area'.")


def unique_num(color: str = "black", _type: str = "row") -> str:
    """
    Generates a constraint for unique {color} numbered cells in a(an) row / column / area.
    {color} can be set to "grid" for wildcard colors.

    A number rule should be defined first.
    """
    if _type == "row":
        return f":- grid(_, C), number(_, _, N), {{ {color}(R, C) : number(R, C, N) }} > 1."

    if _type == "col":
        return f":- grid(R, _), number(_, _, N), {{ {color}(R, C) : number(R, C, N) }} > 1."

    if _type == "area":
        return f":- area(A, _, _), number(_, _, N), {{ {color}(R, C) : area(A, R, C), number(R, C, N) }} > 1."

    raise AssertionError("Invalid type, must be one of 'row', 'col', 'area'.")


def count(
    target: Union[int, Tuple[str, int]], color: str = "black", _type: str = "grid", _id: Optional[Union[int, str]] = None
) -> str:
    """
    Generates a constraint for counting the number of {color} cells in a grid / row / column / area.

    A grid fact should be defined first.
    """
    rop, num = target_encode(target)

    if _id is None:
        _id = "R" if _type == "row" else "C" if _type == "col" else None

    if _type == "grid":
        return f":- #count {{ grid(R, C) : {color}(R, C) }} {rop} {num}."

    if _type == "row":
        return f":- grid({_id}, _), #count {{ C : {color}({_id}, C) }} {rop} {num}."

    if _type == "col":
        return f":- grid(_, {_id}), #count {{ R : {color}(R, {_id}) }} {rop} {num}."

    if _type == "area":
        return f":- #count {{ R, C : area({_id}, R, C), {color}(R, C) }} {rop} {num}."

    raise AssertionError("Invalid type, must be one of 'grid', 'row', 'col', 'area'.")
