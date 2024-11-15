"""Rules and constraints to detect certain shapes."""

import itertools
from typing import Iterable, Optional, Set, Tuple, Union

from .helper import tag_encode, target_encode, validate_type

OMINOES = {
    1: {
        ".": ((0, 0),),
    },
    2: {
        "I": ((0, 0), (1, 0)),
    },
    3: {
        "I": ((0, 0), (1, 0), (2, 0)),
        "L": ((0, 0), (0, 1), (1, 0)),
    },
    4: {
        "T": ((0, 0), (1, 0), (1, 1), (2, 0)),
        "O": ((0, 0), (0, 1), (1, 0), (1, 1)),
        "I": ((0, 0), (1, 0), (2, 0), (3, 0)),
        "L": ((0, 0), (1, 0), (2, 0), (2, 1)),
        "S": ((0, 0), (0, 1), (1, 1), (1, 2)),
    },
    5: {
        "F": ((0, 0), (0, 1), (1, -1), (1, 0), (2, 0)),
        "I": ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)),
        "L": ((0, 0), (1, 0), (2, 0), (3, 0), (3, 1)),
        "N": ((0, 0), (0, 1), (1, 1), (1, 2), (1, 3)),
        "P": ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0)),
        "T": ((0, 0), (0, 1), (0, 2), (1, 1), (2, 1)),
        "U": ((0, 0), (0, 2), (1, 0), (1, 1), (1, 2)),
        "V": ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
        "W": ((0, 0), (0, 1), (1, 1), (1, 2), (2, 2)),
        "X": ((0, 0), (1, -1), (1, 0), (1, 1), (2, 0)),
        "Y": ((0, 0), (1, -1), (1, 0), (1, 1), (1, 2)),
        "Z": ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2)),
    },
}


def get_neighbor(r: int, c: int, _type: Union[int, str] = 4) -> Iterable[Tuple[int, int]]:
    """Get the neighbors of a cell."""
    shape_4 = ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))
    shape_x = ((r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1))

    if _type == 4:
        return shape_4

    if _type == "x":
        return shape_x

    if _type == 8:
        return shape_4 + shape_x

    raise AssertionError("Invalid type, must be one of 4, 8, 'x'.")


