"""Rules and constraints to detect certain shapes."""

from typing import Iterable, Tuple

from .helper import get_variants, tag_encode

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


def get_neighbor(r: int, c: int, _type: int = 4) -> Tuple[Tuple[int, int]]:
    """Get the neighbors of a cell."""
    shape_4 = ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))
    shape_x = ((r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1))

    if _type == 4:
        return shape_4

    if _type == "x":
        return shape_x

    if _type == 8:
        return shape_4 + shape_x

    raise ValueError("Invalid type, must be one of 4, 8, 'x'.")


def all_rect(color: str = "black") -> str:
    """
    Generate a constraint to force rectangles.

    A grid rule should be defined first.
    """
    upleft = f"upleft(R, C) :- grid(R, C), {color}(R, C), not {color}(R - 1, C), not {color}(R, C - 1)."
    left = f"left(R, C) :- grid(R, C), {color}(R, C), upleft(R - 1, C), {color}(R - 1, C), not {color}(R, C - 1).\n"
    left += f"left(R, C) :- grid(R, C), {color}(R, C), left(R - 1, C), {color}(R - 1, C), not {color}(R, C - 1)."
    up = f"up(R, C) :- grid(R, C), {color}(R, C), upleft(R, C - 1), {color}(R, C - 1), not {color}(R - 1, C).\n"
    up += f"up(R, C) :- grid(R, C), {color}(R, C), up(R, C - 1), {color}(R, C - 1), not {color}(R - 1, C).\n"
    remain = "remain(R, C) :- grid(R, C), left(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), left(R, C - 1), remain(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), remain(R - 1, C)."

    constraint = f":- grid(R, C), {color}(R, C), not upleft(R, C), not left(R, C), not up(R, C), not remain(R, C).\n"
    constraint += f":- grid(R, C), remain(R, C), not {color}(R, C)."

    data = upleft + "\n" + left + "\n" + up + "\n" + remain + "\n" + constraint
    return data.replace("not not ", "")


def all_rect_region() -> str:
    """
    Generate a constraint to force rectangles.

    A grid rule and an edge rule should be defined first.
    """
    upleft = "upleft(R, C) :- grid(R, C), vertical_line(R, C), horizontal_line(R, C)."
    left = "left(R, C) :- grid(R, C), upleft(R - 1, C), vertical_line(R, C), not horizontal_line(R, C).\n"
    left += "left(R, C) :- grid(R, C), left(R - 1, C), vertical_line(R, C), not horizontal_line(R, C)."
    up = "up(R, C) :- grid(R, C), upleft(R, C - 1), horizontal_line(R, C), not vertical_line(R, C).\n"
    up += "up(R, C) :- grid(R, C), up(R, C - 1), horizontal_line(R, C), not vertical_line(R, C).\n"
    remain = "remain(R, C) :- grid(R, C), left(R, C - 1), up(R - 1, C), not vertical_line(R, C), not horizontal_line(R, C).\n"
    remain += (
        "remain(R, C) :- grid(R, C), left(R, C - 1), remain(R - 1, C), not vertical_line(R, C), not horizontal_line(R, C).\n"
    )
    remain += (
        "remain(R, C) :- grid(R, C), remain(R, C - 1), up(R - 1, C), not vertical_line(R, C), not horizontal_line(R, C).\n"
    )
    remain += (
        "remain(R, C) :- grid(R, C), remain(R, C - 1), remain(R - 1, C), not vertical_line(R, C), not horizontal_line(R, C)."
    )
    constraint = ":- grid(R, C), not upleft(R, C), not left(R, C), not up(R, C), not remain(R, C).\n"
    constraint += ":- grid(R, C), remain(R, C), left(R, C + 1), not vertical_line(R, C + 1).\n"
    constraint += ":- grid(R, C), remain(R, C), up(R + 1, C), not horizontal_line(R + 1, C).\n"
    constraint += ":- grid(R, C), remain(R, C), upleft(R, C + 1), not vertical_line(R, C + 1).\n"
    constraint += ":- grid(R, C), remain(R, C), upleft(R + 1, C), not horizontal_line(R + 1, C)."

    c_min = "#min { C0: vertical_line(R, C0), C0 > C }"
    r_min = "#min { R0: horizontal_line(R0, C), R0 > R }"
    rect = f"rect(R, C, MR - 1, MC - 1) :- upleft(R, C), {c_min} = MC, {r_min} = MR.\n"
    rect += ":- rect(R, C, MR, MC), vertical_line(R..MR, C + 1..MC).\n"
    rect += ":- rect(R, C, MR, MC), horizontal_line(R + 1..MR, C..MC)."

    data = upleft + "\n" + left + "\n" + up + "\n" + remain + "\n" + constraint + "\n" + rect
    return data.replace("not not ", "")


