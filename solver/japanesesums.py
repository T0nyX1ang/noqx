"""The Japanese Sums solver."""

from typing import Dict, List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, fill_num, grid, shade_c, unique_num
from noqx.rule.helper import fail_false, validate_direction, validate_type


def _line_base(_type: str, color: str) -> List[str]:
    """Generates base rule for counting sums in rows or columns."""
    base = []
    if _type == "row":
        prefix = "row_count(R, C, N, V) :- grid(R, C), row_count_value_range(R, N, V)"
        base.append("row_count(R, -1, -1, 0) :- grid(R, _).")
        base.append(f"{prefix}, {color}(R, C), row_count(R, C - 1, N, _), V = 0.")
        base.append(f"{prefix}, not {color}(R, C), {color}(R, C - 1), row_count(R, C - 1, N - 1, _), number(R, C, V).")
        base.append(f"{prefix}, not {color}(R, C), not grid(R, C - 1), row_count(R, C - 1, N - 1, _), number(R, C, V).")
        base.append(
            f"{prefix}, not {color}(R, C), not {color}(R, C - 1), grid(R, C - 1), row_count(R, C - 1, N, V0), number(R, C, N0), V = V0 + N0."
        )

    if _type == "col":
        prefix = "col_count(R, C, N, V) :- grid(R, C), col_count_value_range(C, N, V)"
        base.append("col_count(-1, C, -1, 0) :- grid(_, C).")
        base.append(f"{prefix}, {color}(R, C), col_count(R - 1, C, N, _), V = 0.")
        base.append(f"{prefix}, not {color}(R, C), {color}(R - 1, C), col_count(R - 1, C, N - 1, _), number(R, C, V).")
        base.append(f"{prefix}, not {color}(R, C), not grid(R - 1, C), col_count(R - 1, C, N - 1, _), number(R, C, V).")
        base.append(
            f"{prefix}, not {color}(R, C), not {color}(R - 1, C), grid(R - 1, C), col_count(R - 1, C, N, V0), number(R, C, N0), V = V0 + N0."
        )

    return base


def _line_clue(_id: int, _type: str, clue: Tuple[Union[int, str], ...], size: int, max_num: int, color: str) -> List[str]:
    """Generates rules for a specific clue in a row or column."""
    rule = [f"{_type}_count_value_range({_id}, -1, 0)."]
    if len(clue) == 1 and clue[0] == 0:
        if _type == "row":
            rule.append(f":- grid({_id}, C), not row_count({_id}, C, -1, 0).")
        if _type == "col":
            rule.append(f":- grid(R, {_id}), not col_count(R, {_id}, -1, 0).")
        return rule

    if _type == "row":
        rule.append(f":- not row_count({_id}, {size - 1}, {len(clue) - 1}, _).")
    if _type == "col":
        rule.append(f":- not col_count({size - 1}, {_id}, {len(clue) - 1}, _).")

    for clue_index, token in enumerate(clue):
        if token == "?":
            sum_max = (
                sum(range(max_num, max_num - (size - 2 * len(clue) + 1), -1))
                if max_num >= size - 2 * len(clue) + 1
                else sum(range(1, max_num + 1))
            )
            rule.append(f"{_type}_count_value_range({_id}, {clue_index}, 0..{sum_max}).")
            continue

        rule.append(f"{_type}_count_value_range({_id}, {clue_index}, 0..{token}).")
        if _type == "row":
            slope = f"grid({_id}, C), not {color}({_id}, C), {_type}_count({_id}, C, {clue_index}, V)"
            rule.append(f":- {slope}, {color}({_id}, C + 1), V != {token}.")
            rule.append(f":- {slope}, not grid({_id}, C + 1), V != {token}.")

        if _type == "col":
            slope = f"grid(R, {_id}), not {color}(R, {_id}), {_type}_count(R, {_id}, {clue_index}, V)"
            rule.append(f":- {slope}, {color}(R + 1, {_id}), V != {token}.")
            rule.append(f":- {slope}, not grid(R + 1, {_id}), V != {token}.")

    return rule


def japsum_rule(_type: str, size: int, clues: Dict[int, Tuple[Union[int, str], ...]], max_num: int, color: str = "black"):
    """Generates Japanese sums rule for either rows or columns."""
    validate_type(_type, ("row", "col"))
    rule = _line_base(_type, color)

    for _id, clue in clues.items():
        rule.extend(_line_clue(_id, _type, clue, size, max_num, color))

    return "\n".join(rule)


