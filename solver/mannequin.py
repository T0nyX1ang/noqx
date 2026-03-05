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
            "data": "m=edit&p=7VVNb9swDL3nVxQ68yBRzmL7MmRdskuWbkuKoTCMwHHd1ZgNZ048DAry30fRcr0BDtp9oNhhUEQ8PZEUKcrM/kuT1BmMaWgfJCgaiD5PT9pfN9b5ocjCC5g2h/uqJgBwNZ/DXVLsMxhFTi0eHU0QmimYN2EklACBNJWIwbwPj+ZtaGZgVrQlwCdu0SohwVkPP/K+RZctqSThpcMEbwimeZ0W2WbRMu/CyKxB2HNesbWFoqy+ZsLFYddpVW5zS2yTA2Wzv893bmff3FafG/FwhCib4pCnVVHVgv2p+ARm2qawGkhB9ynohxT0cAr4V1IodtVQ8MFw8CcqzAcKfxNGNpPrHvo9XIXHk43yKFBaS02mbfUE6u5yHOFNLPGyJ8Zsgh1BjhS7u2E5Z4ks13QaGM3yNUvJcsxywTozCiLw6NroXCSHUoNS2GKFhB2vLO85nYCwdFj9jKWzldZWOVv1g0+fcOAw+UFni/RNoNNH0kenj+QHdc9rp69JXzs/mniv8zMhfd/hwOmf7EOx2V6y9Fi+4FuY2Io8sWbCBYt0rt8W8M9v/9HYImzbhR3jp6F4FIlVU98laUZPd3b7KbtYVnWZFLRaNuU2q7s19ZHTSHwTPCOqMXj/W8s/21pskeQvNZhneJ+PhBPRc+k6DJgrELtmk2woM0H/YsC7XdM5s/37xiugFjDMy3PuuBEFZ087t/3st06NIR59Bw==",
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