def canonicalize_shape(shape: Iterable[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
    """
    Given a (possibly non-canonical) shape representation,

    Return the canonical representation of the shape, a tuple:
        - in sorted order
        - whose first element is (0, 0)
        - whose other elements represent the offsets of the other cells from the first one
    """
    shape = sorted(shape)
    root_r, root_c = shape[0]
    dr, dc = -1 * root_r, -1 * root_c
    return tuple((r + dr, c + dc) for r, c in shape)


def get_variants(
    shape: Iterable[Tuple[int, int]], allow_rotations: bool, allow_reflections: bool
) -> Set[Iterable[Tuple[int, int]]]:
    """
    Get a set of canonical shape representations for a (possibly non-canonical) shape representation.

    allow_rotations = True iff shapes can be rotated
    allow_reflections = True iff shapes can be reflected
    """
    # build a set of functions that transform shapes
    # in the desired ways
    functions = set()
    if allow_rotations:
        functions.add(lambda shape: canonicalize_shape((-c, r) for r, c in shape))
    if allow_reflections:
        functions.add(lambda shape: canonicalize_shape((-r, c) for r, c in shape))

    # make a set of currently found shapes
    result = set()
    result.add(canonicalize_shape(shape))

    # apply our functions to the items in this set
    all_shapes_covered = False
    while not all_shapes_covered:
        new_shapes = set()
        current_num_shapes = len(result)
        for f, s in itertools.product(functions, result):
            new_shapes.add(f(s))
        result = result.union(new_shapes)
        all_shapes_covered = current_num_shapes == len(result)
    return result


def general_shape(
    name: str,
    _id: int = 0,
    deltas: Optional[Iterable[Tuple[int, int]]] = None,
    color: str = "black",
    _type: str = "grid",
    adj_type: Union[int, str] = 4,
    simple: bool = False,
) -> str:
    """
    Generates a rule for general shapes (using bruteforce technique).
    The deltas are the relative coordinates of the shape cells.

    A grid rule and an adjacent rule should be defined first.
    """
    validate_type(_type, ("grid", "area"))
    if not deltas:
        raise AssertionError("Shape coordinates must be provided.")

    tag = tag_encode("shape", name, color)
    tag_be = tag_encode("belong_to_shape", name, color)
    neighbor_type = adj_type if adj_type in [4, 8, "x"] else 4
    data = ""

    variants = get_variants(deltas, allow_rotations=True, allow_reflections=True)
    for i, variant in enumerate(variants):
        valid, belongs_to = set(), set()
        for dr, dc in variant:
            if _type == "grid":
                valid.add(f"grid(R + {dr}, C + {dc})")
                valid.add(f"{color}(R + {dr}, C + {dc})")
                belongs_to.add(
                    f"{tag_be}(R + {dr}, C + {dc}, {_id}, {i}) :- grid(R + {dr}, C + {dc}), {tag}(R, C, {_id}, {i})."
                )

            if _type == "area":
                valid.add(f"area(A, R + {dr}, C + {dc})")
                valid.add(f"{color}(R + {dr}, C + {dc})")
                belongs_to.add(
                    f"{tag_be}(A, R + {dr}, C + {dc}, {_id}, {i}) :- area(A, R + {dr}, C + {dc}), {tag}(A, R, C, {_id}, {i})."
                )

            for nr, nc in get_neighbor(dr, dc, _type=neighbor_type):
                if (nr, nc) in variant:
                    if adj_type not in [4, 8, "x"] and (dr, dc) < (nr, nc):
                        valid.add(f"adj_{adj_type}(R + {dr}, C + {dc}, R + {nr}, C + {nc})")
                        valid.add(f"{color}(R + {nr}, C + {nc})")
                elif not simple:  # Skip the adjacency re-check if it is simple
                    if color == "grid":  # Simplify the adjacency re-check if the color is set to 'grid'
                        valid.add(f"not adj_{adj_type}(R + {dr}, C + {dc}, R + {nr}, C + {nc})")
                    else:
                        valid.add(
                            f"{{ not adj_{adj_type}(R + {dr}, C + {dc}, R + {nr}, C + {nc}); not {color}(R + {nr}, C + {nc}) }} > 0"
                        )

        if _type == "grid":
            data += f"{tag}(R, C, {_id}, {i}) :- grid(R, C), {', '.join(valid)}.\n" + "\n".join(belongs_to) + "\n"

        if _type == "area":
            data += f"{tag}(A, R, C, {_id}, {i}) :- area(A, R, C), {', '.join(valid)}.\n" + "\n".join(belongs_to) + "\n"

    return data.strip()


def all_shapes(name: str, color: str = "black", _type: str = "grid") -> str:
    """
    Generate a constraint to force all {color} cells are in defined shapes.

    A grid rule and a shape/belong_to_shape rule should be defined first.
    """
    validate_type(_type, ("grid", "area"))
    tag = tag_encode("belong_to_shape", name, color)

    rule = ""
    if _type == "grid":
        rule = f":- grid(R, C), {color}(R, C), not {tag}(R, C, _, _)."

    if _type == "area":
        rule = f":- area(A, R, C), {color}(R, C), not {tag}(A, R, C, _, _)."

    return rule


def count_shape(
    target: Union[int, Tuple[str, int]],
    name: str,
    _id: Optional[Union[int, str]] = None,
    color: str = "black",
    _type: str = "grid",
) -> str:
    """
    Generates a constraint to count the number of a shape.

    A grid rule and a shape rule should be defined first.
    """
    validate_type(_type, ("grid", "area"))
    tag = tag_encode("shape", name, color)
    rop, num = target_encode(target)
    _id = "_" if _id is None else _id

    rule = ""
    if _type == "grid":
        rule = f":- {{ {tag}(R, C, {_id}, _) }} {rop} {num}."

    if _type == "area":
        rule = f":- area(A, _, _), {{ {tag}(A, R, C, _, {_id}) }} {rop} {num}."

    return rule


def all_rect(color: str = "black", square: bool = False) -> str:
    """
    Generate a constraint to force rectangles.

    A grid rule should be defined first.
    """
    upleft = f"upleft(R, C) :- grid(R, C), {color}(R, C), not {color}(R - 1, C), not {color}(R, C - 1).\n"
    left = f"left(R, C) :- grid(R, C), {color}(R, C), upleft(R - 1, C), {color}(R - 1, C), not {color}(R, C - 1).\n"
    left += f"left(R, C) :- grid(R, C), {color}(R, C), left(R - 1, C), {color}(R - 1, C), not {color}(R, C - 1).\n"
    up = f"up(R, C) :- grid(R, C), {color}(R, C), upleft(R, C - 1), {color}(R, C - 1), not {color}(R - 1, C).\n"
    up += f"up(R, C) :- grid(R, C), {color}(R, C), up(R, C - 1), {color}(R, C - 1), not {color}(R - 1, C).\n"
    remain = "remain(R, C) :- grid(R, C), left(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), left(R, C - 1), remain(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), remain(R - 1, C).\n"

    if color.startswith("not "):  # additional boundary check if the color starts with "not"
        upleft += f"upleft(0, 0) :- grid(0, 0), {color}(0, 0).\n"
        upleft += f"upleft(R, 0) :- grid(R, 0), {color}(R, 0), not {color}(R - 1, 0).\n"
        upleft += f"upleft(0, C) :- grid(0, C), {color}(0, C), not {color}(0, C - 1).\n"
        left += f"left(R, 0) :- grid(R, 0), {color}(R, 0), upleft(R - 1, 0), {color}(R - 1, 0).\n"
        left += f"left(R, 0) :- grid(R, 0), {color}(R, 0), left(R - 1, 0), {color}(R - 1, 0).\n"
        up += f"up(0, C) :- grid(0, C), {color}(0, C), upleft(0, C - 1), {color}(0, C - 1).\n"
        up += f"up(0, C) :- grid(0, C), {color}(0, C), up(0, C - 1), {color}(0, C - 1).\n"

    constraint = f":- grid(R, C), {color}(R, C), not upleft(R, C), not left(R, C), not up(R, C), not remain(R, C).\n"
    constraint += f":- grid(R, C), remain(R, C), not {color}(R, C).\n"

    if square:
        c_min = f"#min {{ C0: grid(R, C0 - 1), not {color}(R, C0), C0 > C }}"
        r_min = f"#min {{ R0: grid(R0 - 1, C), not {color}(R0, C), R0 > R }}"
        constraint += f":- upleft(R, C), MR = {r_min}, MC = {c_min}, MR - R != MC - C.\n"
        constraint += ":- upleft(R, C), left(R + 1, C), not up(R, C + 1).\n"
        constraint += ":- upleft(R, C), not left(R + 1, C), up(R, C + 1).\n"

    data = upleft + left + up + remain + constraint
    return data.replace("not not ", "").strip()


def all_rect_region() -> str:
    """
    Generate a constraint to force rectangles.

    A grid rule and an edge rule should be defined first.
    """
    upleft = "upleft(R, C) :- grid(R, C), edge_left(R, C), edge_top(R, C)."
    left = "left(R, C) :- grid(R, C), upleft(R - 1, C), edge_left(R, C), not edge_top(R, C).\n"
    left += "left(R, C) :- grid(R, C), left(R - 1, C), edge_left(R, C), not edge_top(R, C)."
    up = "up(R, C) :- grid(R, C), upleft(R, C - 1), edge_top(R, C), not edge_left(R, C).\n"
    up += "up(R, C) :- grid(R, C), up(R, C - 1), edge_top(R, C), not edge_left(R, C)."
    remain = "remain(R, C) :- grid(R, C), left(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), left(R, C - 1), remain(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), remain(R - 1, C)."

    constraint = ":- grid(R, C), { upleft(R, C); left(R, C); up(R, C); remain(R, C) } != 1.\n"
    constraint += ":- grid(R, C), remain(R, C), left(R, C + 1), not edge_left(R, C + 1).\n"
    constraint += ":- grid(R, C), remain(R, C), up(R + 1, C), not edge_top(R + 1, C).\n"
    constraint += ":- grid(R, C), remain(R, C), upleft(R, C + 1), not edge_left(R, C + 1).\n"
    constraint += ":- grid(R, C), remain(R, C), upleft(R + 1, C), not edge_top(R + 1, C)."

    rect = ":- grid(R, C), left(R, C), remain(R, C + 1), edge_left(R, C + 1).\n"
    rect += ":- grid(R, C), remain(R, C), remain(R, C + 1), edge_left(R, C + 1).\n"
    rect += ":- grid(R, C), up(R, C), remain(R + 1, C), edge_top(R + 1, C).\n"
    rect += ":- grid(R, C), remain(R, C), remain(R + 1, C), edge_top(R + 1, C)."

    data = upleft + "\n" + left + "\n" + up + "\n" + remain + "\n" + constraint + "\n" + rect
    return data


def avoid_rect(
    rect_r: int, rect_c: int, corner: Tuple[Optional[int], Optional[int]] = (None, None), color: str = "black"
) -> str:
    """
    Generates a constraint to avoid rectangular patterned {color} cells.

    A grid fact should be defined first.
    """
    corner_r, corner_c = corner
    corner_r = corner_r if corner_r is not None else "R"
    corner_c = corner_c if corner_c is not None else "C"

    if corner_r != "R" and corner_c != "C":
        rect_pattern = [f"{color}({corner_r + r}, {corner_c + c})" for r in range(rect_r) for c in range(rect_c)]
    else:
        rect_pattern = [f"{color}({corner_r} + {r}, {corner_c} + {c})" for r in range(rect_r) for c in range(rect_c)]
        rect_pattern.append(f"grid({corner_r}, {corner_c})")
        rect_pattern.append(f"grid({corner_r} + {rect_r - 1}, {corner_c} + {rect_c - 1})")

    return f":- {', '.join(rect_pattern)}."


def area_same_color(color: str = "black") -> str:
    """Ensure that all cells in the same area have the same color."""
    return f":- area(A, R, C), area(A, R1, C1), {color}(R, C), not {color}(R1, C1)."
