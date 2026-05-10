"""Rules and constraints to detect certain shapes."""

from collections import deque
from typing import Dict, Iterable, List, Optional, Set, Tuple, Union

from noqx.puzzle import Direction
from noqx.rule.helper import fail_false, tag_encode, target_encode, validate_type

OMINOES: Dict[int, Dict[str, Tuple[Tuple[int, int], ...]]] = {
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
        "F": ((0, 0), (1, 0), (1, 1), (1, 2), (2, 1)),
        "I": ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)),
        "L": ((0, 0), (1, 0), (2, 0), (3, 0), (3, 1)),
        "N": ((0, 0), (0, 1), (1, 1), (1, 2), (1, 3)),
        "P": ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0)),
        "T": ((0, 0), (0, 1), (0, 2), (1, 1), (2, 1)),
        "U": ((0, 0), (0, 2), (1, 0), (1, 1), (1, 2)),
        "V": ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
        "W": ((0, 0), (0, 1), (1, 1), (1, 2), (2, 2)),
        "X": ((0, 1), (1, 0), (1, 1), (2, 1), (1, 2)),
        "Y": ((0, 0), (1, 0), (1, 1), (2, 0), (3, 0)),
        "Z": ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2)),
    },
}


def normalize_shape(shape: Iterable[Tuple[int, int]]) -> Tuple[Tuple[int, int], ...]:
    """Normalize a shape to its canonical representation.

    * The **canonical** representation of the shape is a sorted tuple representing the offsets from `(0, 0)`.

    Args:
        shape: the representation of a shape.
    """
    shape = sorted(shape)
    min_r = min(r for r, _ in shape)
    min_c = min(c for _, c in shape)
    return tuple((r - min_r, c - min_c) for r, c in shape)


def get_variants(
    shape: Iterable[Tuple[int, int]], allow_rotations: bool, allow_reflections: bool
) -> Set[Tuple[Tuple[int, int], ...]]:
    """Generate the equivalent variants for a shape.

    Args:
        shape: the representation of a shape.
        allow_rotations: Whether the shapes can be rotated to build the variants.
        allow_reflections: Whether the shapes can be reflected to build the variants.
    """
    shape = normalize_shape(shape)
    result: Set[Tuple[Tuple[int, int], ...]] = {shape}
    queue = deque([shape], 8)
    while queue:
        current_shape = queue.popleft()
        new_shapes: Set[Tuple[Tuple[int, int], ...]] = set()

        if allow_rotations:
            new_shapes.add(normalize_shape((-c, r) for r, c in current_shape))

        if allow_reflections:
            new_shapes.add(normalize_shape((-r, c) for r, c in current_shape))

        for new_shape in new_shapes:
            if new_shape not in result:
                result.add(new_shape)
                queue.append(new_shape)

    return result


def parse_shape(shape_str: str) -> Tuple[Tuple[int, int], ...]:
    """Parse a shape string into a tuple of coordinates.

    * The shape string is a string where `1` represents a shaded cell and `0` represents an unshaded cell, and the "|" character is used to separate rows.
    * The coordinates are represented and normalized as (row, column) tuples, where the top-left cell is (0, 0).

    Args:
        shape_str: The shape string to be parsed.
    """

    rows = shape_str.split("|")
    coord: List[Tuple[int, int]] = []
    col_length = len(rows[0])

    for r, row in enumerate(rows):
        fail_false(len(row) == col_length, "Invalid shape size.")
        for c, cell in enumerate(row):
            fail_false(cell in ("0", "1"), "Invalid shape expression.")
            if cell == "1":
                coord.append((r, c))

    return normalize_shape(coord)


def parse_shapeset(shapeset: List[Dict[str, Union[int, str]]]) -> Dict[Tuple[Tuple[int, int], ...], int]:
    """Parse a shapeset argument into a dictionary of shape coordinates with their counts.

    * The shape set is a list of dictionaries, where each dictionary has a "shape" key whose value is a shape string, and a "count" key whose value is the number of shapes of that type.

    Args:
        shapeset: The shape set argument to be parsed.
    """
    result: Dict[Tuple[Tuple[int, int], ...], int] = {}
    for shape_dict in shapeset:
        shape = parse_shape(str(shape_dict["shape"]))
        count = int(shape_dict["count"])
        result[shape] = count  # TODO: add tolerance for equivalent shapes

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
        adj_type: The type of adjacency (accepted types: `4`, `8`, `x`, `line`, `line_directed`).
        simple: Whether to skip the adjacency re-checking.

    Success:
        * If `_type` is set to "grid", this rule will generate two predicates named `shape_{name}_{color}(R, C)` and `belong_to_shape_{name}_{color}(R, C, I, V)`.

        * If `_type` is set to "area", this rule will generate two predicates named `shape_{name}_{color}(R, C)` and `belong_to_shape_{name}_{color}(A, R, C, I, V)`.

    Warning:
        Although the shape representation does not require the connectivity of the shape, it is recommended to ensure that the provided shape is connected. Some derived rules may behave weird if the shape is not connected.

    Warning:
        The `simple` option is more efficient, but the use-case is limited. It is only recommended to use in the `area` type, and every area only contains **one piece** of the shape.

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
            data += f"{tag}(R, C, {_id}, {i}) :- {', '.join(valid)}.\n" + "\n".join(belongs_to) + "\n"

        if _type == "area":
            data += f"{tag}(A, R, C, {_id}, {i}) :- {', '.join(valid)}.\n" + "\n".join(belongs_to) + "\n"

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


