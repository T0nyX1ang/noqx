"""The Aquarium solver."""

from typing import Dict, List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type


def water_physics(
    ar: Tuple[Tuple[int, int], ...],
    edge: Dict[Tuple[int, int, str, str], bool],
    color: str = "blue",
) -> str:
    """Generates a constraint to fill the {color} areas according to gravity."""
    pt_to_idx = {pt: i for i, pt in enumerate(ar)}
    rows: Dict[int, List[int]] = {}
    for r, c in ar:
        rows.setdefault(r, []).append(c)

    parent = list(range(len(ar)))

    def find(i: int) -> int:
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i: int, j: int):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j

    lines: List[str] = []

    # water falls down naturally
    for r, c in ar:
        if (r + 1, c) in pt_to_idx and not edge.get(Point(r + 1, c, Direction.TOP)):
            lines.append(f":- {color}({r}, {c}), not {color}({r + 1}, {c}).")

    # connected cells at the same level (row) must be equal, but the connectivity must go from bottom.
    sorted_rows = sorted(rows.keys(), reverse=True)
    for r in sorted_rows:
        cur_cols = rows[r]
        for c in cur_cols:
            idx = pt_to_idx[(r, c)]

            if (r, c - 1) in pt_to_idx and not edge.get(Point(r, c, Direction.LEFT)):
                union(idx, pt_to_idx[(r, c - 1)])

            if (r + 1, c) in pt_to_idx and not edge.get(Point(r + 1, c, Direction.TOP)):
                union(idx, pt_to_idx[(r + 1, c)])

        groups: Dict[int, List[int]] = {}  # group cells in the current row by the connected component leader
        for c in cur_cols:
            idx = pt_to_idx[(r, c)]
            root = find(idx)
            groups.setdefault(root, []).append(idx)

        # enforce water level equality within each group
        for group in groups.values():
            for i in range(len(group) - 1):
                u, v = group[i], group[i + 1]
                lines.append(f":- {color}({ar[u][0]}, {ar[u][1]}), not {color}({ar[v][0]}, {ar[v][1]}).")
                lines.append(f":- {color}({ar[v][0]}, {ar[v][1]}), not {color}({ar[u][0]}, {ar[u][1]}).")

    return "\n".join(lines)


class AquariumSolver(Solver):
    """The Aquarium solver."""

    name = "Aquarium"
    category = "shade"
    aliases = ["aquarium"]
    examples = [
        {
            "data": "m=edit&p=7VZdT9tIFH3nV1R+7UjrGXvsONI+BBq67UIIDYglFopMMBDqYNZJoDXiv/fcmTHxVyjd1VZ9WCWxT869c+d+2XcWf6+iLGbcpq/TYbjj4/KO+omOp362+RzNlkncfcN6q+V1mgEwdrC7yy6jZBGzj6fXeztp7+Fd76/7znI85u/t1Qf75Gb35u2n+Z8fZk7Gdwed4f5wfyauen/sbB96/bfecLU4Xsb3h3O+fXM8ProcnlwF4mt/MHbz8YEtP44vf7vvHf++FXLlm3229ZgH3bzH8vfd0OIWswR+3Dpj+WH3Md/v5n2WjyCyGAe3p5UEYH8NT5Sc0I4muQ08MBjwFHA6y6ZJPNnTzLAb5kfMon221WqC1jy9jy3jB/2fpvPzGRHn0RKpWlzP7oxksbpIP6+MLgxa81WynE3TJM2IJO6J5T0dwqgIQa5DcNYhENQhEGoJgSL7j0MI2kN4Qnk+IYhJN6R4jtews4aj7iOug+6j5XBa6WCprqHlCCK8EuEQIUtEhwi3RAS1Ja5bIzhXTGkNF8rKsw7c4cqpU3XdVVehrkfwmeWOur5TV1tdpbruKZ0+QhHCZ8JFPAIt6dprLCUTHnwk7AV4nhAR4Y5YY+J9W2Mfa32z1ufQkUbfreIAIRAO8JwGxn4QMIdrm7gzR/gaC2+NuQD2DObQR8oVxguA632Vvqv9wZ05EglUvI+1el/cgfW+uDPHMfoO9KkEaq0LrH12HOxVYA47VPuCp7IrHjYL7MBP1/jpkj9FLNBxjY5LNktYGvsuYpdFvMDUAIRtirGEbeODTXkofJPAZl8bPpSxXdQO8ZawCIra4X1Zxr72AXWj96jhqe4l7Bs7vgO+0EcvdUx9fap7CfumBzz0Rhl7Og+4Axd9Rb2k4xUSfnrGN4mekaZnJPaSxr6EzyZvwoUdafwk7BqbqPUzRn2f1xI29cUd2KxFHSuYnmiFEa+pKe7AhR345hZ9hVrQ8636ATk3PSkC9E/RqzZ6jNNaPIgn6nHcUVdXXT31mPr04nnlq8kyQUj4KfV76t+/Hr7rW4iU0egtf7xfiznbCq3RKruMpjEmQv/iKn4zSLN5lODfYDU/j7PiP4a0tUiTyUJrT+Iv0XRpdfU5oSypcLfKRoVK0vQumd22WShEFXJ2dZtmcauIyBg+bzBFohZT52l2UfPpIUqSaizqDFWh9OCtUMsMU7X0P8qy9KHCzKPldYUoTeCKpfi2lsxlVHUx+hzVdpuv0/G0ZX2x1C/EE0hl/f9E9UufqKhU9g+dq37C++o77oTIOAZCfsCsu9UkmiAmlbJWHskN0WTPR6iaGGXQYnOq+ofiF4yPGG93aoTR8koejRPmgyavNlC8OoFisKgTaJvCKz3j7kYJunuDxNso8Y0E57ZapIUHTYmpZEvWTHpaJCpBP5pQdIts12/wm/RNthq8ydUm+3KDPw2+0Hca+j/9mVSv+jR7Ye6uhXW6ZfqCfWEAl6Rt/IZZW5LW+cZgJWebsxVsy3gFW5+woJpDFmRjzoLbMGrJan3aklf1gUtbNWYubVUeu+HZ1jc=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="blue"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(water_physics(ar, puzzle.edge, color="blue"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
                self.add_program_line(count(num, color="blue", _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
                self.add_program_line(count(num, color="blue", _type="row", _id=r))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK and color != Color.BLUE)} blue({r}, {c}).")

        self.add_program_line(display(item="blue"))

        return self.program
