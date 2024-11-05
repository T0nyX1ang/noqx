"""The Tapa solver."""

from typing import Dict, List, Set, Tuple, Union

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver

direc = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
pattern_ref: Dict[Tuple[int, ...], List[int]] = {}
pattern_idx: Dict[Tuple[int, ...], int] = {}


def parse_pattern(pattern: str) -> Tuple[int, ...]:
    """Parse 8-neighboring pattern to tapa clue sorted in increasing order."""
    if pattern == "11111111":
        return (8,)
    if pattern == "00000000":
        return (0,)

    idx = pattern.find("0")
    pattern = pattern[idx:] + pattern[:idx]

    result: List[int] = []
    cur = 0
    while cur < len(pattern):
        total = 0
        if pattern[cur] == "1":
            while cur < len(pattern) and pattern[cur] == "1":
                total += 1
                cur += 1
            result.append(total)
        cur += 1

    return tuple(sorted(result))


def tapa_pattern_rule() -> str:
    """Generate pattern reference dictionary and tapa pattern map."""
    for i in range(256):
        pat = bin(i)[2:].zfill(8)
        parsed = parse_pattern(pat)

        if pattern_ref.get(parsed):
            pattern_ref[parsed].append(i)
        else:
            pattern_ref[parsed] = [i]

    rule = ""
    for i, (pat, vals) in enumerate(pattern_ref.items()):
        pattern_idx[pat] = i
        for v in vals:
            rule += f"valid_tapa_map({i}, {v}).\n"

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
        rule += f"valid_tapa({r}, {c}, {num}).\n"
    return rule.strip()


def color_to_binary(r: int, c: int, color: str = "black") -> str:
    "Map the color to a binary number."
    rule = f"binary(R, C, 0) :- -1 <= R, R <= {r}, -1 <= C, C <= {c}, not grid(R, C).\n"
    rule += f"binary(R, C, 0) :- grid(R, C), not {color}(R, C).\n"
    rule += f"binary(R, C, 1) :- grid(R, C), {color}(R, C)."
    return rule


def valid_tapa(r: int, c: int) -> str:
    """Generate rules for a valid tapa clue."""
    num_seg: List[str] = []
    binary_seg: List[str] = []
    for i, (dr, dc) in enumerate(direc):
        binary_seg.append(f"{2 ** (7 - i)} * N{i}")
        num_seg.append(f"binary({r + dr}, {c + dc}, N{i})")
    rule = f":- not valid_tapa({r}, {c}, P), valid_tapa_map(P, N), {', '.join(num_seg)}, N = {' + '.join(binary_seg)}."
    return rule


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(color_to_binary(puzzle.row, puzzle.col, color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="black"))
    solver.add_program_line(tapa_pattern_rule())

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), clue in puzzle.text.items():
        assert isinstance(clue, list), "Please set all NUMBER to tapa sub."
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(parse_clue(r, c, clue))
        solver.add_program_line(valid_tapa(r, c))

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Tapa",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVda9swFH3Pryh6vg/6sBzbLyPtmr1k2UcySjGmOJlLwxKcOfEYCvnvvbryZtkJY2NQ+hCMDyfH50rnKrK1+17nVQFSgAhARcABGUQqBD1ELoR0wJtrvtqvi+QKRvX+qayQAHwYj+ExX++KQdq4ssHBxIkZgXmXpEwwYBJvwTIwn5KDeZ+YKZgZPmIQoDZxJon0tqV39NyyGycKjnyKPECO9B7pclUt18XDxCkfk9TMgdl5rqnaUrYpfxSsyWF/L8vNYmWFRb7HZnZPq23zZFd/Lb/VjVdkRzAjF3d2Jq5q41rq4lp2Jq7t4v/jrrfluaBxdjzign/GqA9JalN/aWnU0llyQJwmB6ZDW/oGUwCmw/F0ZAX8k34JEQmqFWLREwRXpPiSoCrcL54mqVBKbzahGs2XApI6paGb058hJFt3hmE/vIhPo8XUsqdI7hSvTvK4n0uqocvlS+TCHlpJn6aXmmxe2zKksfwMIXn8qmF/nWXkEnihFKfp7GvwW6FmfI8gj59SCRqpo7iGfUnp/kgBlXmNKO3W11Nca/44Ee9XRVTlr5E62WYqpuk7Sndo3MKCNvI94ZhQEs5xn4NRhG8JOaEmnJDnlvCO8IYwIAzJM7Rvyj+9Sy8QJ9X4Df7LS1+cF+efrmyQslldPebLAs+Sab1ZFNXVtKw2+ZrhsX0csJ+M7lShPbic5C9+ktvF56/tG/Ta4uBXke3zbc6ywTM=",
        },
    ],
}
