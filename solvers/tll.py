"""The Tapa-like Loop solver."""

import itertools
from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid, direction
from .utilsx.rule import adjacent, shade_c, fill_path
from .utilsx.loop import NON_DIRECTED, single_loop, connected_loop
from .utilsx.solution import solver

directions = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
tapa_clue_dict = {}
NON_DIRECTED_DIRS = ["lu", "ld", "ru", "rd", "lr", "ud"]


def single_shape(l, u, r, d):
    # sum should be 0 or 2
    n_edge = sum([0 if x is None else x for x in [l, u, r, d]])
    if not 0 <= n_edge <= 2:
        return None
    remain = 1 if n_edge == 1 else 0
    shape_str = "".join(map(str, [remain if x is None else x for x in [l, u, r, d]]))
    str_to_sign = {"1100": "J", "1010": "-", "1001": "7", "0110": "L", "0101": "1", "0011": "r", "0000": ""}
    return str_to_sign[shape_str]


def parse_shape_clue(inner: tuple[str], outer: tuple[str]):
    """
    Returns the shape of surroundings. Orders are in the `direction` array.
    """

    shapes = [None for _ in range(8)]
    shapes[0] = single_shape(outer[0], None, inner[0], inner[7])
    shapes[1] = single_shape(inner[0], None, inner[1], 0)
    shapes[2] = single_shape(inner[1], outer[1], None, inner[2])
    shapes[3] = single_shape(0, inner[2], None, inner[3])
    shapes[4] = single_shape(inner[4], inner[3], outer[2], None)
    shapes[5] = single_shape(inner[5], 0, inner[4], None)
    shapes[6] = single_shape(outer[3], inner[6], inner[5], None)
    shapes[7] = single_shape(None, inner[7], 0, inner[6])
    if None in shapes:
        return None, None

    if sum(inner) == 8:  # shading is all True
        return shapes, [8]

    # choose a 0 to start
    idx = 0
    if sum(inner) != 0:
        while inner[idx] == 0 or inner[(idx + 7) % 8] == 1:
            idx += 1
    clues = []
    curr_num = 0
    for i in range(idx, idx + 8):
        e, s = inner[i % 8], shapes[i % 8]
        if e:
            curr_num += 1
        else:
            if curr_num > 0:
                clues.append(curr_num + 1)
            elif s != "":  # outer loop in corner
                clues.append(1)
            curr_num = 0
    if curr_num > 0:
        clues.append(curr_num)

    if not clues:
        clues = [0]

    return shapes, sorted(clues)


def generate_patterns(pattern):
    """
    Generate patterns given numbers and "?"
    """
    result = [pattern]
    num_max = 8 - len(pattern)
    for i in range(len(pattern)):
        if pattern[i] == "?":
            old_result = result
            result = []
            for patt in old_result:
                new_patt = []
                for num in range(1, num_max + 1):
                    tmp = patt.copy()
                    tmp[i] = num
                    new_patt.append(tmp)
                result.extend(new_patt)
    result = [tuple(sorted(patt)) for patt in result if sum(patt) <= 8]
    return list(set(result))


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def tapa_rules() -> str:
    """
    Generate tapa rules and grid shapes.
    """
    valid_tapa = []
    n_clue = 0
    for inner in itertools.product([1, 0], repeat=8):
        for outer in itertools.product([1, 0], repeat=4):
            shape_clue, tapa_clue = parse_shape_clue(inner, outer)
            if shape_clue:
                shape_clue, tapa_clue = map(tuple, [shape_clue, tapa_clue])
                if tapa_clue not in tapa_clue_dict:
                    n_clue += 1
                    tapa_clue_dict[tapa_clue] = n_clue
                tapa_var = str(tapa_clue_dict[tapa_clue])
                shape_var = ", ".join(map(lambda s: f'"{s}"', shape_clue))
                valid_tapa.append(f"valid_tapa({tapa_var}, {shape_var}).")
    return "\n".join(valid_tapa)


def valid_tapa_pattern(r: int, c: int, patterns: list) -> str:
    valid_pattern, num_str, num_constrain = [], [], []
    for i, (dr, dc) in enumerate(directions):
        num_str.append(f"S{i}")
        num_constrain.append(f"loop_sign({r+dr}, {c+dc}, S{i})")
    num_str = ", ".join(num_str)
    num_constrain = ", ".join(num_constrain)
    for pattern in patterns:
        clue_str = str(tapa_clue_dict[pattern])
        rule = f"not valid_tapa({clue_str}, {num_str})"
        valid_pattern.append(rule)
    valid_pattern = ", ".join(valid_pattern)
    return f":- {valid_pattern}, {num_constrain}."


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(tapa_rules())
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(fill_path(color="not black"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(connected_loop(color="not black"))
    solver.add_program_line(single_loop(color="not black", visit_all=False))
    solver.add_program_line(f'loop_sign(R, C, "") :- -1 <= R, R <= {E.R}, -1 <= C, C <= {E.c}, not grid(R, C).')

    idx = 1
    for (r, c), clue in E.clues.items():
        patterns = generate_patterns(clue)
        solver.add_program_line(f"black({r}, {c}).")
        if idx in [1, 2, 3, 4, 5]:
            solver.add_program_line(valid_tapa_pattern(r=r, c=c, patterns=patterns))
        idx += 1

    solver.add_program_line(display(item="loop_sign", size=3))
    with open("logic_puzzles/clingo.txt", "w") as f:
        f.write(solver.program)
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
