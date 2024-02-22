"""Rules and constraints to detect certain shapes."""

from typing import Tuple, Iterable, List

from .helper import tag_encode, get_variants


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

    not_color = "not_color(R, C) :- grid(R + 1, C), not grid(R, C).\n"
    not_color += "not_color(R, C) :- grid(R, C + 1), not grid(R, C).\n"
    not_color += f"not_color(R, C) :- grid(R, C), not {color}(R, C)."

    upleft = f"upleft(R, C) :- grid(R, C), {color}(R, C), not_color(R - 1, C), not_color(R, C - 1)."
    left = f"left(R, C) :- grid(R, C), {color}(R, C), upleft(R - 1, C), {color}(R - 1, C), not_color(R, C - 1).\n"
    left += f"left(R, C) :- grid(R, C), {color}(R, C), left(R - 1, C), {color}(R - 1, C), not_color(R, C - 1)."
    up = f"up(R, C) :- grid(R, C), {color}(R, C), upleft(R, C - 1), {color}(R, C - 1), not_color(R - 1, C).\n"
    up += f"up(R, C) :- grid(R, C), {color}(R, C), up(R, C - 1), {color}(R, C - 1), not_color(R - 1, C).\n"
    remain = "remain(R, C) :- grid(R, C), left(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), left(R, C - 1), remain(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), remain(R - 1, C)."

    constraint = f":- grid(R, C), {color}(R, C), not upleft(R, C), not left(R, C), not up(R, C), not remain(R, C)."
    constraint += f":- grid(R, C), remain(R, C), not {color}(R, C)."
    return not_color + "\n" + upleft + "\n" + left + "\n" + up + "\n" + remain + "\n" + constraint


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


def valid_omino(num: int = 4, color: str = "black", _type: str = "grid", distinct_variant: bool = False) -> str:
    """
    Generates a rule for a valid omino.

    A grid rule or an area rule should be defined first.
    """
    common = f"omino_{num}(T, V, DR, DC), R = AR + DR, C = AC + DC"
    tag = tag_encode("valid_omino", num, color)
    param = "T, V" if distinct_variant else "T"

    if _type == "grid":
        count_valid = f"#count {{ R, C : grid(R, C), {color}(R, C), {common} }} = {num}"
        return f"{tag}({param}, AR, AC) :- grid(AR, AC), omino_{num}(T, V, _, _), {count_valid}."

    if _type == "area":
        count_valid = f"#count {{ R, C : area(A, R, C), {color}(R, C), {common} }} = {num}"
        return f"{tag}(A, {param}, AR, AC) :- area(A, AR, AC), omino_{num}(T, V, _, _), {count_valid}."

    if _type == "edge":
        constraint = f"{{ {tag}({param}, R, C) : omino_{num}(T, V, _, _)}} 1 :- grid(R, C).\n"
        count_omino = f"#count {{ DR, DC : reachable_edge(AR, AC, R, C), {color}(R, C), {common} }}"
        constraint += (
            f":- {tag}({param}, AR, AC), grid(AR, AC), {color}(R, C), not reachable_edge(AR, AC, R, C), {common}."
        )
        constraint += f":- not {tag}({param}, AR, AC), grid(AR, AC), omino_{num}(T, V, _, _), {count_omino} = {num}."
        return constraint

    raise ValueError("Invalid type, must be one of 'grid', 'area', 'edge'.")


def general_shape(
    name: str, deltas: Iterable[Tuple[int, int]], color: str = "black", _id: int = None, adj_type: int = 4
) -> str:
    """
    Generates a rule for general shapes (using bruteforce technique).

    A grid rule and an adjacent rule should be defined first.
    """
    tag = tag_encode("shape", name, color)
    tag_belong = tag_encode("belong_to_shape", name, color)
    neighbor_type = adj_type if adj_type in [4, 8, "x"] else 4
    param = f"R, C, {_id}" if _id is not None else "R, C"
    param0 = f"R0, C0, {_id}" if _id is not None else "R0, C0"

    valid = []
    belongs_to = []
    for dr, dc in deltas:
        valid.append(f"grid(R + {dr}, C + {dc}), {color}(R + {dr}, C + {dc})")
        belongs_to.append(
            f"{tag_belong}({param}) :- R = R0 + {dr}, C = C0 + {dc}, grid(R0 + {dr}, C0 + {dc}), {tag}({param0})."
        )

        sum_adj = 0
        for nr, nc in get_neighbor(dr, dc, _type=neighbor_type):
            if (nr, nc) in deltas:
                sum_adj += 1
                if adj_type not in [4, 8, "x"] and (dr < nr or dc < nc):
                    valid.append(f"adj_{adj_type}(R + {dr}, C + {dc}, R + {nr}, C + {nc})")
        valid.append(f"#count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R + {dr}, C + {dc}, R1, C1) }} = {sum_adj}")

    return f"{tag}({param}) :- {', '.join(valid)}.\n" + "\n".join(belongs_to)


def all_same_shape(name: str, color: str = "black") -> str:
    """
    Generates a constraint to force all cells to be the same shape.

    A grid rule and a belong_to_shape rule should be defined first.
    """
    tag = tag_encode("belong_to_shape", name, color)
    return f":- grid(R, C), {color}(R, C), {{ {tag}(R, C, T) }} < 1."


def shape_omino(
    num: int,
    omino_types: List[str] = None,
    color: str = "black",
    adj_type: int = 4,
    distinct_variant: bool = False,
):
    """
    Generates a rule for a valid omino.

    A grid rule or an area rule should be defined first.
    """

    if omino_types is None:
        omino_types = list(OMINOES[num].keys())

    data, total = "", 0
    for omino_type in omino_types:
        omino_shape = OMINOES[num][omino_type]
        omino_variants = get_variants(omino_shape, allow_rotations=True, allow_reflections=True)

        for variant in omino_variants:
            if distinct_variant:
                total += 1
            data += general_shape(f"omino_{num}", variant, color, _id=total, adj_type=adj_type) + "\n"

    return data.strip()
