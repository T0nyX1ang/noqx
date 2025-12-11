"""Rules and constraints to detect certain shapes."""

from typing import Iterable, Optional, Set, Tuple, Union

from noqx.rule.helper import tag_encode, target_encode, validate_type

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


def canonicalize_shape(shape: Iterable[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
    """Convert a shape to its canonical representation.

    * The representation of a shape containing all the cells that consist of the shape, and:
        * the first element can be any coordinate,
        * the other element represent the offsets of the other cells from the first one.

    * The **canonical** representation of the shape is a sorted tuple, and:
        * the first element is `(0, 0)`,
        * the other elements represent the offsets of the other cells from the first one.

    Args:
        shape: the representation of a shape.
    """
    shape = sorted(shape)
    root_r, root_c = shape[0]
    dr, dc = -1 * root_r, -1 * root_c
    return tuple((r + dr, c + dc) for r, c in shape)


def get_variants(
    shape: Iterable[Tuple[int, int]], allow_rotations: bool, allow_reflections: bool
) -> Set[Iterable[Tuple[int, int]]]:
    """Generate the equivalent variants for a shape.

    Args:
        shape: the representation of a shape.
        allow_rotations: Whether the shapes can be rotated to build the variants.
        allow_reflections: Whether the shapes can be reflected to build the variants.
    """
    functions = set()
    if allow_rotations:
        functions.add(lambda shape: canonicalize_shape((-c, r) for r, c in shape))
    if allow_reflections:
        functions.add(lambda shape: canonicalize_shape((-r, c) for r, c in shape))

    result = set()
    result.add(canonicalize_shape(shape))

    all_shapes_covered = False
    while not all_shapes_covered:
        new_shapes = set()
        current_num_shapes = len(result)
        for f in functions:
            new_shapes.update(f(s) for s in result)

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
    """A rule to define general shapes in a grid or an area.

    * Two predicates will be generated, `shape` and `belong_to_shape`. The `shape` predicate
    defines the shape pattern, while the `belong_to_shape` predicate defines whether a cell
    belongs to a certain shape instance.

    Args:
        name: The name of the shape.
        _id: The ID of the shape, needs to be unique.
        deltas: The relative coordinates of the shape cells.
        color: The color to be checked.
        _type: The type of the shape rule (accepted types: "grid" or "area").
        adj_type: The type of adjacency (accepted types: `4`, `8`, `x`, `loop`, `loop_directed`).
        simple: Whether to skip the adjacency re-checking.

    Warning:
        Although the shape representation does not require the connectivity of the shape,
        it is recommended to ensure that the provided shape is connected. Some derived rules
        may behave weird if the shape is not connected.

    Warning:
        The `simple` option is more efficient, but the use-case is limited. It is only recommended to use
        in the `area` type, and every area only contains **one piece** of the shape.
    """

    def get_neighbor(r: int, c: int) -> Iterable[Tuple[int, int]]:
        """Get the 4-directional neighbors of a cell."""
        return ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))

    validate_type(_type, ("grid", "area"))
    if not deltas:
        raise ValueError("Shape coordinates must be provided.")

    tag = tag_encode("shape", name, color)
    tag_be = tag_encode("belong_to_shape", name, color)
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

            for nr, nc in get_neighbor(dr, dc):
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

    return data


