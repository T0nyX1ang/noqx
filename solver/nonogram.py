"""The Nonogram solver."""

from typing import Dict, List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect


def _expand_star(clue: Tuple[Union[int, str], ...], line_length: int) -> List[Tuple[Union[int, str], ...]]:
    """Expands the clue by replacing '*' with all possible combinations of blocks and empty cells."""
    if "*" not in clue:
        return [clue]

    def min_cells(clue: Tuple[Union[int, str], ...]) -> int:
        """Calculates the minimum number of cells required to satisfy the clue."""
        return sum(1 if token in {"?", "*"} else int(token) for token in clue) + len(clue) - 1

    max_blocks = (line_length + 1) // 2
    variants = {()}
    for token in clue:
        next_variants = set()
        if token == "*":
            for variant in variants:
                for block_count in range(max_blocks + 1):
                    next_variants.add(variant + ("?",) * block_count)
        else:
            for variant in variants:
                next_variants.add(variant + (token,))
        variants = next_variants

    return [variant for variant in sorted(variants, key=lambda item: (len(item), item)) if min_cells(variant) <= line_length]


def _line_base(_type: str, color: str) -> List[str]:
    """Generates base rule for counting consecutive shaded cells in rows or columns."""
    base = []
    if _type == "row":
        prefix = "row_count(R, C, N, V) :- grid(R, C), row_count_value_range(R, N, V)"
        base.append("row_count(R, -1, -1, 0) :- grid(R, _).")
        base.append(f"{prefix}, not {color}(R, C), row_count(R, C - 1, N, _), V = 0.")
        base.append(f"{prefix}, {color}(R, C), not {color}(R, C - 1), row_count(R, C - 1, N - 1, _), V = 1.")
        base.append(f"{prefix}, {color}(R, C), {color}(R, C - 1), row_count(R, C - 1, N, V - 1).")

    if _type == "col":
        prefix = "col_count(R, C, N, V) :- grid(R, C), col_count_value_range(C, N, V)"
        base.append("col_count(-1, C, -1, 0) :- grid(_, C).")
        base.append(f"{prefix}, not {color}(R, C), col_count(R - 1, C, N, _), V = 0.")
        base.append(f"{prefix}, {color}(R, C), not {color}(R - 1, C), col_count(R - 1, C, N - 1, _), V = 1.")
        base.append(f"{prefix}, {color}(R, C), {color}(R - 1, C), col_count(R - 1, C, N, V - 1).")

    return base


def _line_clue(
    _id: int, _type: str, clue: Tuple[Union[int, str], ...], size: int, color: str, variant: Union[int, None] = None
) -> List[str]:
    """Generates rules for a specific clue in a row or column, with optional asterisk variant handling."""
    guard = f"{_type}_variant({_id}, {variant})" if variant is not None else ""

    rule = [f"{_type}_count_value_range({_id}, -1, 0){' :- ' + guard if guard else ''}."]
    if len(clue) == 0 or clue == (0,):
        if _type == "row":
            rule.append(f":-{guard + ',' if guard else ''} grid({_id}, C), not row_count({_id}, C, -1, 0).")

        if _type == "col":
            rule.append(f":-{guard + ',' if guard else ''} grid(R, {_id}), not col_count(R, {_id}, -1, 0).")

        return rule

    if _type == "row":
        rule.append(f":-{guard + ',' if guard else ''} not row_count({_id}, {size - 1}, {len(clue) - 1}, _).")

    if _type == "col":
        rule.append(f":-{guard + ',' if guard else ''} not col_count({size - 1}, {_id}, {len(clue) - 1}, _).")

    for clue_index, token in enumerate(clue):
        if token == "?":
            upper = size + 2 - 2 * len(clue)
            rule.append(f"{_type}_count_value_range({_id}, {clue_index}, 0..{upper}){(' :- ' + guard if guard else '')}.")
            continue

        rule.append(f"{_type}_count_value_range({_id}, {clue_index}, 0..{token}){(' :- ' + guard if guard else '')}.")
        if _type == "row":
            slope = f"grid({_id}, C), {color}({_id}, C), {_type}_count({_id}, C, {clue_index}, V)"
            rule.append(f":-{guard + ',' if guard else ''} {slope}, not {color}({_id}, C + 1),  V != {token}.")

        if _type == "col":
            slope = f"grid(R, {_id}), {color}(R, {_id}), {_type}_count(R, {_id}, {clue_index}, V)"
            rule.append(f":-{guard + ',' if guard else ''} {slope}, not {color}(R + 1, {_id}), V != {token}.")

    return rule


def nonogram_rule(_type: str, size: int, clues: Dict[int, Tuple[Union[int, str], ...]], color: str = "black"):
    """Generates nonogram rule for either rows or columns."""
    validate_type(_type, ("row", "col"))
    rule = _line_base(_type, color)

    variant_name = "row_variant" if _type == "row" else "col_variant"
    option_name = f"{_type}_variant_option"

    for _id, clue in clues.items():
        variants = _expand_star(clue, size)
        if len(variants) == 1 and variants[0] == clue:
            rule.extend(_line_clue(_id, _type, clue, size, color))
            continue

        for variant_id in range(len(variants)):
            rule.append(f"{option_name}({_id}, {variant_id}).")
        rule.append(f"1 {{ {variant_name}({_id}, K): {option_name}({_id}, K) }} 1.")

        for variant_id, variant_clue in enumerate(variants):
            rule.extend(_line_clue(_id, _type, variant_clue, size, color, variant_id))

    return "\n".join(rule)