def avoid_same_omino_adjacent(
    omino_num: int, color: str = "black", adj_type: Union[int, str] = 4, allow_isometry: bool = True
) -> str:
    """A rule to avoid adjacent ominos with the same shape.

    Args:
        omino_num: The number of cells in the omino.
        color: The color to be checked.
        adj_type: The type of adjacency (accepted values: `4`, `8`, `x`, `edge`).
        allow_isometry: Whether to consider reflection/rotation as the same type.

    Warning:
        This rule only deals with `grid-based` ominos currently and cannot deal with `area-based` ominos.
    """
    validate_type(adj_type, (4, 8, "x", "edge"))
    t_be = tag_encode("belong_to_shape", "omino", omino_num, color)
    itag = "_" if allow_isometry else "V"

    rule = ""
    if adj_type == 4:  # only checkerboard adjacent ominos are allowed
        rule = f":- not {color}(R, C + 1), not {color}(R + 1, C), {t_be}(R, C, T, {itag}), {t_be}(R + 1, C + 1, T, {itag}).\n"
        rule += f":- not {color}(R, C), not {color}(R + 1, C + 1), {t_be}(R + 1, C, T, {itag}), {t_be}(R, C + 1, T, {itag})."

    if adj_type in (8, "x"):  # all adjacent ominos are not allowed
        rule += f":- adj_{adj_type}(R, C, R1, C1), {t_be}(R, C, T, {itag}), {t_be}(R1, C1, T1, {itag}), T != T1."

    if adj_type == "edge":
        rule += f':- grid(R, C), grid(R, C + 1), {t_be}(R, C, T, {itag}), {t_be}(R, C + 1, T, {itag}), edge(R, C + 1, "{Direction.LEFT}").\n'
        rule += f':- grid(R, C), grid(R + 1, C), {t_be}(R, C, T, {itag}), {t_be}(R + 1, C, T, {itag}), edge(R + 1, C, "{Direction.TOP}").'
    return rule