def all_shapes(name: str, color: str = "black", _type: str = "grid") -> str:
    """A rule to ensure all the color cells belong to defined shapes in a grid or an area.

    Args:
        name: The name of the shape.
        color: The color to be checked.
        _type: The type of the shape rule (accepted types: "grid" or "area").

    Warning:
        The generated tags of the shapes are without the adjacency type and ID.
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
    """A rule to compare the number of certain shapes to a specified target.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        name: The name of the shape.
        _id: The ID of the shape. If not provided, all the shapes with different IDs will be counted.
        color: The color to be checked.
        _type: The type of the shape rule (accepted types: "grid" or "area").

    Warning:
        The generated tags of the shapes are without the adjacency type and ID.
    """
    validate_type(_type, ("grid", "area"))
    tag = tag_encode("shape", name, color)
    rop, num = target_encode(target)
    _id = "_" if _id is None else _id

    rule = ""
    if _type == "grid":
        rule = f":- {{ {tag}(R, C, {_id}, _) }} {rop} {num}."

    if _type == "area":
        rule = f":- area(A, _, _), {{ {tag}(A, R, C, {_id}, _) }} {rop} {num}."

    return rule


def all_rect(color: str = "black", square: bool = False) -> str:
    """A rule to ensure that all the shapes (recognized by colors) in the grid are rectangles.

    * The main concept of this rule is to define four helper predicates: `upleft`, `left`, `up`, and `remain`,
    and categorize all the cells into these predicates. If some cells are missing, the shape is not rectangular.

    * Due to technical reasons, the color cannot start with `not`, and the `noqx.common.invert_c` rule can help.

    Args:
        color: The color to be checked.
        square: Whether to force the rectangles to be squares.

    Raises:
        ValueError: If the color starts with 'not'.

    Warning:
        This rule is available with only *one* color, since the helper predicates are not relevant to colors.
    """
    rule = ""
    if color.startswith("not"):
        raise ValueError("Unsupported color prefix 'not', please define the color explicitly.")

    upleft = f"upleft(R, C) :- grid(R, C), {color}(R, C), not {color}(R - 1, C), not {color}(R, C - 1).\n"
    left = f"left(R, C) :- grid(R, C), {color}(R, C), upleft(R - 1, C), {color}(R - 1, C), not {color}(R, C - 1).\n"
    left += f"left(R, C) :- grid(R, C), {color}(R, C), left(R - 1, C), {color}(R - 1, C), not {color}(R, C - 1).\n"
    up = f"up(R, C) :- grid(R, C), {color}(R, C), upleft(R, C - 1), {color}(R, C - 1), not {color}(R - 1, C).\n"
    up += f"up(R, C) :- grid(R, C), {color}(R, C), up(R, C - 1), {color}(R, C - 1), not {color}(R - 1, C).\n"
    remain = "remain(R, C) :- grid(R, C), left(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), left(R, C - 1), remain(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), remain(R - 1, C).\n"

    constraint = f":- grid(R, C), {color}(R, C), not upleft(R, C), not left(R, C), not up(R, C), not remain(R, C).\n"
    constraint += f":- grid(R, C), remain(R, C), not {color}(R, C).\n"

    if square:
        c_min = f"#min {{ C0: grid(R, C0 - 1), not {color}(R, C0), C0 > C }}"
        r_min = f"#min {{ R0: grid(R0 - 1, C), not {color}(R0, C), R0 > R }}"
        constraint += f":- upleft(R, C), MR = {r_min}, MC = {c_min}, MR - R != MC - C.\n"
        constraint += ":- upleft(R, C), left(R + 1, C), not up(R, C + 1).\n"
        constraint += ":- upleft(R, C), not left(R + 1, C), up(R, C + 1).\n"

    data = rule + upleft + left + up + remain + constraint
    return data


def all_rect_region(square: bool = False) -> str:
    """A rule to ensure that all the shapes (recognized by edges) in the grid are rectangles.

    Args:
        square: Whether to force the rectangles to be squares.
    """
    upleft = "upleft(R, C) :- grid(R, C), edge_left(R, C), edge_top(R, C).\n"
    left = "left(R, C) :- grid(R, C), upleft(R - 1, C), edge_left(R, C), not edge_top(R, C).\n"
    left += "left(R, C) :- grid(R, C), left(R - 1, C), edge_left(R, C), not edge_top(R, C).\n"
    up = "up(R, C) :- grid(R, C), upleft(R, C - 1), edge_top(R, C), not edge_left(R, C).\n"
    up += "up(R, C) :- grid(R, C), up(R, C - 1), edge_top(R, C), not edge_left(R, C).\n"
    remain = "remain(R, C) :- grid(R, C), left(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), left(R, C - 1), remain(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), remain(R - 1, C).\n"

    constraint = ":- grid(R, C), { upleft(R, C); left(R, C); up(R, C); remain(R, C) } != 1.\n"
    constraint += ":- grid(R, C), remain(R, C), left(R, C + 1), not edge_left(R, C + 1).\n"
    constraint += ":- grid(R, C), remain(R, C), up(R + 1, C), not edge_top(R + 1, C).\n"
    constraint += ":- grid(R, C), remain(R, C), upleft(R, C + 1), not edge_left(R, C + 1).\n"
    constraint += ":- grid(R, C), remain(R, C), upleft(R + 1, C), not edge_top(R + 1, C).\n"

    if square:
        c_min = "#min { C0: grid(R, C0 - 1), edge_left(R, C0), C0 > C }"
        r_min = "#min { R0: grid(R0 - 1, C), edge_top(R0, C), R0 > R }"
        constraint += f":- upleft(R, C), MR = {r_min}, MC = {c_min}, MR - R != MC - C.\n"

    rect = ":- grid(R, C), left(R, C), remain(R, C + 1), edge_left(R, C + 1).\n"
    rect += ":- grid(R, C), remain(R, C), remain(R, C + 1), edge_left(R, C + 1).\n"
    rect += ":- grid(R, C), up(R, C), remain(R + 1, C), edge_top(R + 1, C).\n"
    rect += ":- grid(R, C), remain(R, C), remain(R + 1, C), edge_top(R + 1, C)."

    data = upleft + left + up + remain + constraint + rect
    return data


def avoid_rect(
    rect_r: int, rect_c: int, color: str = "black", corner: Tuple[Optional[int], Optional[int]] = (None, None)
) -> str:
    """A rule to avoid rectangular shapes of specified size in a grid.

    Args:
        rect_r: The height (rows) of the rectangle.
        rect_c: The width (columns) of the rectangle.
        color: The color to be checked.
        corner: The corner of the rectangle in (`row`, `col`), set to `None` to check for any rows or cols.
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


