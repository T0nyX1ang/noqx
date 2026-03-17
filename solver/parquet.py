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
            "data": "m=edit&p=7VdNbxs3EL37VwR75mH5zdXNTdxeXKetHRSBIBiKozRCZSiVrKJYQ/+9bzhvtYUTQUERBDkE8i6fuY8zw9l55HL7126+WRjr5M8X0xqLX+hCvXyO9Wr5u1k+rBaTZ+Z89/B+vQEw5uWVeTdfbRfmbErW7Oyx7yb9uel/mkwb25jG4bLNzPS/Th77nyf9hemv8agxZWaa+93qYXm3Xq03Te2z4F3qQAd4McLf63NBz7XTtsBXxICvAe+Wm7vV4vZSe36ZTPsb04jvH+pogc39+u9Fw9jk/7v1/ZuldLyZP2CC2/fLD43xeLDdvV3/uWsGD3vTn+sMrj9zBn6cgT/MwH96Bu5LzGAz326X2+VqNV9+YgrdbL/H2/kNk7idTGU+r0ZYRng9edxLXHK39f663n+sd1fvN6Ca3tf7i3pv6z3W+2XlXEweG9+ihtrUTJwBTsCZOAMX4gLcEXfG21axbYGtYg++Jx+V6j35HvxAfgA/kB8ssCNGcQevOIGfyc/gZ/Iz+Jn8DH4mP3vgQFw1UbHLnXEdcRfHOC3sOM7R5dFvgJ3ImGN3sKMaY34y8pM5NmNs5nwz5ps5Fn59YfwF8Rf164pFPJnxYKylXwu/jmOd5Ip+A/wmxpzswa8rHnY62pF3Qb4F3w/vQnLLOAN8pSG3/j9xglPIKdmEVjloTbDKQWuCV/toTYhqH60JKY/5L7RZwG/JR10FR74D32faga9IXxG+UjfmuWP8HfisQ7SwQ74Dn3WFFnboK8IX66TyWbdogclH3QbWLVpg8lEPwTpiB+xH+6xbtMDko24D6xYtMPmonxACMdbn+h73sqiI1J7Xe4DgXNeq4Kyp2MmkBSMBI07AjjgDe+ICHDg2aIFX7FWgFTsVrpWCkmJ3xOh3aqcK2gXiPPa7qAKtOKhwh36XiJMKSHAU0dBODCpcS9HHyH6MjRwbk4q44qwitlwM4mCzqBAtF4bIuchiUGinxAMOrRSL2gwWL98qP3gpFo0tBCkWjQ0tio5jbdFir3acisCywCPjLEULvHKCFrhV0eAZ++GrpS8RjaMvB1+evnxSEVT7TkVgKRTWQxUK31cViqd9EQrzjD4VQe1HPHnw5VQo1WZSAUmcUm+sq7pAdnxHEJlnjdWFbcCdV9EQe9ZbXeQOGO+XtYdWxVRxUjER+47zdUHFVHFUMVkKlHVYBeoic4i8uSEnsOkGO1kFZylWx/w4sTPkRBYqjkW9BdZVFe4BS/45VoQbh7GwkxkPNoGQGU9CPDmNOHG+slEk5jO1ulFYbixu0CDyFpi3EHSBFyxfdJa6llwxb67ImsD1oTjgQk7Rhd9y07C0aWHTD7prdROw3EAC4wmwn/hektMNwXJDSLSTgm5clS8x05eXzZlzkY3FM07ZfFryW/kQoC8rc5E8Y8FL9Wsjy2fLZ37YNJ57ObJUvtRXzsfL8JPYpj7UL+uPf/F7v/xmZ9Pmerd5N79b4Jv24u0fi2dX6839fNXgPLE/a/5p6jXFx4mQvx8xvuUjhryp9isfNE5K8EQ4U9TM4bBi+pem+bC7nd8i6Q3OtIaP9fxy9LEeaY4+1lPO0cd68Dn2mGeh//n4hPFToZ2Y2Im0HE/qNZb+J/2O/fFJv5999YrBuj07+xc="
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
