"""The Heyawake solver."""

from typing import Iterable, Set, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect


def avoid_diamond_pattern(color: str = "black") -> str:
    """Avoid diamond patterns (radius = 1)."""
    rule = f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), not grid(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), not grid(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), not grid(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), not grid(R, C + 1).\n"

    return rule


def limit_area_2x2_rect(limit: int, _id: int, color: str = "black") -> str:
    """Limit 2x2 rectangle in areas."""
    rule = f"rect_2x2({_id}, R, C) :- area({_id}, R, C), area({_id}, R + 1, C), area({_id}, R, C + 1), area({_id}, R + 1, C + 1), not {color}(R, C), not {color}(R + 1, C), not {color}(R, C + 1), not {color}(R + 1, C + 1).\n"
    rule += f":- {{ rect_2x2({_id}, R, C) }} > {limit}.\n"
    return rule


def limit_border(limit: int, ar: Iterable[Tuple[int, int]], puzzle: Puzzle, _type: str, color: str = "black") -> str:
    """Limit the border shades of an area."""
    if _type == Direction.TOP:
        n, key = puzzle.col, 0
    elif _type == Direction.BOTTOM:
        n, key = puzzle.col, puzzle.row - 1
    elif _type == Direction.LEFT:
        n, key = puzzle.row, 0
    elif _type == Direction.RIGHT:
        n, key = puzzle.row, puzzle.col - 1
    else:
        raise ValueError(f"Invalid border type: {_type}")

    def coord(i: int) -> Tuple[int, int]:
        return (key, i) if _type in ["top", "bottom"] else (i, key)

    rule, i = "", 0
    while i < n:
        segment, data = 0, []
        while coord(i) in ar and i < n and puzzle.surface.get(Point(*coord(i))) != 2:
            r, c = coord(i)
            data.append(f"{color}({r}, {c})")
            segment += 1
            i += 1

        minimum = (segment + 1) // 2 - limit
        if len(data) > n // 2 - 1 and minimum > 0:
            rule += f":- {{ {';'.join(data)} }} < {minimum}.\n"

        i += 1

    return rule


