"""The Parquet solver."""

from typing import Dict, List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_same_color
from noqx.rule.reachable import border_color_connected, grid_color_connected
from noqx.rule.shape import avoid_rect


def area_shade_unique(room_map: Dict[Tuple[Tuple[int, int], ...], List[int]], color: str) -> str:
    """Ensure that each bigger area has a unique smaller area shadeing color."""
    rule = ""
    for i, area_ids in enumerate(room_map.values()):
        rule += "\n".join(f"room_map({i}, {j})." for j in area_ids) + "\n"

    rule += f":- room_map(M, _), #count {{ A : room_map(M, A), area(A, R, C), {color}(R, C) }} != 1."
    return rule


class ParquetSolver(Solver):
    """The Parquet solver."""

    name = "Parquet"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=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"
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(area_same_color(color="gray"))
        self.add_program_line(avoid_rect(2, 2, color="gray"))
        self.add_program_line(grid_color_connected(color="gray", adj_type=4))
        self.add_program_line(border_color_connected(puzzle.row, puzzle.col, color="not gray", adj_type=8))

        edges: Dict[Tuple[int, int, str, str], bool] = {}
        for r in range(puzzle.row):
            for c in range(puzzle.col + 1):
                edges[Point(r, c, Direction.LEFT)] = puzzle.edge.get(
                    Point(r, c, Direction.LEFT, "delete"), True
                ) or puzzle.edge.get(Point(r, c, Direction.LEFT, "normal"), False)

        for r in range(puzzle.row + 1):
            for c in range(puzzle.col):
                edges[Point(r, c, Direction.TOP)] = puzzle.edge.get(
                    Point(r, c, Direction.TOP, "delete"), True
                ) or puzzle.edge.get(Point(r, c, Direction.TOP, "normal"), False)

        bigger_rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        rooms = full_bfs(puzzle.row, puzzle.col, edges)
        room_map: Dict[Tuple[Tuple[int, int], ...], List[int]] = {}  # cluster the rooms into bigger_rooms
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            br = next(_br for _br in bigger_rooms if set(ar).issubset(set(_br)))
            room_map.setdefault(br, []).append(i)

        self.add_program_line(area_shade_unique(room_map, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
