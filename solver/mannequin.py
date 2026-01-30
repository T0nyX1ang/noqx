"""The Mannequin Gate solver."""

from collections import deque
from typing import Dict, List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import grid_color_connected


def distance_in_room(ar: Tuple[Tuple[int, int], ...], edge: Dict[Tuple[int, int, str, str], bool]) -> str:
    """Calculate the shortest distance between every grid in the room using BFS."""
    n = len(ar)
    pt_to_idx = {pt: i for i, pt in enumerate(ar)}
    neighbors = [[] for _ in range(n)]

    # pre-build adjacency list
    for i, (r, c) in enumerate(ar):
        if (r, c - 1) in pt_to_idx and not edge.get(Point(r, c, Direction.LEFT)):
            neighbors[i].append(pt_to_idx[(r, c - 1)])

        if (r, c + 1) in pt_to_idx and not edge.get(Point(r, c + 1, Direction.LEFT)):
            neighbors[i].append(pt_to_idx[(r, c + 1)])

        if (r - 1, c) in pt_to_idx and not edge.get(Point(r, c, Direction.TOP)):
            neighbors[i].append(pt_to_idx[(r - 1, c)])

        if (r + 1, c) in pt_to_idx and not edge.get(Point(r + 1, c, Direction.TOP)):
            neighbors[i].append(pt_to_idx[(r + 1, c)])

    lines: List[str] = []
    for start_node in range(n):
        distances = {start_node: 0}
        queue = deque([start_node], n)

        lines.append(f"dist({ar[start_node][0]}, {ar[start_node][1]}, {ar[start_node][0]}, {ar[start_node][1]}, 0).")

        while queue:
            u = queue.popleft()
            d = distances[u]

            for v in neighbors[u]:
                if v not in distances:
                    distances[v] = d + 1
                    lines.append(f"dist({ar[start_node][0]}, {ar[start_node][1]}, {ar[v][0]}, {ar[v][1]}, {d}).")
                    queue.append(v)

    return "\n".join(lines)


def mannequin_constraint(color: str = "black") -> str:
    """
    Generate a rule to enforce the Mannequin Gate constraint.

    An area_adjacent rule and a dist rule are required.
    """
    rule = f"area_num(A, N) :- area(A, R0, C0), area(A, R1, C1), {color}(R0, C0), {color}(R1, C1), (R0, C0) < (R1, C1), dist(R0, C0, R1, C1, N).\n"
    rule += ":- area(A, _, _), area_num(A, N0), area_num(A, N1), N0 < N1.\n"
    rule += ":- area_adj_4(A1, A2), area_num(A1, N), area_num(A2, N).\n"
    return rule


class MannequinSolver(Solver):
    """The Mannequin Gate solver."""

    name = "Mannequin Gate"
    category = "shade"
    aliases = ["mannequingate", "manekingeto"]
    examples = [
        {
            "data": "m=edit&p=7VZhT/JIEP7OrzD71U2u3RYtTS4XRPDVQ0SBcNIQUrBAtWV5S4u+Jf53Z7bbQEtR3zMx9+FSOnn6zOzszCx9YPUzsgOHluHSDKpQFS7GDHHrCn7Sq+uGnmMe0WoUznkAgNKbRoNObW/l0Kv7ebPGq8/n1X/WRjgYqBdKdKn0HxuPx3f+35euFqiNltG+bl+7bFb9UTu7Pakfn7SjVS901re+evbYG3Sn7f6swn7VWwM9Htwo5avB9I91tfdnyZI1DEubuGLGVRpfmBZRCSUMbpUMaXxrbuJrM67TuAMuQg3gmkkQA1jfwr7wI6olpKoAbkkM8B7gxA0mnjNqJkzbtOIuJbjPmViNkPh87RBZBz5PuD92kRjbIYxqNXeX0rOKHvhTJGMhIfEjL3Qn3OMBksi90riatNApaEHbtoAwaQFRQQvY2ddb8Ja8qPhKcfGvcDB3UP7ItLCT3hYaW9gxN2Bb5oYwBVdqsDQ5PcK0dDiS0E+R+GtLlMUSOO6EgESqSHcvbENYJmwXdqOxJuy5sIqwZWGbIqYORVR0GBvsyyCholFVZQlWGWDJq8jrMqYCGKoQGF6TXazItQquVeVajElzGoArEkMeHABiBi8ck/EM4pmMZ5AHZ5LymozXIF6TeTTg9TTPKcQbEkN+EQ999kW3NWF1YU/EFE7xRD55ZuK0IDGDfY3kAL8+/Q9rs3A08ip/Dg1LFulEwdSeOPDVrT/MnKMWD3zbg6dW5I+dIH0GHSEr7o1WSfTIebEnITETKdv1ZLiFyJGhPM6XnrsoypC6MqQ7W/DAKXQh6UDNB1KhqyDVmAcPuZqebc/L9iIkPkMl2pChwgBe/J1nOwj4c4bx7XCeIXZ0LpPJWeSGGdrZEu0nO7ebvx3Ha4m8EHFb8PZR/X/R/8+KPh6S8lvS/w3K8UE5FnxdUu2n8Q0ly2hkj6AzAv8vqPCmPwcH3P9+cYeCOBfzyqF04ieicnC3Q+5vn7p4jXnwjqZunXm6QFmBfUdcd7xF/AEd3fHm+T3RxGL3dRPYAukENq+eQO0LKJB7GgrcARnFrHklxaryYopb7ekpbrUrqRZZRIE75hEZlt4A",
        },
        {
            "url": "https://puzz.link/p?mannequin/10/10/abkt6ij7o7j4nvnu69g4fapb2nsefe4ja3huhag21g2k1h1j1",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(area_adjacent())
        self.add_program_line(mannequin_constraint(color="gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(distance_in_room(ar, puzzle.edge))
            self.add_program_line(count(target=2, color="gray", _type="area", _id=i))
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(f"area_num({i}, {num}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