def all_rect(color: str = "black", square: bool = False) -> str:
    """A rule to ensure that all the shapes (recognized by colors) in the grid are rectangles.

    * The main concept of this rule is to define the `rect` predicate with four directions: `top-left`, `left`, `top`, and `bottom-right`, and categorize all the cells into these directions:
        * `top-left`: the **top-left** corner of a rectangle.
        * `left`: the **left** edge of a rectangle (excluding the **top-left** corner).
        * `top`: the **top** edge of a rectangle (excluding the **top-left** corner).
        * `bottom-right`: all the *remaining* cells inside the rectangle.

    * If some cells are not categorized into the `rect` predicate, the shape is not rectangular.

    * Due to technical reasons with edges, the color cannot start with `not`, please use the `noqx.rule.common.invert_c` rule for assistance.

    Args:
        color: The color to be checked.
        square: Whether to force the rectangles to be squares.

    Raises:
        ValueError: If the color starts with 'not'.

    Success:
        This rule will generate a predicate named `rect(R, C, D)`.

    Warning:
        This rule is available with only *one* color, since the helper predicates are not relevant to colors.

    Warning:
        This rule conflicts with `all_rect_region`. Please use either one of them.
    """
    if color.startswith("not"):
        raise ValueError("Unsupported color prefix 'not', please define the color explicitly by `invert_c`.")

    rule = f'rect(R, C, "{Direction.TOP_LEFT}") :- grid(R, C), {color}(R, C), not {color}(R - 1, C), not {color}(R, C - 1).\n'
    rule += f'rect(R, C, "{Direction.LEFT}") :- grid(R, C), {color}(R, C), rect(R - 1, C, "{Direction.TOP_LEFT}"), {color}(R - 1, C), not {color}(R, C - 1).\n'
    rule += f'rect(R, C, "{Direction.LEFT}") :- grid(R, C), {color}(R, C), rect(R - 1, C, "{Direction.LEFT}"), {color}(R - 1, C), not {color}(R, C - 1).\n'
    rule += f'rect(R, C, "{Direction.TOP}") :- grid(R, C), {color}(R, C), rect(R, C - 1, "{Direction.TOP_LEFT}"), {color}(R, C - 1), not {color}(R - 1, C).\n'
    rule += f'rect(R, C, "{Direction.TOP}") :- grid(R, C), {color}(R, C), rect(R, C - 1, "{Direction.TOP}"), {color}(R, C - 1), not {color}(R - 1, C).\n'
    rule += f'rect(R, C, "{Direction.BOTTOM_RIGHT}") :- grid(R, C), rect(R, C - 1, "{Direction.LEFT}"), rect(R - 1, C, "{Direction.TOP}").\n'
    rule += f'rect(R, C, "{Direction.BOTTOM_RIGHT}") :- grid(R, C), rect(R, C - 1, "{Direction.LEFT}"), rect(R - 1, C, "{Direction.BOTTOM_RIGHT}").\n'
    rule += f'rect(R, C, "{Direction.BOTTOM_RIGHT}") :- grid(R, C), rect(R, C - 1, "{Direction.BOTTOM_RIGHT}"), rect(R - 1, C, "{Direction.TOP}").\n'
    rule += f'rect(R, C, "{Direction.BOTTOM_RIGHT}") :- grid(R, C), rect(R, C - 1, "{Direction.BOTTOM_RIGHT}"), rect(R - 1, C, "{Direction.BOTTOM_RIGHT}").\n'
    rule += f':- grid(R, C), {color}(R, C), not rect(R, C, "{Direction.TOP_LEFT}"), not rect(R, C, "{Direction.LEFT}"), not rect(R, C, "{Direction.TOP}"), not rect(R, C, "{Direction.BOTTOM_RIGHT}").\n'
    rule += f':- grid(R, C), rect(R, C, "{Direction.BOTTOM_RIGHT}"), not {color}(R, C).\n'

    if square:
        c_min = f"#min {{ C0: grid(R, C0 - 1), not {color}(R, C0), C0 > C }}"
        r_min = f"#min {{ R0: grid(R0 - 1, C), not {color}(R0, C), R0 > R }}"
        rule += f':- rect(R, C, "{Direction.TOP_LEFT}"), MR = {r_min}, MC = {c_min}, MR - R != MC - C.\n'
        rule += f':- rect(R, C, "{Direction.TOP_LEFT}"), rect(R + 1, C, "{Direction.LEFT}"), not rect(R, C + 1, "{Direction.TOP}").\n'
        rule += f':- rect(R, C, "{Direction.TOP_LEFT}"), not rect(R + 1, C, "{Direction.LEFT}"), rect(R, C + 1, "{Direction.TOP}").\n'

    return rule.strip()


