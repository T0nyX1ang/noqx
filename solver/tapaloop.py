"""The Tapa-like Loop solver."""

import itertools
from typing import List, Optional, Tuple, Union

from .core.common import direction, display, fill_path, grid
from .core.loop import single_loop
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.solution import solver

direc = ((-1, -1, "r"), (-1, 0, "r"), (-1, 1, "d"), (0, 1, "d"), (1, 1, "l"), (1, 0, "l"), (1, -1, "u"), (0, -1, "u"))
direc_outer = ((-1, -1, "l"), (-1, 1, "u"), (1, 1, "r"), (1, -1, "d"))
tapa_clue_dict = {}
NON_DIRECTED_DIRS = ["lu", "ld", "ru", "rd", "lr", "ud"]


def single_shape(*shape_d: Optional[int]) -> Optional[str]:
    """Returns the shape of the surroundings."""
    # sum should be 0 or 2
    n_edge = sum(0 if x is None else x for x in shape_d)
    if not 0 <= n_edge <= 2:
        return None
    remain = 1 if n_edge == 1 else 0
    shape_str = "".join(map(str, [remain if x is None else x for x in shape_d]))
    str_to_sign = {"1100": "J", "1010": "-", "1001": "7", "0110": "L", "0101": "1", "0011": "r", "0000": ""}
    return str_to_sign[shape_str]


def parse_shape_clue(
    inner: Tuple[int, ...], outer: Tuple[int, ...]
) -> Tuple[Optional[List[Optional[str]]], Optional[List[int]]]:
    """Parse the shape of surroundings. Orders are in the `direction` array."""
    shapes: List[Optional[str]] = [None for _ in range(8)]
    shapes[0] = single_shape(outer[0], None, inner[0], inner[7])
    shapes[1] = single_shape(inner[0], None, inner[1], 0)
    shapes[2] = single_shape(inner[1], outer[1], None, inner[2])
    shapes[3] = single_shape(0, inner[2], None, inner[3])
    shapes[4] = single_shape(inner[4], inner[3], outer[2], None)
    shapes[5] = single_shape(inner[5], 0, inner[4], None)
    shapes[6] = single_shape(None, inner[6], inner[5], outer[3])
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


def grid_direc_to_num(r: int, c: int) -> str:
    """Convert grid direction to numbers."""
    constraint = f"grid_direc_num(R, C, D, 0) :- -1 <= R, R <= {r}, -1 <= C, C <= {c}, not grid(R, C), direction(D).\n"
    constraint += "grid_direc_num(R, C, D, 0) :- grid(R, C), direction(D), not grid_direction(R, C, D).\n"
    constraint += "grid_direc_num(R, C, D, 1) :- grid(R, C), grid_direction(R, C, D)."
    return constraint


def generate_patterns(pattern: List[Union[int, str]]) -> List[Tuple[int]]:
    """Generate patterns given numbers and '?'."""
    result = [pattern]
    num_max = 8 - len(pattern)
    for i, patt in enumerate(pattern):
        if patt == "?":
            old_result = result
            result = []
            for patt in old_result:
                new_patt: List[List[int]] = []
                for num in range(1, num_max + 1):
                    tmp = patt.copy()
                    tmp[i] = num
                    new_patt.append(tmp)  # type: ignore
                result.extend(new_patt)
    new_result: List[Tuple[int]] = [tuple(sorted(patt)) for patt in result if sum(patt) <= 8]  # type: ignore
    return list(set(new_result))


def tapa_rules() -> str:
    """Generate tapa rules and grid shapes."""
    valid_tapaloop = []
    n_clue = 0
    for inner in itertools.product([1, 0], repeat=8):
        for outer in itertools.product([1, 0], repeat=4):
            _, tapa_clue = parse_shape_clue(inner, outer)
            if tapa_clue:
                shape_clue = inner + outer
                shape_clue, tapa_clue = map(tuple, [shape_clue, tapa_clue])
                if tapa_clue not in tapa_clue_dict:
                    n_clue += 1
                    tapa_clue_dict[tapa_clue] = n_clue
                tapa_var = str(tapa_clue_dict[tapa_clue])
                shape_var = ", ".join(map(str, shape_clue))
                valid_tapaloop.append(f"valid_tapaloop({tapa_var}, {shape_var}).")
    return "\n".join(valid_tapaloop)


def valid_tapaloop_pattern(r: int, c: int, clue: List[Union[int, str]]) -> str:
    "Generate valid tapa-loop patterns."
    valid_pattern, num_str, num_constrain = [], [], []
    for i, (dr, dc, d) in enumerate(direc + direc_outer):
        num_str.append(f"E{i}")
        num_constrain.append(f'grid_direc_num({r + dr}, {c + dc}, "{d}", E{i})')
    num_str = ", ".join(num_str)
    num_constrain = ", ".join(num_constrain)

    patterns = generate_patterns(clue)
    question_mark_clue_dict = []
    if "?" in clue:
        constraint = ""
        sorted_clue = tuple(sorted(map(str, clue)))
        clue_str = f'"{"".join(sorted_clue)}"'
        if sorted_clue not in question_mark_clue_dict:
            for pattern in patterns:
                if pattern not in tapa_clue_dict:
                    continue
                clue_num = str(tapa_clue_dict[pattern])
                constraint += f"matches({clue_str}, {clue_num}).\n"
            question_mark_clue_dict.append(sorted_clue)
        matches = f"matches({clue_str}, C)"
        valid_pattern = f"valid_tapaloop(C, {num_str})"
        constraint += f":- #count{{ C: {matches}, {valid_pattern}, {num_constrain} }} != 1."
    else:
        clue_num = str(tapa_clue_dict[patterns[0]])
        valid_pattern = f"not valid_tapaloop({clue_num}, {num_str})"
        constraint = f":- {valid_pattern}, {num_constrain}."
    return constraint.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))

    if puzzle.param["visit_all"]:
        solver.add_program_line("tapaloop(R, C) :- grid(R, C), not black(R, C).")
    else:
        solver.add_program_line("{ tapaloop(R, C) } :- grid(R, C), not black(R, C).")

    solver.add_program_line(tapa_rules())
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(fill_path(color="tapaloop"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="tapaloop", adj_type="loop"))
    solver.add_program_line(single_loop(color="tapaloop"))
    solver.add_program_line(grid_direc_to_num(puzzle.row, puzzle.col))

    for (r, c), clue in puzzle.text.items():
        assert isinstance(clue, list), "Please set all NUMBER to tapa sub."
        solver.add_program_line(f"black({r}, {c}).")
        solver.add_program_line(valid_tapaloop_pattern(r, c, clue))

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
