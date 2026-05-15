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
            "data": "m=edit&p=7Vbdj9JAEH/nr7js88R0P9pu+4Yn+oKcCpeLaQgpXBVCSbFQY0r4353dNrQrY0zOeNHELB3mY3c7v/nY7eFLlZYZcM/8pAb8x6F8/UK1NPJA6AANzZhtjnkW38CwOq6LEhmAuwl8SvNDBoOknTUfnOoorodQv4kTJhjYh7M51O/jU/02ridQT9HEgKNujBxnIJAddeyDtRvutlFyD/kJ8rJZ9hHZbbqtyqKR38VJPQNm3vLSrjUs2xVfM9ZsYOVVsVtujGKZHhHKYb3Zt5ZD9Vhsq3YuN0ur/LhZFXlRstbXM9TDBsCIACA7APICQBIAWoQGwGpTrvJsMf4DECIawhmT8wFBLOLE4LnvWN2x0/h0Nr4ayuMT01r0AhOJqC+Fuidxj0tHFIEjKt8VXWuoHDFyt4ocKw+4KwpH1H0fufAdJ4W7s/Qcr6T4QeycPJu0nRg3EyT064/xgNCFhE4TuuhaJzxCxwmdIHSS0ClCR+AQhC+SwKaIdygCm0/EICCwBYQvIYE3JPCGxDs0sZ8msEVEXCJiHlY2paSyzonQcDLvVKK4oKpGEiHjkqpDRfmpqD19arl/hR2L/rU9CoSlMzwjoJaWvrLUs9S3dGznjCx9sPTWUmVpYOeE5pR5wjnUdN/T3MF6xVRF2jSRAGF6WprmCUAor+EV3nU+VoP8peuJbG5Kd/j/nm4+SNjo8XN2MynKXZrjPTKpdsus7OTpOt1nDK/084B9Y/bB6sCPhP+3/F99y5tEec/cY7/b8glG/NKeUN8B21eLdIHQGH5VgjFjF9OGSyv/zNx295X52WOAx8d88B0=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false((puzzle.row * puzzle.col - len(puzzle.symbol)) % 3 == 0, "The grid cannot be divided into 3-ominoes!")
        sums: List[Tuple[int, List[Tuple[int, int]]]] = []
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            if label == f"corner_{Direction.TOP_RIGHT}" and isinstance(num, int):
                area_points: List[Tuple[int, int]] = []
                cur = c + 1
                while cur < puzzle.col and not puzzle.symbol.get(Point(r, cur, Direction.CENTER)):
                    area_points.append((r, cur))
                    cur += 1

                fail_false(len(area_points) > 0, f"Invalid tri-place clue at ({r}, {c}).")
                sums.append((num, area_points))

            if label == f"corner_{Direction.BOTTOM_LEFT}" and isinstance(num, int):
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
                    d = Direction.LEFT if c1 != c else Direction.TOP
                    self.add_program_line(f'{prefix}edge({r2}, {c2}, "{d}").')

        t_be = tag_encode("belong_to_shape", "omino", 3, "grid")
        for area_id, (num, coord_list) in enumerate(sums):
            self.add_program_line(area(_id=area_id, src_cells=coord_list))

            edge_tag = f'edge(R + 1, C, "{Direction.TOP}")'
            if len(coord_list) > 1 and coord_list[0][0] == coord_list[1][0]:  # the rule is in order
                edge_tag = f'edge(R, C + 1, "{Direction.LEFT}")'

            self.add_program_line(f":- #count {{ R, C: area({area_id}, R, C), {t_be}(R, C, 0, _), {edge_tag} }} != {num}.")
            area_id += 1

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