def no_rect(color: str = "black") -> str:
    """A rule to avoid rectangular shapes of any size in a grid.

    * The main concept of this rule is to detect `L-shape` and ensure that
    all the color cells are reachable through `L-shape`.

    Args:
        color: The color to be checked.
    """
    tag = tag_encode("reachable", "Lshape", "adj", 4, color)

    mutual = "grid(R, C), grid(R + 1, C + 1)"
    initial = f"{tag}(R, C) :- {mutual}, {color}(R, C), {color}(R, C + 1), {color}(R + 1, C), not {color}(R + 1, C + 1).\n"
    initial += f"{tag}(R, C) :- {mutual}, {color}(R, C), {color}(R, C + 1), {color}(R + 1, C + 1), not {color}(R + 1, C).\n"
    initial += f"{tag}(R, C) :- {mutual}, {color}(R, C), {color}(R + 1, C), {color}(R + 1, C + 1), not {color}(R, C + 1).\n"
    initial += (
        f"{tag}(R + 1, C + 1) :- {mutual}, not {color}(R, C), {color}(R, C + 1), {color}(R + 1, C), {color}(R + 1, C + 1).\n"
    )
    propagation = f"{tag}(R, C) :- {tag}(R1, C1), {color}(R, C), adj_4(R, C, R1, C1).\n"
    constraint = f":- grid(R, C), {color}(R, C), not {tag}(R, C)."
    return initial + propagation + constraint


def count_rect_size(
    target: Union[int, Tuple[str, int]],
    src_cell: Tuple[int, int],
    color: Optional[str] = None,
    adj_type: Union[int, str] = 4,
) -> str:
    """A rule to compare the the size of a rectangle (starting from a source) to a specified target.

    * A `noqx.reachable.bulb_src_color_connected` rule should be applied first.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        src_cell: The source cell of the rectangle.
        color: The color to be checked. If it is `None`, only the `edge` adjacency is accepted.
        adj_type: The type of adjacency (accepted types: `4`, `8`, `x`, `loop`, `loop_directed`).
    """
    if color is None:
        validate_type(adj_type, ("edge",))

    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)
    rop, num = target_encode(target)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {count_r}, {count_c}, CR * CC {rop} {num}."


def avoid_edge_crossover() -> str:
    """A rule to avoid the crossover shape of edges.

    * This rule is useful in tatami-like puzzles.
    """
    no_rect_adjacent_by_point = [
        "edge_left(R, C + 1)",
        "edge_left(R + 1, C + 1)",
        "edge_top(R + 1, C)",
        "edge_top(R + 1, C + 1)",
    ]
    rule = f":- grid(R, C), {', '.join(no_rect_adjacent_by_point)}."
    return rule
