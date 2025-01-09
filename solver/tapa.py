"""The Tapa solver."""

from typing import Dict, List, Set, Tuple, Union

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction
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


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(color_to_binary(puzzle.row, puzzle.col, color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="black"))
    solver.add_program_line(tapa_pattern_rule())

    clue_dict: Dict[Tuple[int, int], List[Union[int, str]]] = {}
    for (r, c, d, pos), clue in puzzle.text.items():
        validate_direction(r, c, d)
        assert pos and pos.startswith("tapa"), f"Clue at {r, c} should be set to 'Tapa' sub."
        clue_dict.setdefault((r, c), [])
        clue_dict[(r, c)].append(clue)

        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(valid_tapa(r, c))

    for (r, c), clue in clue_dict.items():
        solver.add_program_line(parse_clue(r, c, clue))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")
        else:
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Tapa",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VZNj9owEL3zK1Y+zyG243xdKrpdeqFsW6hWqyhCgWa1qEGhgVSVEf99x+O0MQFVW1WiFxQxery88bwx/mD7vcnrAgQH7oOMwANEEMkAVIiYc2GD1z6z1a4skhsYNrvnqkYAcD8awVNebotB2qqywV7HiR6Cfp+kjDNgAj+cZaA/JXv9IdET0FN8xcBHbmxFAuFdBx/ovUG3luQe4gliHzHCR4TLVb0si/nYMh+TVM+AmTpvKdtAtq5+FKz1Yb4vq/ViZYhFvsNmts+rTftm23ytvjWtlmcH0ENrd3rGruzsGmjtGnTGruni3+2Wm+qc0Tg7HHDCP6PVeZIa1186GHVwmuwxTpI9U4FJfYMuAN3heCoyBP5Iv4iICNkRMe8R3JPEuBSnLFwvDicoUQinGpct51I+UUepga3pVghIdlwh7Jvn8am1mFp2GOFZxskTXtz3JWRofbkUqbCHjlKn7oUimdO2CGgs10NAGjcr7M+ziKwDx5T0qJzZBr8ZasbVcNK4LiWnkY4Y27BLSdUfyac0pxGp7Pw6jG3NHSfy+lkRZblzJE+WmYyp/BFzPDQuYU4L+ZHiiKKgOMN1DlpSfEfRo6gojklzR/GB4i1Fn2JAmtDslFfuJaYES3xgZvkJu7Eu4C1VeCC/8lFX5VX5pycbpGza1E/5ssCLZdKsF0V9M6nqdV4yvMMPA/aT0SeVKPev1/rFr3Uz+d5fXe7//3xMcV7xlNL3wDbNPJ8vq5Lhf0IwfBid8Bd3j4co2+WbnGWDFw==",
        },
        {"url": "https://puzz.link/p?tapa/10/10/i0ha0t1h2hb0t3h4h.q.h5h6ha0o.g.h7h8g.o./", "test": False},
    ],
}
