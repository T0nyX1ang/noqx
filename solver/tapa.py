"""The Tapa solver."""

from typing import Dict, List, Set, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect

direc = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
pattern_ref = "())*)+*,)++-*-,.)++-+/-0*--1,0.2)++-+/-0+//3-304*--1-315,005.426)++-+/-0+//3-304+//3/738-339084:*--1-315-339195;,005085<.44;2:6=)*+,+--.+-/0-102+-/0/334-1350546+-/0/334/378398:-135399;058<4;:=*,-.-012-0341556-034389:159;5<;=,.020456048:5;<=.2464:;=26:=6==>"  # fmt: skip  # formula: chr(pattern_idx.value()) + 40 (invalid patterns are "!")

pattern_idx: Dict[Tuple[int, ...], int] = {(0,): 0, (1,): 1, (2,): 2, (1, 1): 3, (3,): 4, (1, 2): 5, (4,): 6, (1, 1, 1): 7, (1, 3): 8, (2, 2): 9, (5,): 10, (1, 1, 2): 11, (1, 4): 12, (2, 3): 13, (6,): 14, (1, 1, 1, 1): 15, (1, 1, 3): 16, (1, 2, 2): 17, (1, 5): 18, (2, 4): 19, (3, 3): 20, (7,): 21, (8,): 22}  # fmt: skip


def tapa_pattern_rule() -> str:
    """Generate pattern reference dictionary and tapa pattern map."""
    return "\n".join(f"valid_tapa_map({ord(pattern_ref[v]) - 40}, {v})." for v in range(256) if pattern_ref[v] != "!")


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
    for pattern in filter(lambda x: len(x) == len(clue), pattern_idx.keys()):
        if clue_in_target(clue, list(pattern)):
            result.add(pattern_idx[pattern])

    return "\n".join(f"valid_tapa({r}, {c}, {num})." for num in result)


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


class TapaSolver(Solver):
    """The Tapa solver."""

    name = "Tapa"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZZNi9swEIbv+RWLznOwNJa/LiXdbnpJs22TsizGBG/qZUMdnDpxKQ757x2NvbVXDmULJb0E4+HN65H0WBlJ3n2v0jIDJUG6gAE4QAoC9ED7pKVUTXDaa7He51l0BeNq/1SUJABuJxN4TPNdNorbrGR0qMOoHkP9PoqFFCAU3VIkUH+KDvWHqJ5BPadHAlzypk2SInnTyTt+btR1Y0qH9Iy0S5rkPcnVulzl2XLaOB+juF6AMOO85dZGik3xIxMth/m9KjYPa2M8pHt6md3Tets+2VVfi29VmyuTI9TjBnd+Ahc7XPyNi6dx1T/BzbfFKdAwOR5pwj8T6jKKDfWXTgadnEeHoyE6CO2Zpm+IAoiO+tOBMVRnBGxgZ4TSMqSD7PQtya2oXnqe4oZK9UaT2Hp9y2XrRVNPDkbw3OEIvg0vwyFa6Fn8ymkc1bdCm0uh33D1Lc7CvqWH9EqH1iQrz7cZvPC52J4d355nFfg2FDo8nNt3PGsOULo2JUrfGg1laL8dorZ7cn3rRVCjBYneoOvAsVsF2Px3fcsuMwz1wHnZNZWw5EK+5zjhqDguqM6hRo7vODocNccp59xwvON4zdHl6HGOb1bKK9eS0EpELghTfqpZWGdgi7XiHfo1l75kXjL/dCWjWMyr8jFdZXSwzKrNQ1ZezYpyk+aCzvDjSPwUfMdI6e7lWD/7sW4m3/mrw/3/748xzSvtUvUtiG21TJerIhf0TQjG94OBf3Z62kST0S8=",
        },
        {"url": "https://puzz.link/p?tapa/10/10/i0ha0t1h2hb0t3h4h.q.h5h6ha0o.g.h7h8g.o./", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(color_to_binary(puzzle.row, puzzle.col, color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="black"))
        self.add_program_line(tapa_pattern_rule())

        clue_dict: Dict[Tuple[int, int], List[Union[int, str]]] = {}
        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            fail_false(isinstance(label, str) and label.startswith("tapa"), f"Clue at {r, c} should be set to 'Tapa' sub.")

            if (r, c) not in clue_dict:
                self.add_program_line(f"not black({r}, {c}).")
                self.add_program_line(valid_tapa(r, c))
                clue_dict.setdefault((r, c), [])

            clue_dict[(r, c)].append(clue)

        for (r, c), clue in clue_dict.items():
            self.add_program_line(parse_clue(r, c, clue))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
