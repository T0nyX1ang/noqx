"""The Pigpen Park solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import adjacent, shade_c, count_shape, count
from .utilsx.shape import all_shapes, general_shape
from .utilsx.solution import solver
from .utilsx.helper import tag_encode, ConnectivityHelper, get_variants

PIGPEN_SHAPES = {
    "0": ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)),
    "1": ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)),
    "2": ((0, 0), (0, 1), (0, 2), (1, 0), (2, 0)),
    "3": ((0, 0), (0, 1), (1, 1), (0, 2)),
    "4": ((0, 0), (1, 1), (0, 2)),
    "5": ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)),
    "6": ((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)),
    "7": ((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)),
}

word_list = {
    "a": [2, 2],
    "b": [6, 0],
    "c": [2, 0],
    "d": [6, 3],
    "e": [7, 0],
    "f": [6, 2],
    "g": [2, 1],
    "h": [6, 1],
    "i": [2, 3],
    "j": [1, 1],
    "k": [5, 3],
    "l": [1, 0],
    "m": [5, 0],
    "n": [0, 0],
    "o": [5, 2],
    "p": [1, 2],
    "q": [5, 1],
    "r": [1, 3],
    "s": [4, 1],
    "t": [4, 0],
    "u": [4, 2],
    "v": [4, 3],
    "w": [3, 3],
    "x": [3, 1],
    "y": [3, 0],
    "z": [3, 2],
}


def special_connected(color: str = "black", adj_type: int = 4, _type: str = "grid") -> str:
    """
    Generate a constraint to check the reachability of {color} cells.

    An adjacent rule, a grid fact and a shape rule should be defined first.
    """
    not_color = f"not {color}".replace("not not ", "")
    tag = tag_encode("shape", "pigpen", not_color)
    helper = ConnectivityHelper("reachable", _type, color, adj_type)
    initial = helper.initial()
    propagation = helper.propagation()
    constraint = helper.constraint()
    constraint = constraint.replace(".", f", not {tag}(R - 1, C - 1, 7, 0).")  # special judge for "E"
    return initial + "\n" + propagation + "\n" + constraint


def special_stuv_case(color: str = "black") -> str:
    """
    Generate a constraint to deal with the overlapping of the S, T, U, V case.

    A grid fact and a shape rule should be defined first.
    """
    tag = tag_encode("shape", "pigpen", color)
    tag_stuv = tag_encode("shape", "pigpen_stuv", color)
    tag_be = tag_encode("belong_to_shape", "pigpen", "black")
    tag_be_stuv = tag_encode("belong_to_shape", "pigpen_stuv", "black")

    data = f"{{ {tag_stuv}(R, C, 4, V) }} :- {tag}(R, C, 4, V).\n"
    variants = get_variants(PIGPEN_SHAPES["4"], allow_rotations=True, allow_reflections=True)
    for i, variant in enumerate(variants):
        for dr, dc in variant:
            data += f"{tag_be_stuv}(R + {dr}, C + {dc}, R, C, {i}) :- grid(R + {dr}, C + {dc}), {tag_stuv}(R, C, 4, {i}).\n"

    data += f":- {tag_be_stuv}(R, C, R0, C0, V), {tag_be_stuv}(R, C, R1, C1, V1), |R0 - R1| + |C0 - C1| + |V - V1| > 0.\n"
    # data += f":- grid(R, C), {color}(R, C), {tag_be}(R, C, 4, _), not {tag_be_stuv}(R, C, _, _, _).\n"

    return data.strip()


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(special_connected(color="not black"))

    solver.add_program_line(all_shapes("pigpen", color="black"))
    for i, p_shape in enumerate(PIGPEN_SHAPES.values()):
        solver.add_program_line(general_shape("pigpen", i, p_shape, color="black", adj_type=4))

    target_word = E.params["word"].lower()
    word_count = {s: 0 for s in word_list}
    for s in target_word:
        word_count[s] += 1

    solver.add_program_line(special_stuv_case(color="black"))
    for s, cnt in word_count.items():
        _id, vid = word_list[s]
        if s in "stuv":
            solver.add_program_line(count_shape(cnt, name="pigpen_stuv", _id=_id, variant_id=vid, color="black"))
        else:
            solver.add_program_line(count_shape(cnt, name="pigpen", _id=_id, variant_id=vid, color="black"))

    # total_count = sum(cnt * len(PIGPEN_SHAPES[str(word_list[s][0])]) for s, cnt in word_count.items())
    # solver.add_program_line(count(total_count, color="black"))

    for (r, c), clue in E.clues.items():
        if clue == "b":
            solver.add_program_line(f"black({r}, {c}).")
        elif clue == "w":
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