class JapaneseSumsSolver(Solver):
    """The Japanese Sums solver."""

    name = "Japanese Sums"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VRNb5tAEL3zK6I9z4Fl+b65adyLS9riKooQsjAlCiqIFJuqWsv/PTMDqSklVVKpaQ/Vap+e374dz8wuu/vSZW0BPg7lgwkSh7ItnpYZ8DSHsS73VRGewaLb3zYtEoDL5RJusmpXgJFYaMGZGgcdhHoB+k2YCClAWDilSEG/Dw/6bagj0DEuCbBTEHVX7cu8qZpWsCbRt+o3WkgvTvSK14md96I0kUcDR3qNNC/bvCo2q155FyZ6DYL++xXvJirq5mtBf0a50e+8qbclCdtsjxXubss7AQoXdt2n5nM3WGV6BL3oK4ifWAEGeaiAaF8BsZkKqLA/W0GQHo94OB+whk2YUDkfT9Q/0Tg8IEbhQShJWxWm0p+gsFmgzB8EiwR3JKipw546HBLMk+BMg7oc1BkJHHQkeBxjtMV3SbBHgjdJPfCnQjARpOREvmeGTZDcimvGJaPFuMZOgVaMrxlNRodxxZ4LxivGc0ab0WWPR71+4mkIB+u3hzNxuDl0YV4qycSx+F3oh/f7PDUSEXftTZYXeHGjrt4W7VnUtHVWCXw2job4JngmCqtD+/+X5B9+SeigzGe9J3//g0qw4bYEfQnirttkG2w2d2dWxz4meMVQH31vYwP2fDD8uHHQ8bP51cYYXHs+E0fNZTLjf0zHA5vV8ZKR7rkT3XlEf278wf9TnME/E//F7wc+Z6lxDw==",
            "config": {"max_number": 4},
        },
        {
            "data": "m=edit&p=7ZVRb5swEMff8ykqP98DxkAcXqasa/aS0W3JVFUIRYRRFY2IjoRpcpTv3rsDGo9k2iZtVR8mwuXy42z/z2cu269NWucgHfooDfiNlyc1364O+Ha6a1nsyjy8gGmzu69qdACuZzO4S8ttDqNYYQjeyWhvJqGZgnkbxkIKEC7eUiRgPoR78y40EZgFPhLgJSA2TbkrsqqsasFMYty8Heiie3V0b/g5eZctlA76Ueeje4tuVtRZma/mLXkfxmYJgtZ+zaPJFZvqW06LkTb6nVWbdUFgne4ww+198SBA4YNt87n60nShMjmAmbYZLH4zA5ykz4DcNgPyzmRAif3bDCbJ4YDF+Yg5rMKY0vl0dPXRXYR7tFG4F0rRUB+ltBUUyiPwygIBAXUE3rjfrx5oBjaZDMb4DoHAAnIwie8OIgKOsJQFHGEpC1i7tUrA2scW8Ang6XwCnIw9aZuMRcY8q2eB4Y5oHmNJ1bwB1jLSYfHWGOmweulYSPLE1jwSdQwJC7aJN8xaejyPTfy2Ik+KsNiSS37LdsbWZbvEEwFGsX3D1mHrs51zzBXbG7aXbD22AceM6Uz90al7Bjnx2OdO11/67/9KRrFYNPVdmuX4kkbNZp3XF1FVb9JSYIs8jMR3wTf2TZfC/3fNF9w1qVDOSzvFv5AT45FRCrjRuN27/9Cs0hXuusD/aegCzPUJXwC+ID9y3OizHPeL5kHObfEnC+HAYDAQ60Rc6/MLnXBeCPlkwPEwdQLOJBKdxnd6Tnif4FCnSp69rtigktEj",
            "config": {"max_number": 6},
        },
    ]
    parameters = {"max_number": {"name": "Max number", "type": "number", "default": 5}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        max_num = int(puzzle.param["max_number"])
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(fill_num(_range=range(1, max_num + 1), color="black"))
        self.add_program_line(unique_num(_type="row", color="not black"))
        self.add_program_line(unique_num(_type="col", color="not black"))

        top_clues = {}
        for c in range(puzzle.col):
            r1 = -1
            clue: List[Union[int, str]] = []
            while (r1, c, Direction.CENTER, "normal") in puzzle.text:
                clue.append(puzzle.text[Point(r1, c, Direction.CENTER, "normal")])
                r1 -= 1
            if len(clue) > 0:
                top_clues[c] = tuple(reversed(clue))

        left_clues = {}
        for r in range(puzzle.row):
            c1 = -1
            clue: List[Union[int, str]] = []
            while (r, c1, Direction.CENTER, "normal") in puzzle.text:
                clue.append(puzzle.text[Point(r, c1, Direction.CENTER, "normal")])
                c1 -= 1
            if len(clue) > 0:
                left_clues[r] = tuple(reversed(clue))

        self.add_program_line(japsum_rule(_type="row", size=puzzle.col, clues=left_clues, max_num=max_num))
        self.add_program_line(japsum_rule(_type="col", size=puzzle.row, clues=top_clues, max_num=max_num))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"black({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            if 0 <= r < puzzle.row and 0 <= c < puzzle.col:
                validate_direction(r, c, d)
                validate_type(label, "normal")
                fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be an integer.")
                self.add_program_line(f"number({r}, {c}, {num}).")
                self.add_program_line(f"not black({r}, {c}).")

        self.add_program_line(display(item="black", size=2))
        self.add_program_line(display(item="number", size=3))

        return self.program
