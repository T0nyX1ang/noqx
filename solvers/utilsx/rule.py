"""Utility for general clingo rules."""

from typing import Iterable, List, Tuple, Union

from .helper import ConnectivityHelper, tag_encode

rev_op_dict = {"eq": "!=", "ge": "<", "gt": "<=", "le": ">", "lt": ">=", "ne": "="}


def shade_c(color: str = "black") -> str:
    """
    Generate a rule that a cell is either {color} or not {color}.

    A grid fact should be defined first.
    """
    return f"{{ {color}(R, C) }} :- grid(R, C)."


def shade_cc(colors: List[str]) -> str:
    """
    Generates a rule that enforces several different {color} cells.

    A grid fact should be defined first.
    """
    return f"{{ {'; '.join(str(c) + '(R, C)' for c in colors)} }} = 1 :- grid(R, C)."


def fill_num(_range: Iterable[int], _type: str = "grid", _id: int = "A", color: str = None) -> str:
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

    raise ValueError("Invalid type, must be one of 'grid', 'area'.")


def count(target: int, op: str = "eq", color: str = "black", _type: str = "grid", _id: int = None) -> str:
    """
    Generates a constraint for counting the number of {color} cells in a grid / row / column / area.

    A grid fact should be defined first.
    """
    op = rev_op_dict[op]

    if _id is None:
        _id = "R" if _type == "row" else "C" if _type == "col" else None

    if _type == "grid":
        return f":- #count {{ grid(R, C) : {color}(R, C) }} {op} {target}."

    if _type == "row":
        return f":- grid({_id}, _), #count {{ C : {color}({_id}, C) }} {op} {target}."

    if _type == "col":
        return f":- grid(_, {_id}), #count {{ R : {color}(R, {_id}) }} {op} {target}."

    if _type == "area":
        return f":- #count {{ R, C : area({_id}, R, C), {color}(R, C) }} {op} {target}."

    raise ValueError("Invalid type, must be one of 'grid', 'row', 'col', 'area'.")


def adjacent(_type: Union[int, str] = 4) -> str:
    """
    Generates a rule for getting the adjacent neighbors.
    If _type = 4, then only orthogonal neighbors are considered.
    If _type = 8, then both orthogonal and diagonal neighbors are considered.

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
    op = rev_op_dict[op]
    return f":- #count {{ R, C: {color}(R, C), adj_{adj_type}(R, C, {src_r}, {src_c}) }} {op} {target}."


def count_adjacent_lines(target: int, src_cell: Tuple[int, int], op: str = "eq") -> str:
    """
    Return a rule that counts the adjacent lines around a cell.

    An edge rule should be defined first.
    """
    src_r, src_c = src_cell
    op = rev_op_dict[op]
    v_1 = f"vertical_line({src_r}, {src_c})"
    v_2 = f"vertical_line({src_r}, {src_c + 1})"
    h_1 = f"horizontal_line({src_r}, {src_c})"
    h_2 = f"horizontal_line({src_r + 1}, {src_c})"
    return f":- {{ {v_1}; {v_2}; {h_1}; {h_2} }} {op} {target}."


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

    raise ValueError("Invalid type, must be one of 'row', 'col', 'area'.")


def connected_parts(color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generate a rule to get all the grid_color_connected components of {color} cells.
    Please note that 'reachable/4' is much slower than the 'reachable/2' which only searches for one component.

    An adjacent rule and a grid fact should be defined first.
    """
    helper = ConnectivityHelper("reachable", "grid", color, adj_type)
    initial = helper.initial(full_search=True)
    propagation = helper.propagation(full_search=True)
    return initial + "\n" + propagation


def count_connected_parts(target: int, color: str = "black", adj_type: Union[int, str] = 4, op: str = "eq") -> str:
    """
    Generate a constraint to count the number of grid_color_connected components of {color} cells.

    A reachable rule should be defined first.
    """
    op = rev_op_dict[op]
    tag = tag_encode("reachable", "adj", adj_type, color)
    return f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {tag}(R, C, R1, C1) }} {op} {target}."