def avoid_rect(rect_r: int, rect_c: int, corner: Tuple[int, int] = (None, None), color: str = "black") -> str:
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


def general_shape(
    name: str,
    _id: int = 0,
    deltas: Iterable[Tuple[int, int]] = None,
    color: str = "black",
    _type: str = "grid",
    adj_type: int = 4,
    simple: bool = False,
) -> str:
    """
    Generates a rule for general shapes (using bruteforce technique).
    The deltas are the relative coordinates of the shape cells.

    A grid rule and an adjacent rule should be defined first.
    """

    if not deltas:
        raise ValueError("Shape coordinates must be provided.")

    tag = tag_encode("shape", name, color)
    tag_be = tag_encode("belong_to_shape", name, color)
    neighbor_type = adj_type if adj_type in [4, 8, "x"] else 4
    data = ""

    variants = get_variants(deltas, allow_rotations=True, allow_reflections=True)
    for i, variant in enumerate(variants):
        valid, belongs_to = [], []
        for dr, dc in variant:
            if _type == "grid":
                valid.append(f"grid(R + {dr}, C + {dc}), {color}(R + {dr}, C + {dc})")
                belongs_to.append(
                    f"{tag_be}(R + {dr}, C + {dc}, {_id}, {i}) :- grid(R + {dr}, C + {dc}), {tag}(R, C, {_id}, {i})."
                )
            elif _type == "area":
                valid.append(f"area(A, R + {dr}, C + {dc}), {color}(R + {dr}, C + {dc})")
                belongs_to.append(
                    f"{tag_be}(A, R + {dr}, C + {dc}, {_id}, {i}) :- area(A, R + {dr}, C + {dc}), {tag}(A, R, C, {_id}, {i})."
                )

            sum_adj = 0
            for nr, nc in get_neighbor(dr, dc, _type=neighbor_type):
                if (nr, nc) in variant:
                    sum_adj += 1
                    if adj_type not in [4, 8, "x"] and (dr, dc) < (nr, nc):
                        valid.append(f"adj_{adj_type}(R + {dr}, C + {dc}, R + {nr}, C + {nc})")

            if simple:
                continue  # Skip the adjacency re-check if it is simple

            if _type == "grid":
                valid.append(f" {{ {color}(R1, C1): adj_{adj_type}(R + {dr}, C + {dc}, R1, C1) }} = {sum_adj}")
            elif _type == "area":
                valid.append(
                    f" {{ {color}(R1, C1): area(A, R1, C1), adj_{adj_type}(R + {dr}, C + {dc}, R1, C1) }} = {sum_adj}"
                )

        if _type == "grid":
            data += f"{tag}(R, C, {_id}, {i}) :- grid(R, C), {', '.join(valid)}.\n" + "\n".join(belongs_to)
        elif _type == "area":
            data += f"{tag}(A, R, C, {_id}, {i}) :- area(A, R, C), {', '.join(valid)}.\n" + "\n".join(belongs_to)

    return data.strip()


def all_shapes(name: str, color: str = "black", _type: str = "grid") -> str:
    """
    Generate a constraint to force all {color} cells are in defined shapes.

    A grid rule and a shape/belong_to_shape rule should be defined first.
    """

    tag = tag_encode("belong_to_shape", name, color)
    if _type == "grid":
        return f":- grid(R, C), {color}(R, C), not {tag}(R, C, _, _)."

    if _type == "area":
        return f":- area(A, R, C), {color}(R, C), not {tag}(A, R, C, _, _)."

    raise ValueError("Invalid type, must be one of 'grid', 'area'.")