def area_border_simple(_id: int, ar: Iterable[Tuple[int, int]]) -> str:
    """Generates a simpler fact for the border of an area."""
    borders: Set[Tuple[int, int]] = set()
    for r, c in ar:
        for dr, dc in ((0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            r1, c1 = r + dr, c + dc
            if (r1, c1) not in ar:
                borders.add((r, c))

    rule = "\n".join(f"area_border({_id}, {r}, {c})." for r, c in borders)
    return rule


def area_border_connected(_id: int, color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """Generate a constraint to check the reachability of {color} cells connected to borders of an area."""
    tag = tag_encode("reachable", "area", "border", "adj", adj_type, color)
    initial = f"{tag}({_id}, R, C) :- area_border({_id}, R, C), {color}(R, C)."
    propagation = (
        f"{tag}({_id}, R, C) :- {tag}({_id}, R1, C1), area({_id}, R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    )
    constraint = f":- area({_id}, R, C), {color}(R, C), not {tag}({_id}, R, C)."

    return initial + "\n" + propagation + "\n" + constraint


class HeyawakeSolver(Solver):
    """The Heyawake solver."""

    name = "Heyawake"
    category = "shade"
    aliases = ["heyawacky"]
    examples = [
        {
            "data": "m=edit&p=7ZZRT9swFIXf+yuQn/0Q2zexnZeJsbIXBttgmlBVVaWUUa1VWUunKVX/+47dEyJNSGyaxl5QqfnqHF9fX584WX/bjFdTbWz6c0EX2uAjUfLX+TJ/C34uZvfzaX2gDzf3t8sVQOuz42N9M56vp70BVcPetol1c6ibt/VAGaWVxdeooW4+1NvmXd30dXOOS0oH9J3sRRbY7/Bzvp7oaN9pCvApGXgJnMxWk/l0dLLveV8Pmgut0jyv8+iEarH8PlXMI/2eLBdXs9RxNb7HYta3szteWW+ul183qp1ip5vDfbrnj6TrunTdQ7ru8XTtv083Dnc7lP0jEh7Vg5T7pw5Dh+f1dpfy2iop09BXyCXvDXpNvnaZ2+Pc2txeYKhuXG7f5LbIbZnbk6zpI6L1om0sVG2x4zCNjYbswY4cwLLnUIArsgF7sgNHMkxYMGYswNRHA6Y+OjD1ybSm1VdgS/Zg5hAjuMyM2OCKDL21ZOitI0NvqTfQW+rTHWMDGTnYSMZN4wwZMR1jWugd9RZ6R72FXqi30EurD2AhIwdhDg5rF09GTGFM3L6upN5BX1Iv0JfUC/Ql9YJaVQUZOVTMQbD2imsXxKwYs0wHAvVlOhioL6H31JfQe+or1MqzVhVy8Myhwto9114hZmBMD32g3kMfqPfQB+rhMRdbPXKgxxx85egrxAZz7fCYo8cQW0vB2gYPZs4hgqmHx4QeQ2wwc0gHIn2F2GDOC48JPYbY4EB24EiG3hoy9LbVIwd6TIoA3uePecAVGTlYT0Z8+g3jtNA/GKdFCjLi0z8YB2Z8eEnoJYzTQm9gHJhzwRtCb2AcmPHhE6FPME4L9x3jwJwL+y7cd4wDMz48IK0HfH6gdHv30F913vDJS6HbUx+7WhWhq1XR9seHfRHju/qb0NXfQGPb+hTdXljT7YW13V64VNu2Vli741oc1u5YK4e1O+6Lw7y8r/G/2xdJdW7rlurc1g3zlm3dUs05b5lq3tZQuEe79HBJR+xRbiW3VT56fTrTf/PUV2lBQaucw/4R8PdH/pO5DVA+8+infOlPn2FvoM43q5vxZIrHev/6y/TgdLlajOf4dbpZXE1X7W+8Ve166ofK34HDYHl50fpPL1ppC4o/et16hnvtiXQGqC7uxuZMq7vNaDyaLOEx1C7140D6tf/Zs8dhMez9BA==",
        },
        {
            "url": "https://puzz.link/p?heyawake/19/15/201480mhg2i40a8s192816704r503gk0m2g2oa0a18085010k046g0003hu0104000400fbvgvo005fu1800o0000000800600000003s0003c-1c140411g81ah8233",
            "config": {"fast_mode": True},
            "test": False,
        },
        {
            "data": "m=edit&p=7VNdS8MwFH3vrxh5vg9N0q5t3ubcfJnzYxMZpYyuVjfcqHarSEb/uze3mUUYiIjog4Qczr05SU4+7va5SsscQghAhuACxyY9AdL1wOty6q5t09VunasO9KrdsiiRAFwMh3Cfrre5E1tV4ux1pHQP9JmKGWfABHbOEtBXaq/PlR6AnuAQgxBzo0YkkA5aekvjhvWbJHeRjy1HOkOarcpsnc9HTeZSxXoKzOxzQrMNZZviJWfWh4mzYrNYmcQi3eFhtsvVkx3ZVnfFY8UOW9Sge43dyRG7srUr3+3K43bFz9uNkrrGa79Gw3MVG+83LQ1bOlH72vjaM9HFqTzEx6anYTIysQ1Rw0k5IxwSCsIpLgRaEp4SuoQ+4Yg0A1yf+7h24DIlcEU/Qs4bHuAmobRcIPesBvV+ZPPuR30gGh5Kq6/NlZut+oQeYZcsBOakX7qL75/2Uzux6FJhtc3/2ThxYjapyvs0y/G/DO4e8s64KDfpGqNxtVnk5SHGcq0d9sqox3jB4P1X8C9VsHkC96/93b9mB6spcd4A",
            "config": {"fast_mode": True, "limit_border": 1},
        },
        {
            "url": "https://puzz.link/p?heyawake/12/12/00000o0003063cc0o00030000000008020080a4a92a02008020000-2811111111",
            "config": {"fast_mode": True, "limit_2x2": 1},
            "test": False,
        },
    ]
    parameters = {
        "fast_mode": {"name": "Fast Mode", "type": "checkbox", "default": False},
        "limit_border": {"name": "Border Limit", "type": "number", "default": 0},
        "limit_2x2": {"name": "2x2 Limit", "type": "number", "default": 0},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(avoid_same_color_adjacent(color="gray"))
        self.add_program_line(avoid_diamond_pattern(color="gray"))
        self.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))

            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count(num, color="gray", _type="area", _id=i))

                    if puzzle.param["fast_mode"] and num > len(ar) // 4:
                        lmt_2x2 = int(puzzle.param["limit_2x2"])
                        lmt_border = int(puzzle.param["limit_border"])
                        self.add_program_line(area_border_simple(_id=i, ar=ar))
                        self.add_program_line(area_border_connected(_id=i, color="gray", adj_type="x"))
                        self.add_program_line(limit_area_2x2_rect(lmt_2x2, _id=i, color="gray"))
                        self.add_program_line(limit_border(lmt_border, ar, puzzle, _type=Direction.TOP, color="gray"))
                        self.add_program_line(limit_border(lmt_border, ar, puzzle, _type=Direction.BOTTOM, color="gray"))
                        self.add_program_line(limit_border(lmt_border, ar, puzzle, _type=Direction.LEFT, color="gray"))
                        self.add_program_line(limit_border(lmt_border, ar, puzzle, _type=Direction.RIGHT, color="gray"))

        for r in range(puzzle.row):
            borders_in_row = [c for c in range(1, puzzle.col) if Point(r, c, Direction.LEFT) in puzzle.edge]
            for i in range(len(borders_in_row) - 1):
                b1, b2 = borders_in_row[i], borders_in_row[i + 1]
                self.add_program_line(avoid_rect(1, b2 - b1 + 2, color="not gray", corner=(r, b1 - 1)))

        for c in range(puzzle.col):
            borders_in_col = [r for r in range(1, puzzle.row) if Point(r, c, Direction.TOP) in puzzle.edge]
            for i in range(len(borders_in_col) - 1):
                b1, b2 = borders_in_col[i], borders_in_col[i + 1]
                self.add_program_line(avoid_rect(b2 - b1 + 2, 1, color="not gray", corner=(b1 - 1, c)))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
