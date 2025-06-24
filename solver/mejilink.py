"""The Mejilink solver."""

from typing import Dict

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.loop import convert_direction_to_edge, single_loop
from noqx.rule.neighbor import adjacent, area_border
from noqx.rule.reachable import grid_color_connected


def bypass_area_edges() -> str:
    """
    Get the edges that not pass through the area.

    An area fact and an area_border fact should be defined first.
    """
    rule = 'bypass_area_edges(A, R, C, "l") :- area_border(A, R, C, "l"), not edge_left(R, C).\n'
    rule += 'bypass_area_edges(A, R, C, "r") :- area_border(A, R, C, "r"), not edge_left(R, C + 1).\n'
    rule += 'bypass_area_edges(A, R, C, "u") :- area_border(A, R, C, "u"), not edge_top(R, C).\n'
    rule += 'bypass_area_edges(A, R, C, "d") :- area_border(A, R, C, "d"), not edge_top(R + 1, C).\n'
    return rule.strip()


class MejilinkSolver(Solver):
    """The Mejilink solver."""

    name = "Mejilink"
    category = "loop"
    examples = [
        {
            "data": "m=edit&p=7VZdb9s2FH33ryj4WgIjqS9KwB6c1O7apY7TJshiwTAUR0mUylEmS0mnIP+9hxQ1W7JdzAOW7WEQdHV0LnW/SN/r5e9llMdU4rIkZZTjsmyhb8F8fTNznSZFGgdvaL8sbrMcgNLj4ZBeR+kyph8vbo8Os/7Tu/5vj7KYTPh7Vn5g53fDu7efF79+SKycD0dy/Gn8KRE3/V8OD07cwVt3XC7PivjxZMEP7s4mp9fj8xtf/DEYTexqcsycj5Prnx77Zz/3QhPDtPdc+UHVp9X7ICSCUMJxCzKl1UnwXH0KqgGtvkBFKJ9SsijTIplnaZaThquOgGxCBeAA0KnhudYrdAgEo5wBjwwGvACcJ/k8jWdHNTMOwuqUEuX7QH+tIFlkj7FypuJS7/NscZko4jIqUL7lbfJAqAXFsrzKvpZmKZ++0Kq/Rwb4BkZ0BgbWGSi0JQOV2D+bgT99ecHmfEYOsyBU6ZytoFzBL8Ez5EhLruWFlkMthZanWEorS8t3WjItHS2P9JqBludaHmppB8+EO5Jyj5GA42S4/gpLQbm0auxblPu2xoI5OOKu4e0/MZ7A3gpzWWPurTBT2K+xxaiw+ArbwmAO3mDbAm/8Wgo7hkcMjvFlw5dj7CtsNzx82Q0vgRu/WGOZNQI2LWNT/XR5nbsQiEHUMXAXP3HPYIk6yDoe7juoSVMHlXuTI3wx44ujJYhmvbJf58s9GzZrv3gCGzuu4g32XOA6To1lbZ9Lbw1j72TtS2HBTPwM9WSNL8TsmRgkfEljX2Ff2cdBcPUx8dR5e+UTSSyO2HxJAVAQBWy1mxqoo+jLzUPbiTgUKE/rQmqv+T7thWRwdRO/GWX5IkrRBfTbII+WMUEDJsssnS3L/Dqax7P4WzQvSFDPgHVNi7svF5cxOtgalWbZQ5rcb7PQqFpkcnOf5fFWlSJjhLjDlFJtMXWZ5VedmJ6iNG3noqdji6o7aIsqcrTHtfcoz7OnFrOIitsWsdZKW5bi+04xi6gdYvQ16nhbrMrx0iPfiL5DtAK1k/9Py//wtFQbxf71mblfwwxRcExZdG3XJ7Q6puShnEUz1Jzg3xn9S2pPzSAU4e+o0Vf3VKAB763w91Tsdo5ktn/BrD0VO8PFzNlQvPqp0a0oy38wF1bKLr1lOoD9wYBY027jd8yCNW2X32j8KtjN3g92S/sH250AoDaHAMiNOQBuxyhQVrvTQEXVHQjK1cZMUK7Wx0I47X0H",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(direction("lurd"))
        self.add_program_line(shade_c(color="mejilink"))
        self.add_program_line(fill_path(color="mejilink"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="mejilink", adj_type="loop"))
        self.add_program_line(single_loop(color="mejilink"))
        self.add_program_line(convert_direction_to_edge())
        self.add_program_line(bypass_area_edges())

        # construct the edge grid
        edges: Dict[Point, bool] = {}
        for r in range(puzzle.row):
            for c in range(puzzle.col + 1):
                edges[Point(r, c, Direction.LEFT)] = True

        for r in range(puzzle.row + 1):
            for c in range(puzzle.col):
                edges[Point(r, c, Direction.TOP)] = True

        for (r, c, d, pos), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")
            if pos == "delete" and not draw:
                edges[Point(r, c, d)] = False

        areas = full_bfs(puzzle.row, puzzle.col, edges)
        for i, ar in enumerate(areas):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=edges))
            self.add_program_line(f":- #count {{ (R, C, D): bypass_area_edges({i}, R, C, D) }} != {len(ar)}.")

        self.add_program_line(display(item="edge_top", size=2))
        self.add_program_line(display(item="edge_left", size=2))

        return self.program
