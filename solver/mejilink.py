"""The Mejilink solver."""

from typing import Dict, Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, display, fill_line, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_border
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import convert_line_to_edge, single_route


def bypass_area_edges() -> str:
    """Get the edges that not pass through the area."""
    rule = f'bypass_area_edges(A, R, C, "{Direction.LEFT}") :- area_border(A, R, C, "{Direction.LEFT}"), not edge(R, C, "{Direction.LEFT}").\n'
    rule += f'bypass_area_edges(A, R, C, "{Direction.RIGHT}") :- area_border(A, R, C, "{Direction.RIGHT}"), not edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f'bypass_area_edges(A, R, C, "{Direction.TOP}") :- area_border(A, R, C, "{Direction.TOP}"), not edge(R, C, "{Direction.TOP}").\n'
    rule += f'bypass_area_edges(A, R, C, "{Direction.BOTTOM}") :- area_border(A, R, C, "{Direction.BOTTOM}"), not edge(R + 1, C, "{Direction.TOP}").\n'
    return rule


class MejilinkSolver(Solver):
    """The Mejilink solver."""

    name = "Mejilink"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7ZZLb9NAEMfv+RTVnuewL9u7voWScAkt0FZVZUVRmhoakcglD4Qc5bvz3/G6RrSVCBKBA7I8+XlmPY/17CjrL9vpqiSHyziSpHAZq/nW0vMt43U53yzK/IT62819tQIQnQ+H9HG6WJfUK+KycW9X+7zuU/0mL4QWJBRuLcZUv8939du8HlB9AZMgNSax3C4281m1qFai1dUjkBWkgQNg0uA12wOdguBUSfBZZOANcDZfzRblZNRo3uVFfUkixH7FbwcUy+prKZrX+HlWLW/nQXE73aDC9f38QZCBYb29qz5vRRthT3X/gAoUO+EKIjYVmOcr0H+8Aj/e7/FxPqCGSV6Ecq46dB1e5Lt9SCtIxfKG5ZClZnmJpVQblq9ZSpYJyxGvGbC8ZnnK0uY7oRJHKpMiV+iM1HfsNClnGvaGlLfMWibowjTq7SPjF5x1rFzDKutYBvYNG0naqI6tjqygj2wN9DGuCZxEPXJIYiyLWInr2LZ6xLKt3oHbuFhj4hoNnyb6DKdLyahHDlrHPcEpzCI77IOzsfYEe9LuQ6i9rdGFUxprx6nV7frgv6lXZRY+k8jwk0U/qe04S8FZx87FHLIfGN/O+UfWMuYvsZ+yjYWcs5iDQyyXduyDfzRCym2ShX47ckcKo5CbdwRIGrDhazKEVvTuadP+lHGhUx6U3ZUc93ncK8Tg7lN5clatltMFpgA/DVbTdSkwgPc98U3wXaDhwvr/M/kfnsnhQ8m/PpkPO5YFNhyzHLMh9YLqcxIP28l0gj0X+A9Av2TOwqRTv2fG6T3QgGN+sMEfaHg5OIp5/g1pDjS8mC4m2xPD0bsG03Hc+w4=",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(convert_line_to_edge())
        self.add_program_line(bypass_area_edges())

        # construct the edge grid
        edges: Dict[Tuple[int, int, str, str], bool] = {}
        for r in range(puzzle.row):
            for c in range(puzzle.col + 1):
                edges[Point(r, c, Direction.LEFT)] = True

        for r in range(puzzle.row + 1):
            for c in range(puzzle.col):
                edges[Point(r, c, Direction.TOP)] = True

        for (r, c, d, label), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')
            if label == "delete" and not draw:
                edges[Point(r, c, d)] = False

        rooms = full_bfs(puzzle.row, puzzle.col, edges)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=edges))
            self.add_program_line(f":- #count {{ (R, C, D): bypass_area_edges({i}, R, C, D) }} != {len(ar)}.")

        self.add_program_line(display(item="edge", size=3))

        return self.program