def count_region(
    target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: Union[int, str] = 4, op: str = "eq"
) -> str:
    """
    Generate a constraint to count the size of {color} region grid_color_connected to a source cell.

    A region rule should be defined first.
    """
    op = rev_op_dict[op]
    src_r, src_c = src_cell
    return f":- {{ {tag_encode('reachable', 'grid', 'src', 'adj', adj_type, color)}({src_r}, {src_c}, R, C) }} {op} {target}."


def count_lit(
    target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: Union[int, str] = 4, op: str = "eq"
) -> str:
    """
    Generate a constraint to count the number of {color} cells lit up by a source cell.

    A lit rule should be defined first.
    """
    op = rev_op_dict[op]
    src_r, src_c = src_cell
    return f":- {{ {tag_encode('reachable', 'bulb', 'src', 'adj', adj_type, color)}({src_r}, {src_c}, R, C) }} {op} {target}."


def reachable_edge() -> str:
    """
    Define edges as numbers on its adjacent grids are different.

    A grid fact and an adjacent edge rule should be defined first.
    """
    initial = "reachable_edge(R, C, R, C) :- grid(R, C).\n"
    propagation = "reachable_edge(R0, C0, R, C) :- grid(R, C), reachable_edge(R0, C0, R1, C1), adj_edge(R, C, R1, C1).\n"
    # edge between two reachable grids is forbidden.
    constraint = ":- reachable_edge(R, C, R, C + 1), vertical_line(R, C + 1).\n"
    constraint += ":- reachable_edge(R, C, R + 1, C), horizontal_line(R + 1, C).\n"
    constraint += ":- reachable_edge(R, C + 1, R, C), vertical_line(R, C + 1).\n"
    constraint += ":- reachable_edge(R + 1, C, R, C), horizontal_line(R + 1, C)."
    return initial + propagation + constraint


def count_reachable_edge(target: int, op: str = "eq", color: str = None) -> str:
    """
    Generates a constraint for counting grids in a region divided by edges.

    An edge rule should be defined first.
    """
    op = rev_op_dict[op]
    if not color:
        return f":- grid(R0, C0), #count {{ R, C: reachable_edge(R0, C0, R, C) }} {op} {target}."

    return f":- grid(R0, C0), {color}(R0, C0), #count {{ R, C: reachable_edge(R0, C0, R, C) }} {op} {target}."


def count_shape(target: int, name: str, _id: int = None, color: str = "black", _type: str = "grid", op: str = "eq") -> str:
    """
    Generates a constraint to count the number of a shape.

    A grid rule and a shape rule should be defined first.
    """
    tag = tag_encode("shape", name, color)
    op = rev_op_dict[op]
    _id = "_" if _id is None else _id

    if _type == "grid":
        return f":- {{ {tag}(R, C, {_id}, _) }} {op} {target}."

    if _type == "area":
        return f":- area(A, _, _), {{ {tag}(A, R, C, _, {_id}) }} {op} {target}."

    raise ValueError("Invalid type, must be one of 'grid', 'area'.")


def reachable_row(adj_type: int) -> str:
    """
    Generates a rule for reachable rows.
    """
    tag = tag_encode("reachable", "row", adj_type)
    rule = f"{tag}(R, C1, C2) :- grid(R, C1), C1 = C2.\n"
    rule += f"{tag}(R, C1, C2) :- grid(R, C1), grid(R, C2), C1 < C2, adj_{adj_type}(R, C2 - 1, R, C2), {tag}(R, C1, C2 - 1).\n"
    rule += f"{tag}(R, C1, C2) :- grid(R, C1), grid(R, C2), C1 > C2, {tag}(R, C2, C1)."
    return rule


def reachable_col(adj_type: int) -> str:
    """
    Generates a rule for reachable columns.
    """
    tag = tag_encode("reachable", "col", adj_type)
    rule = f"{tag}(R1, R2, C) :- grid(R1, C), R1 = R2.\n"
    rule += f"{tag}(R1, R2, C) :- grid(R1, C), grid(R2, C), R1 < R2, adj_{adj_type}(R2, C, R2 - 1, C), {tag}(R1, R2 - 1, C).\n"
    rule += f"{tag}(R1, R2, C) :- grid(R1, C), grid(R2, C), R1 > R2, {tag}(R2, R1, C)."
    return rule
