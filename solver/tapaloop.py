"""The Tapa-like Loop solver."""

from typing import Dict, List, Optional, Set, Tuple, Union

from noqx.puzzle import Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver

direc = ((-1, -1, "r"), (-1, 0, "r"), (-1, 1, "d"), (0, 1, "d"), (1, 1, "l"), (1, 0, "l"), (1, -1, "u"), (0, -1, "u"))
direc_outer = ((-1, -1, "l"), (-1, 1, "u"), (1, 1, "r"), (1, -1, "d"))
pattern_ref: Dict[Tuple[int, ...], List[int]] = {}
pattern_idx: Dict[Tuple[int, ...], int] = {}


def single_shape(*shape_d: Optional[int]) -> Optional[str]:
    """Returns the shape of the surroundings."""
    # sum should be 0 or 2
    n_edge = sum(0 if x is None else x for x in shape_d)
    if not 0 <= n_edge <= 2:
        return None
    remain = 1 if n_edge == 1 else 0
    shape_str = "".join(map(str, [remain if x is None else x for x in shape_d]))
    return shape_str


def parse_shape_clue(inner: Tuple[int, ...], outer: Tuple[int, ...]) -> Optional[Tuple[int, ...]]:
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
        return None

    if sum(inner) == 8:  # shading is all True
        return (8,)

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
            elif s != "0000":  # outer loop in corner
                clues.append(1)
            curr_num = 0

    if curr_num > 0:  # pragma: no cover
        clues.append(curr_num)  # it seems that this is never reached, but needs validation

    if not clues:
        clues = (0,)

    return tuple(sorted(clues))


def tapaloop_pattern_rule() -> str:
    """Generate pattern reference dictionary and tapaloop pattern map."""
    for i in range(4096):
        pat = bin(i)[2:].zfill(12)
        inner = tuple(map(int, pat[:8]))
        outer = tuple(map(int, pat[8:]))
        parsed = parse_shape_clue(inner, outer)

        if not parsed:
            continue

        if pattern_ref.get(parsed):
            pattern_ref[parsed].append(i)
        else:
            pattern_ref[parsed] = [i]

    rule = ""
    for i, (pat, vals) in enumerate(pattern_ref.items()):
        pattern_idx[pat] = i
        for v in vals:
            rule += f"valid_tapaloop_map({i}, {v}).\n"

    return rule.strip()


def clue_in_target(clue: List[Union[int, str]], target: List[int]) -> bool:
    """Check if clue is in target."""
    for c in clue:
        if c == "?":
            continue
        if c not in target:
            return False
        target.remove(c)

    return True


def parse_clue(r: int, c: int, clue: List[Union[int, str]]) -> str:
    """Parse tapa clue to binary pattern."""
    result: Set[int] = set()
    for pattern in filter(lambda x: len(x) == len(clue), pattern_ref.keys()):
        if clue_in_target(clue, list(pattern)):
            result.add(pattern_idx[pattern])

    rule = ""
    for num in result:
        rule += f"valid_tapaloop({r}, {c}, {num}).\n"
    return rule.strip()


def direction_to_binary(r: int, c: int) -> str:
    """Convert grid direction to numbers."""
    constraint = f"binary(R, C, D, 0) :- -1 <= R, R <= {r}, -1 <= C, C <= {c}, not grid(R, C), direction(D).\n"
    constraint += "binary(R, C, D, 0) :- grid(R, C), direction(D), not grid_direction(R, C, D).\n"
    constraint += "binary(R, C, D, 1) :- grid(R, C), grid_direction(R, C, D)."
    return constraint


