"""The Tapa solver."""

import itertools
from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import adjacent, connected, shade_c
from .utilsx.shape import avoid_rect
from .utilsx.solution import solver


def parse_shading(shading: List[str]):
    """
    Returns the Tapa clue that a ring of 8 cells corresponds to, digits sorted in increasing order.
    For example, shading = [T,F,T,T,T,F,F,T] should output [2, 3].
    As a special case, outputs [0] if shading is all False.
    """
    if all(shading):  # shading is all True
        return [8]

    # rotate so that the first spot is False
    idx = shading.index(False)
    shading = shading[idx:] + shading[:idx]

    # now `clue` is the lengths of consecutive runs of `True` in shading
    clue = []
    curr_num = 0
    for b in shading:
        if b:  # shaded, add to shaded string
            curr_num += 1
        else:  # unshaded, end current shaded string
            if curr_num > 0:
                clue.append(curr_num)
            curr_num = 0
    if curr_num > 0:  # add last string
        clue.append(curr_num)

    if not clue:
        clue = [0]
    return sorted(clue)


def generate_patterns(pattern):
    """
    Generate patterns given numbers and "?"
    """
    result = [pattern]
    num_max = 9 - len(pattern) * 2
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
    result = [tuple(sorted(patt)) for patt in result if sum(patt) + len(patt) <= 8]
    return list(set(result))


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def color_to_num(r: int, c: int, color: str = "black") -> str:
    num = f"num(R, C, N) :- -1 <= R, R <= {r}, -1 <= C, C <= {c}, not grid(R, C), N = 0.\n"
    num += f"num(R, C, N) :- grid(R, C), not {color}(R, C), N = 0.\n"
    num += f"num(R, C, N) :- grid(R, C), {color}(R, C), N = 1."
    return num


def tapa_rules() -> str:
    valid_tapa = []
    for shading in itertools.product([True, False], repeat=8):
        tapa_clue = parse_shading(shading)
        tapa_var = ", ".join(map(str, tapa_clue))
        shading_var = ", ".join(map(str, map(int, shading)))
        valid_tapa.append(f"valid_tapa({tapa_var}, {shading_var}).")
    return "\n".join(valid_tapa)


def valid_tapa_pattern(r: int, c: int, patterns: list, color: str = "black") -> str:
    valid_pattern, num_str, num_constrain = [], [], []
    for i, (dr, dc) in enumerate(((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))):
        num_str.append(f"N{i}")
        num_constrain.append(f"num({r+dr}, {c+dc}, N{i})")
    num_str = ", ".join(num_str)
    num_constrain = ", ".join(num_constrain)
    for pattern in patterns:
        clue_str = ", ".join(map(str, pattern))
        rule = f"not valid_tapa({clue_str}, {num_str})"
        valid_pattern.append(rule)
    valid_pattern = ", ".join(valid_pattern)
    return f":- {valid_pattern}, {num_constrain}."


def solve(E: Encoding) -> List:
    solver.reset(mode="shade")
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(color_to_num(r=E.R, c=E.C, color="black"))
    solver.add_program_line(tapa_rules())
    solver.add_program_line(adjacent())
    solver.add_program_line(connected(color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))

    for (r, c), clue in E.clues.items():
        patterns = generate_patterns(clue)
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(valid_tapa_pattern(r=r, c=c, patterns=patterns, color="black"))

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