class NonogramSolver(Solver):
    """The Nonogram solver."""

    name = "Nonogram"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVNT+MwEL3nV6A5zyG2kzbJZVU+updSWNoVQlFUpSGIalMF0gatXOW/M540BAwHOAAX5Pr19dljP4896ua+Tqsch9RUgC4Kasr1uA9c8+nafLUt8ugAR/X2tqyIIJ6Nx3iTFpvciRXNoJ44Ox1GeoT6dxSDAARJXUCC+k+006eRnqKe0RCgR9qknSSJnvT0kscNO2pF4RKf7jnRK6LZqsqKfDFplfMo1nMEs88hRxsK6/Ihh70P8zsr18uVEZbplg6zuV3d7Uc29XX5r4Zuiwb1qLU76+zK3q7q7aonu+ptu/Lz7YZJ01DaL8jwIoqN9789DXo6i3aN8bUDFZjQX+SlvRtQoSV4ri2ILjmdYIf4dohvh/jSCPKZYPvw7UWH9qKBay0a2LuEwgoJ5QuBciA4E1eMY0bJOKdEoVaMx4wuo8844TknjJeMR4we44DnDE2q33kZMKCzeHRGMizbm/kCb/GgLXKBwdvfiRPDrK5u0iyn1zat18u8OpiW1TotgMq7ceA/cKeaF1TFPxX/PRVvrsD9UN1//8uPKbv0/vQZwl29SBdZWQD9aSDr4mP68LX+5aelckqcRw==",
        },
        {
            "data": "m=edit&p=7VVNT9tAEL3nV6A9VnPYD39fKkqhF5q2hAqhyEIhNSKqI1MnqSpH+e+8md1gjJDaoh44VJZ336x3Z997s7ZXPzaztqKcMnIZaTK4XKbJRRa9k1uH63yxrqvigA4369umBSD6dHJCN7N6VdFoajEFk8vRtsuL7pC6D8VUGUXK4jaqpO5Lse0+Ft2YugkeKYpKUstNvV7Mm7pplYwZzDv1Cy3gcQ8v5DmjIz9oNPA4YFJnvMUlwvmindfV1alP9rmYduek+OE7ycBQLZufFW/I/DieN8vrBQ9cz9ZQubpd3ClyeLDafGu+b8JUU+6oO/QqJn+oAkn2Khh6FYyeUWH/mYr6rnmGf17udijPGRRcFVMW87WHWQ8nxRbtuNgqZ7HUsr1cQeUcZ3ojfvuB+MlAJANvHw0kgwxRNgxzhNFDGPNq14e89nH2TGOAz2gIzSBZxmT7pzkn60Oj0yfUjGYygxE73MBY3qFnAFeMeHMp7Tnsos5J+15aLW0s7anMOYaLJoWmDGJQYPRkcshmnOdkDVgDoydrQZmxjck6kGOM99LGoME4NmSTyOMkIptCEudJM+TEHOM4KSZpTOIAADtglgQmRVoolMBpshHqKUHksAkIShAn2AUMJUhAkY2V1GmOfTxf9Ngm8NXgawJfA74u8HWgEgW+EZjEni96cAcRxil4ZOAhOdmboClPgX1O9EPPdFirsVaHvTTLDl5q5uZzovd2CAaHPeeEvQzCABDszUiwgl32AZYkWOID6Ez2NiVs097aBIoSsPUBLBgYyFolSLlogUCKZKk/FOgfiokeOJiJwtrUC0cPo4JwfKItn37BEMIVEgwdYiZO3oWcvyNpI2kTOZcpv+R/9Rl42bH/LYUpjgG/a/5CiV+Ky9FUTTbtzWxe4Us43iyvq/Zg3LTLWa3wP9qN1C8lN74t+K/9/0W98l8Ul0q/hhP6GijgPSlH9w==",
            "config": {"cts": True},
        },
        {
            "url": "https://puzz.link/p?nonogram/30/30/1121222n1331112n3111223n34133p8115q64113p5412312n411232o311323o21215p2112113n41243p32124p231112o2222q32121p22222p3225q52215p41524p4524q4221q422121o354r3132q51121p56sct43s1t411r422r4112q14211p19112p4811q22ar223711o5325q41113p334r2171q13333p15br2123111n222111o6272q431113o32111111m33112p2211111n122112o23711p733r74s77s3425q75sbt7t",
            "test": False,
        },
    ]
    parameters = {"cts": {"name": "Cross the Streams", "type": "checkbox", "default": False}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))

        if puzzle.param["cts"]:
            self.add_program_line(adjacent())
            self.add_program_line(avoid_rect(2, 2, color="black"))
            self.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))

        top_clues = {}
        for c in range(puzzle.col):
            r1 = -1
            clue: List[Union[int, str]] = []
            while (r1, c, Direction.CENTER, "normal") in puzzle.text:
                clue.append(puzzle.text[Point(r1, c, Direction.CENTER, "normal")])
                r1 -= 1

            if (puzzle.param["cts"] and clue) or not puzzle.param["cts"]:
                top_clues[c] = tuple(reversed(clue))

        left_clues = {}
        for r in range(puzzle.row):
            c1 = -1
            clue: List[Union[int, str]] = []
            while (r, c1, Direction.CENTER, "normal") in puzzle.text:
                clue.append(puzzle.text[Point(r, c1, Direction.CENTER, "normal")])
                c1 -= 1

            if (puzzle.param["cts"] and clue) or not puzzle.param["cts"]:
                left_clues[r] = tuple(reversed(clue))

        self.add_program_line(nonogram_rule(_type="row", size=puzzle.col, clues=left_clues))
        self.add_program_line(nonogram_rule(_type="col", size=puzzle.row, clues=top_clues))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