def valid_tapaloop(r: int, c: int) -> str:
    """Generate rules for a valid tapa-loop clue."""
    num_seg: List[str] = []
    binary_seg: List[str] = []
    for i, (dr, dc, d) in enumerate(direc + direc_outer):
        binary_seg.append(f"{2 ** (11 - i)} * N{i}")
        num_seg.append(f'binary({r + dr}, {c + dc}, "{d}", N{i})')
    rule = f":- not valid_tapaloop({r}, {c}, P), valid_tapaloop_map(P, N), {', '.join(num_seg)}, N = {' + '.join(binary_seg)}."
    return rule


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="black"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))

    if puzzle.param["visit_all"]:
        solver.add_program_line("tapaloop(R, C) :- grid(R, C), not black(R, C).")
    else:
        solver.add_program_line("{ tapaloop(R, C) } :- grid(R, C), not black(R, C).")

    solver.add_program_line(direction("lurd"))
    solver.add_program_line(fill_path(color="tapaloop"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="tapaloop", adj_type="loop"))
    solver.add_program_line(single_loop(color="tapaloop"))
    solver.add_program_line(direction_to_binary(puzzle.row, puzzle.col))
    solver.add_program_line(tapaloop_pattern_rule())

    clue_dict: Dict[Tuple[int, int], List[Union[int, str]]] = {}
    for (r, c, d, pos), clue in puzzle.text.items():
        validate_direction(r, c, d)
        fail_false(isinstance(pos, str) and pos.startswith("tapa"), f"Clue at {r, c} should be set to 'Tapa' sub.")
        clue_dict.setdefault((r, c), [])
        clue_dict[(r, c)].append(clue)

        solver.add_program_line(f"black({r}, {c}).")
        solver.add_program_line(valid_tapaloop(r, c))

    for (r, c), clue in clue_dict.items():
        solver.add_program_line(parse_clue(r, c, clue))

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Tapa-Like Loop",
    "category": "loop",
    "aliases": ["tapalikeloop", "tapa-like-loop", "tapalike", "tapa-like", "tll"],
    "examples": [
        {
            "data": "m=edit&p=7ZRfb5swFMXf+RSVn/2AMSHEL1XWNXth7E8zVRVCFck8FYXMGQlT5Sjfvfde0+K0eZkmbZ00EZ8cfpjcYzv29kdXtZqLED8y5fANVyxSalGaUAv7a17vGq3O+LTb3ZkWDOcfZjP+rWq2Oij6XmWwtxNlp9y+UwUTjLMImmAlt5/U3r5XNuf2Ch4xLoBlrlME9nKw1/Qc3YWDIgSfg4/dazdgl3W7bPRt5shHVdg5Z1jnDb2Nlq3NT836HHi/NOtFjWBR7WAw27t60z/Zdl/Nquv7ivLA7dTFzU7ElUNctC4uuhNxcRS/Hbepv2tzfyrqpDwcYMo/Q9hbVWDuL4NNB3ul9qC52jMZ4quwKoJDPvg9OXkGEkEAB/JIIiTn5x6RL0hMkYSHxoSkT6iWT9KUinlEhFRNekQkVM0jEY0C/w5PhFL75YUb6hEZPY8t4hPIlTtC45eIkvskoZ96mkmYcEHTfkM6I41I57Aq3ErSt6Qh6Yg0oz6XpNekF6QxaUJ9xriuv7TyfyBOId0RcnyN/j1WBgXLYNOd5aZdVw3svLxbL3T7eA/H3CFg94xaIfHU/H/y/YWTD6c/fG274LXFgX3JdtWmauqVbozZsDJ4AA==",
        },
        {
            "data": "m=edit&p=7VVNb5tAEL3zK6I972E/AJu9WG4a90LpR1xFEUIRdqiMgouLTRWt5f+emQEEjemhqtRGVbTep8fbmZ3HrjXsv9dplXHp40/7XHAJw5eKpjcNaIp2LPNDkZkLPq8Pm7ICwvmHxYJ/TYt95sRtVOIcbWDsnNt3JmaScaZgSpZw+8kc7XtjI26vYYlxCVrYBCmgVz29oXVkl40oBfAIuNuk3QJd59W6yO7CRvloYrvkDOu8oWykbFv+yFjrA5/X5XaVo7BKD/Ay+02+a1f29X35ULexMjlxO2/shiN2dW8XaWMX2YhdfIs/tlvk37LyccxqkJxOcOSfweydidH3l55Oe3ptjoCROTLfw1RXo08ODmHHQKKkNVxVJ0kxpTA88E5SLkqz2WygaT2i+ZSqhtu5Eyqh5FD0RJM8kILG3aCsEl3ZQRzuc7afUuT5majH0ieU/kyj0j9J0xEpOK+hRRs3CNTy/LS0RwfdS3Alki7mlnBBqAiXcG/casK3hILQIwwp5orwhvCS0CX0KWaCN/9b/42/YCd2FTWZXw/vdf1/Xk+cmIXQzi6istqmBfS0qN6usqp7hg/IyWGPjGasIcV9/ab8g28KHr94ad3jpdmBfsYO6S4t8oesKMsdS5wn",
            "config": {"visit_all": True},
        },
        {
            "url": "https://puzz.link/p?tapaloop/17/17/g2h3h2yarhajh2x4h2haiyaihaih3xabhajh+2lyaihaih2w3h3h2y3haihabx2hajhaiyajhaihajx2hajhajy2h2h3g",
            "test": False,
        },
    ],
    "parameters": {
        "visit_all": {"name": "Visit all cells", "type": "checkbox", "default": False},
    },
}
