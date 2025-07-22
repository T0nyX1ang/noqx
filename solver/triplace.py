"""The Tri-place solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, defined, display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, general_shape


class TriplaceSolver(Solver):
    """The Tri-place solver."""

    name = "Tri-place"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VbvT+NGEP2ev+K0X1m13rWd2Jb6IXDhfhRMOECURCgywRCDzVLHDlcj/vebWacX72a4Slf11EqVk83MG2c8b3b9dpe/10mZcuHgxw04/MLl+cFP3noMHS6DPgTa6zSr8jR6w4d1tVAlGJwfxfwmyZcp/3ixONhTw6e3w99WQTWZiHdO/cE5v9u/2/lU/Pohc0uxHwfjw/FhJm+H7/d2j/ujnf64Xp5V6eq4ELt3Z5PTm/H5bSj/GMUTr5kcOf7Hyc3Pq+HZL73puoTL3nMTRs2QN++iKZOM669gl7w5jp6bw6iJeXMCIcYFYAdgCcYlmKONea7jaO21oHDAjsF2279dgHmf3Nelav1xNG1OOcOn7Or/oskKtUpZm0D7c1VcZQhcJRX0abnIHteRZX2t7uv1vZCQFXVeZXOVqxJBxF54M2wJjAgC7oYAmi0BtGwCa4ZIYJ6V8zydHfwDFEKawgtMzicgMYumyOdsYwYb8yR6hjHWo4ieWRDITmNCGXa9QdDxhCNcw5V9w/V80zWjA89wQzNVaERFX5hut0Qhgm6NQvpGkdLM7DpGVa603E2R0I8L6IfAG1zeXX9M4F02NiAwrMTGsFgLkw6BIWUbQ942hvRsDLtnYwQPPbkW5hLcPOIZHsHNJ3rQJ7j1iVoGBN8BwXdAPCMg8ulFYWF6VdkYcR+sbAqkZl2/AlsgNe/URAlJrRqXaJlwqXXoUXV6VE6f+ru/xR0W/b6WAqnHU9AI3rh6fKtHR4++Hg/0PSM9nutxT4+eHvv6ngGqzHfoUPv2fV85sF5hqsIAXyLJJb7TQBJ+ufSgtWh7sJH6sBrcvyx96rbbsHn5/z3ssjdlo+vb9E2syiLJYR+J6+IqLTf+ySJ5TBls6Wyp8tmyLm+SeTpLPyfzikXtqaIbMbAHncuAcqUe8+yByvBnyACz2wdVpmQIwRRqfyUVhohUV6q8tmp6SvLc5KLPXAbUbtQGVJWwC3f8pCzVk4EUSbUwgM6ObWRKH6xmVolZYnKfWE8rNu146bHPTH/hvYWz4f/nr3/1+QsnyvnB6vd3xXgKHf8qnLw54uyxniUzoMbgvM8xDPpKB76K7Gvhte5uhX94D/SLpcpvqNwmaMOE1gH6DbnrRCn8FWXrRG18S8aw2G0lA5QQM0BtPQNoW9IA3FI1wF4RNsxqaxtWZcsbPmpL4fBRXZGbXva+AA==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false((puzzle.row * puzzle.col - len(puzzle.symbol)) % 3 == 0, "The grid cannot be divided into 3-ominoes!")
        sums: List[Tuple[int, List[Tuple[int, int]]]] = []
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            if label == "sudoku_1" and isinstance(num, int):
                area_points: List[Tuple[int, int]] = []
                cur = c + 1
                while cur < puzzle.col and not puzzle.symbol.get(Point(r, cur, Direction.CENTER)):
                    area_points.append((r, cur))
                    cur += 1

                fail_false(len(area_points) > 0, f"Invalid tri-place clue at ({r}, {c}).")
                sums.append((num, area_points))

            if label == "sudoku_2" and isinstance(num, int):
                area_points: List[Tuple[int, int]] = []
                cur = r + 1
                while cur < puzzle.row and not puzzle.symbol.get(Point(cur, c, Direction.CENTER)):
                    area_points.append((cur, c))
                    cur += 1

                fail_false(len(area_points) > 0, f"Invalid tri-place clue at ({r}, {c}).")
                sums.append((num, area_points))

        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_shapes("omino_3", color="grid"))

        for i, o_shape in enumerate(OMINOES[3].values()):
            self.add_program_line(general_shape("omino_3", i, o_shape, color="grid", adj_type="edge"))

        for (r, c, d, label), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            fail_false(symbol_name.startswith("kakuro"), f"Invalid symbol at ({r}, {c}).")

            if r >= 0 and c >= 0:
                self.add_program_line(f"hole({r}, {c}).")
                for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                    prefix = (
                        "not "
                        if (Point(r1, c1, d, label), symbol_name) in puzzle.symbol.items() and r1 >= 0 and c1 >= 0
                        else ""
                    )
                    direc = "left" if c1 != c else "top"
                    self.add_program_line(f"{prefix}edge_{direc}({r2}, {c2}).")

        t_be = tag_encode("belong_to_shape", "omino", 3, "grid")
        area_id = 0
        for num, coord_list in sums:
            self.add_program_line(area(_id=area_id, src_cells=coord_list))

            edge_tag = "edge_top(R + 1, C)"
            if len(coord_list) > 1 and coord_list[0][0] == coord_list[1][0]:  # the rule is in order
                edge_tag = "edge_left(R, C + 1)"

            self.add_program_line(f":- #count {{ R, C: area({area_id}, R, C), {t_be}(R, C, 0, _), {edge_tag} }} != {num}.")
            area_id += 1

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
