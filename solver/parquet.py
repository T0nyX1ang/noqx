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
            "data": "m=edit&p=7VhbTxtJE33nV0Tzmpa+6ctcbGkfCIFssoRAAuILFkIDMeDEZrJjm2SN+O85VX0mYGMHaVeK8hDZM31cXV23rqqZ9vjvadX0jXXy9aVJjcUndIJevsj0SvnZH0yG/e4Tsz6dXNYNgDFvtrbMeTUc982r95fbG/X6l+fr/78uJ0dH9kU6fZkeftz6+PTt6K+XA9/YrZ1y9/Xu64G7WP9z49levvk0352ODyb9672Rffbx4Gj/fPfwouP+2dw5CrOjN2n26uj8f9frB3+s9WjD8drNrNOd7ZnZi24vsYlJHC6bHJvZXvdm9ro72zSzd5hKTHlsktF0OBmc1cO6SZRmwbcdFzrAzTt4qPOCNiLRpsA7xIDvAc8Gzdmwf7IdKbvd3mzfJKL7ma4WmIzq674oE9vk91k9Oh0I4bSaIHzjy8HnxHhMjKcf6k9TstrjWzNbX/AA1vzIAwhpPRAYPRC0xANx7D970FTj8WA8GA6rwRIXOse3t9idt3DipNsTfw7uYHkH33VvcN/Ru9X7e71v6d3pfR+sZub1/lzvqd4zvW8rz2b3JvEpMjTNk64zwDlwQVwAl8QlcIe4Y7xNI7YpsI3Yg9+TH3XgPfk9+AP5A/gD+YMFdsQoneAjzsFfkL8Af0H+AvwF+QvwF+QvPHAg1opT7IqOcR3iDnxs7bSQ4+ijg82t3gA5GW3OxIa4NlYw41MgPgXXFlhb0N8C/hZcC72+pP0l7C+jXlda2BPXYoQ91Guh13Gtk1hRb4DenDbn4jvXlh5yIj9GyCG/Bb9v90JiSzsDdOVtbCVWrZ3gKclTFiakkQejCTbyYDTBR/kYTciifIwm5G0cILOkzBL8KfmRV8GR34HfR36MkENdGXTlrT2wv0P7O+BnHmKEHPI78DOvMEIOdWXQxTxRfuYtRmDyI28D8xYjMPmRD8HGvMIITF0in3mLEZj8yNvAvMUITH7kTwgxDzECi20oskMttQ29BxSc6yAppOCsbGCKzYRgwQjAHc6BoURxAQwliktgKNG1ISa4YmyCOKoYxSEBAPYIvHdRDkbgKEcL2kU5Wugt3WETxFHFKCYJQEt30WaMsYAEYwN9RjmZFB/5pehlc5SOtRnXZlJAtCeTAqJeaQZZKxO2SSEqHTZn9EWaQUk5JWQSh1SSJcoMFptvI3/wkizRthAkWaJtGJF0XGuRIJLsKgebKUWgPJCZ0c4S9kiCKw82VhJc6bC/pC4pmpS6pGgcdTno8tTl81gEKh+6pAh0LZKX+aCFwv3SQpGGqvyQzziDFotA6bCHMce6WCgqE7qkgMROyTfmlTbIDvcIReaZY9rYWoxc0qIh9sw3bXLfMfaXuYcxFpNi6JViIvbS8NQ2KYjWTvAzx7RAmYdaoC7K1AJlvmEEbuUgJlJwyiP+Mj5O5LQxkUbFtci3wLzSwv2OJf5cK4XLfAMN8aQ9eAgEeQgIzmGPPARaLI1ZcxVxyBlP0PVBoTUiNdXWIOImjUHzWWqKcZP3RWk2WrOIFePm8NDAb2IHHOVgjI1f12JfLGVayPRt3cEGeQioLqll2hMgP+e+5NArDwTFkJNTTg458uBSfrGZurw8nOmLPFg87ZSHT0r+VF4EqMuKLxJnNLxc3zYKeW35yS82Dzvvgjk9H/RV/eEn+02Xz/FaL3k3bc6rsz5eYzc/XPSf7NTNqBomOEIk43p4Mo6zJ/2v1dkk6cZTzP2ZOdrVdHTaxzv4PdKwrj8PB1fLJLRTc8TBxVXd9JdOCbEPG1eIkqklok7r5sOCTV+q4XDeFz3hzZHiGWCONGnwgn/vd9U09Zc5yqiaXM4R7h1n5iT1rxaCOanmTaw+VQvaRnfhuF1LviZ69fCmKNv4+7z3K5/3ZKfSX605PmJODxH/fnI0szcm+Tw9qU4Q9AR/MBhOx8Pkyul4vlw5HY+cK6fjKXTVNA+m/3L6EeGPmfaIY4+EZUVQf3oGaF+pmx80+bvJRfKSVg/qD7r9vdll9BWN/d7sIv1BFxdjHzZyUJf0clAX2zlIDzs6iA+aOmgr+rpIXWztYtVidxdVDxq8qLrf49lanqC3oLUcr30D"
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

            for br in bigger_rooms:
                if set(ar).issubset(set(br)):
                    room_map.setdefault(br, []).append(i)
                    break

        self.add_program_line(area_shade_unique(room_map, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