def all_rect_region(square: bool = False) -> str:
    """A rule to ensure that all the shapes (recognized by edges) in the grid are rectangles.

    Args:
        square: Whether to force the rectangles to be squares.

    Success:
        This rule will generate a predicate named `rect(R, C, D)`.

    Warning:
        This rule conflicts with `all_rect`. Please use either one of them.
    """
    rule = (
        f'rect(R, C, "{Direction.TOP_LEFT}") :- grid(R, C), edge(R, C, "{Direction.LEFT}"), edge(R, C, "{Direction.TOP}").\n'
    )
    rule += f'rect(R, C, "{Direction.LEFT}") :- grid(R, C), rect(R - 1, C, "{Direction.TOP_LEFT}"), edge(R, C, "{Direction.LEFT}"), not edge(R, C, "{Direction.TOP}").\n'
    rule += f'rect(R, C, "{Direction.LEFT}") :- grid(R, C), rect(R - 1, C, "{Direction.LEFT}"), edge(R, C, "{Direction.LEFT}"), not edge(R, C, "{Direction.TOP}").\n'
    rule += f'rect(R, C, "{Direction.TOP}") :- grid(R, C), rect(R, C - 1, "{Direction.TOP_LEFT}"), edge(R, C, "{Direction.TOP}"), not edge(R, C, "{Direction.LEFT}").\n'
    rule += f'rect(R, C, "{Direction.TOP}") :- grid(R, C), rect(R, C - 1, "{Direction.TOP}"), edge(R, C, "{Direction.TOP}"), not edge(R, C, "{Direction.LEFT}").\n'
    rule += f'rect(R, C, "{Direction.BOTTOM_RIGHT}") :- grid(R, C), rect(R, C - 1, "{Direction.LEFT}"), rect(R - 1, C, "{Direction.TOP}").\n'
    rule += f'rect(R, C, "{Direction.BOTTOM_RIGHT}") :- grid(R, C), rect(R, C - 1, "{Direction.LEFT}"), rect(R - 1, C, "{Direction.BOTTOM_RIGHT}").\n'
    rule += f'rect(R, C, "{Direction.BOTTOM_RIGHT}") :- grid(R, C), rect(R, C - 1, "{Direction.BOTTOM_RIGHT}"), rect(R - 1, C, "{Direction.TOP}").\n'
    rule += f'rect(R, C, "{Direction.BOTTOM_RIGHT}") :- grid(R, C), rect(R, C - 1, "{Direction.BOTTOM_RIGHT}"), rect(R - 1, C, "{Direction.BOTTOM_RIGHT}").\n'

    rule += f':- grid(R, C), {{ rect(R, C, "{Direction.TOP_LEFT}"); rect(R, C, "{Direction.LEFT}"); rect(R, C, "{Direction.TOP}"); rect(R, C, "{Direction.BOTTOM_RIGHT}") }} != 1.\n'
    rule += f':- grid(R, C), rect(R, C, "{Direction.BOTTOM_RIGHT}"), rect(R, C + 1, "{Direction.LEFT}"), not edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), rect(R, C, "{Direction.BOTTOM_RIGHT}"), rect(R + 1, C, "{Direction.TOP}"), not edge(R + 1, C, "{Direction.TOP}").\n'
    rule += f':- grid(R, C), rect(R, C, "{Direction.BOTTOM_RIGHT}"), rect(R, C + 1, "{Direction.TOP_LEFT}"), not edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), rect(R, C, "{Direction.BOTTOM_RIGHT}"), rect(R + 1, C, "{Direction.TOP_LEFT}"), not edge(R + 1, C, "{Direction.TOP}").\n'

    rule += f':- grid(R, C), rect(R, C, "{Direction.LEFT}"), rect(R, C + 1, "{Direction.BOTTOM_RIGHT}"), edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), rect(R, C, "{Direction.BOTTOM_RIGHT}"), rect(R, C + 1, "{Direction.BOTTOM_RIGHT}"), edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), rect(R, C, "{Direction.TOP}"), rect(R + 1, C, "{Direction.BOTTOM_RIGHT}"), edge(R + 1, C, "{Direction.TOP}").\n'
    rule += f':- grid(R, C), rect(R, C, "{Direction.BOTTOM_RIGHT}"), rect(R + 1, C, "{Direction.BOTTOM_RIGHT}"), edge(R + 1, C, "{Direction.TOP}").\n'

    if square:
        c_min = f'#min {{ C0: grid(R, C0 - 1), edge(R, C0, "{Direction.LEFT}"), C0 > C }}'
        r_min = f'#min {{ R0: grid(R0 - 1, C), edge(R0, C, "{Direction.TOP}"), R0 > R }}'
        rule += f':- rect(R, C, "{Direction.TOP_LEFT}"), MR = {r_min}, MC = {c_min}, MR - R != MC - C.\n'

    return rule.strip()


def count_rect(target: Union[int, Tuple[str, int]]):
    """A rule to compare the number of rectangles in a grid with a specified target.

    * Since the top-left side of any rectangle is unique, the number of rectangles can be counted by the `rect` predicate.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
    """

    rop, num = target_encode(target)
    return f':- {{ rect(R, C, "{Direction.TOP_LEFT}") }} {rop} {num}.'


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

    * The main concept of this rule is to detect `L-shape` and ensure that all the color cells are reachable through `L-shape`.

    Args:
        color: The color to be checked.

    Success:
        This rule will generate a predicate named `reachable_Lshape_adj_4_{color}(R, C)`.
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

    * A `noqx.rule.reachable.bulb_src_color_connected` rule should be applied first.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        src_cell: The source cell of the rectangle.
        color: The color to be checked. If it is `None`, only the `edge` adjacency is accepted.
        adj_type: The type of adjacency (accepted types: `4`, `8`, `x`, `line`, `line_directed`).
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
        f'edge(R, C + 1, "{Direction.LEFT}")',
        f'edge(R + 1, C + 1, "{Direction.LEFT}")',
        f'edge(R + 1, C, "{Direction.TOP}")',
        f'edge(R + 1, C + 1, "{Direction.TOP}")',
    ]
    rule = f":- grid(R, C), {', '.join(no_rect_adjacent_by_point)}."
    return rule


def avoid_checkerboard(color: str) -> str:
    """A rule to avoid the checkerboard shape.

    Args:
        color: The color to be checked.
    """

    rule = f":- {color}(R, C), not {color}(R, C + 1), not {color}(R + 1, C), {color}(R + 1, C + 1).\n"
    rule += f":- not {color}(R, C), {color}(R, C + 1), {color}(R + 1, C), not {color}(R + 1, C + 1)."
    return rule
