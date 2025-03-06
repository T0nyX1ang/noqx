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
            "data": "m=edit&p=7VbRb5s+EH7PX1H5+R4wxmB4y6/L9pLRbe1UVQhFJGVLlER0pEwTUf733hmUxPSmSf1pnTRNhMvddyb+7uNsZ/etKeoSpKSPMuABehDo0N5S+vb2+utm9bgpkwsYN4/LqkYH4CqFL8VmV46yflA+2rdx0o6hfZdkwhdgbylyaD8m+/Z90qbQXmNKgERsip4U4KM7Obm3Nk/eZQdKD/0UfdU9dofuulg3ddXFH5KsvQFBs/xnnyVXbKvvpeh+wMaLajtfETAvHrGS3XL10Gd2zX21bvqxMj9AO+7IThiy6kSW3I4seUOyfTVEdrGqF5tyNv0NdOP8cEDRPyHhWZIR988n15zc62SPNrVWJnshvTA8VoyvSMrICSPvPPS92Al93wkD6YZuNgqcMFZu6GRVqN3QIalih2TgktQuSe07rLRLUp+RREnuUBJFiILz1hKKyA4xYjzEiPYQI+5DjAoYYobBqJQBFlC1Q4yKGmJMHQEzr2bqCJlnQ+bZiMEMw88wusTMHLYphhiji/SYibF5OZCRHzuXAxkhsDEZkHt9ktMbe5MBNTdSMxLJkNFSci9CRoxy0nATmWeCYOO/tTuCb+0NbhXQKmvfWOtZq62d2jETa2+tvbQ2sDa0YyLabF6wHXUr8GV0hJYoQWzwrNEGfNIDi8Rv8A12EPnGgPII/yX1TOGhx1z670XzUSYm91/Li7Sqt8UGD5m02c7L+hRfL4uHUuDZfhiJH8Le2Ef4T+Hfcf9Hjnt6Ad4rr7L/u+gzVPe4QKG9AvHQzIrZosIGQwkpjeuYTxwX88/S/fp+ln51DXADyUdP",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false((puzzle.row * puzzle.col - len(puzzle.symbol)) % 3 == 0, "The grid cannot be divided into 3-ominoes!")
        sums: List[Tuple[int, List[Tuple[int, int]]]] = []
        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            if pos == "sudoku_1" and isinstance(num, int):
                area_points: List[Tuple[int, int]] = []
                cur = c + 1
                while cur < puzzle.col and not puzzle.symbol.get(Point(r, cur, Direction.CENTER)):
                    area_points.append((r, cur))
                    cur += 1

                fail_false(len(area_points) > 0, f"Invalid kakuro clue at ({r}, {c}).")
                sums.append((num, area_points))

            if pos == "sudoku_2" and isinstance(num, int):
                area_points: List[Tuple[int, int]] = []
                cur = r + 1
                while cur < puzzle.row and not puzzle.symbol.get(Point(cur, c, Direction.CENTER)):
                    area_points.append((cur, c))
                    cur += 1

                fail_false(len(area_points) > 0, f"Invalid kakuro clue at ({r}, {c}).")
                sums.append((num, area_points))

        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_shapes("omino_3", color="grid"))

        for i, o_shape in enumerate(OMINOES[3].values()):
            self.add_program_line(general_shape("omino_3", i, o_shape, color="grid", adj_type="edge"))

        for (r, c, d, pos), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            fail_false(symbol_name.startswith("kakuro"), f"Invalid symbol at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

            for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                prefix = "not " if (Point(r1, c1, d, pos), symbol_name) in puzzle.symbol.items() else ""
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
            self.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
