"""The Mannequin Gate solver."""

from collections import deque
from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import grid_color_connected


def distance_in_room(ar: Tuple[Tuple[int, int], ...]) -> str:
    """Calculate the shortest distance between every grid in the room using BFS."""
    n = len(ar)
    pt_to_idx = {pt: i for i, pt in enumerate(ar)}
    neighbors = [[] for _ in range(n)]

    # pre-build adjacency list
    for i, (r, c) in enumerate(ar):
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nbr = (r + dr, c + dc)
            if nbr in pt_to_idx:
                neighbors[i].append(pt_to_idx[nbr])

    lines: List[str] = []
    for start_node in range(n):
        distances = {start_node: 0}
        queue = deque([start_node])

        lines.append(f"dist({ar[start_node][0]}, {ar[start_node][1]}, {ar[start_node][0]}, {ar[start_node][1]}, 0).")

        while queue:
            u = queue.popleft()
            d = distances[u]

            for v in neighbors[u]:
                if v not in distances:
                    distances[v] = d + 1
                    lines.append(f"dist({ar[start_node][0]}, {ar[start_node][1]}, {ar[v][0]}, {ar[v][1]}, {d}).")
                    queue.append(v)

    return "\n".join(lines) + "\n"


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
            "data": "m=edit&p=7VRBb9pMEL3zK6I9z2F3bRrbl4qm8F0oaQtVFFkWMsRpUKHmM7iqFvHf82a8liuVKGkjcaoWj57fzozfzA67+7/Oq4L6WEFEmgyWtZE8oeZfu2ar/bpILmhQ7x/KCoDoejSi+3y9K3qp98p6BxcnbkDuvyRVRpGyeIzKyH1KDu5D4obkpthSFIEbN04WcNjBG9lndNWQRgNPPAa8BVyuquW6mI8b5mOSuhkp/s47iWaoNuWPQnkd/L4sN4sVE4t8j2J2D6ut39nVd+W32vua7Ehu0MidnpAbdHIZNnIZnZDLVbxe7npbnhIaZ8cjGv4ZUudJyqq/dDDq4DQ5wE6Sg7KaQwOoaE5F2aAt2hPhJRNvO6IvIbolkMhIuluxI7FW7AxfIxeIfS9Wi+2LHYvPECLiEC3Cdy0S6oCMsQ02FtjzhvnQ+8TAUCEYA/or1j5Wc6zxsezT5oyAY4+RhxvA2GLUrfe38Lfe3yIP96TlA+8fwD/gPKjhRiq5EhuKfSMVXnK3X3gechJIbJEzag7n9Z19VlvKZfvVfxnKeqma1tV9viwwgsO7r8XFpKw2+Rpvk3qzKKr2Hf/9Y0/9VPKkOD8K/10HZ78OuPn6jy6FM8zdM3JSjEF7K5C7JrWt5/l8WWLG0DvZbS+KJ7b/PnhKNn6C17/xZ+8b/rLqe12tFmWtst4j",
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
            self.add_program_line(distance_in_room(ar))
            self.add_program_line(count(target=2, color="gray", _type="area", _id=i))
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(f"area_num({i}, {num}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
