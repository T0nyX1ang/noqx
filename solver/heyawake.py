"""The Heyawake solver."""

from typing import Iterable, List, Tuple, Union

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def avoid_diamond_pattern(color: str = "black") -> str:
    """Avoid diamond patterns (radius = 1)."""
    rule = f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), not grid(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), not grid(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), not grid(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), not grid(R, C + 1).\n"

    return rule.strip()


def limit_area_2x2_rect(limit: int, _id: int, color: str = "black") -> str:
    """Limit 2x2 rectangle in areas."""
    rule = f"rect_2x2({_id}, R, C) :- area({_id}, R, C), area({_id}, R + 1, C), area({_id}, R, C + 1), area({_id}, R + 1, C + 1), not {color}(R, C), not {color}(R + 1, C), not {color}(R, C + 1), not {color}(R + 1, C + 1).\n"
    rule += f":- {{ rect_2x2({_id}, R, C) }} > {limit}.\n"
    return rule


def limit_border(limit: int, ar: Iterable[Tuple[int, int]], puzzle: Puzzle, _type: str, color: str = "black") -> str:
    """Limit the border shades of an area."""
    if _type == "top":
        n, key = puzzle.col, 0
    elif _type == "bottom":
        n, key = puzzle.col, puzzle.row - 1
    elif _type == "left":
        n, key = puzzle.row, 0
    elif _type == "right":
        n, key = puzzle.row, puzzle.col - 1
    else:
        raise AssertionError(f"Invalid border type: {_type}")

    def coord(i: int) -> Tuple[int, int]:
        return (key, i) if _type in ["top", "bottom"] else (i, key)

    rule, i = "", 0
    while i < n:
        segment, data = 0, []
        while coord(i) in ar and i < n and puzzle.surface.get(coord(i)) != 2:
            r, c = coord(i)
            data.append(f"{color}({r}, {c})")
            segment += 1
            i += 1

        minimum = segment // 2 - limit
        if len(data) > n // 2 - 1 and minimum > 0:
            rule += f":- {{ {';'.join(data)} }} < {minimum}.\n"

        i += 1

    return rule.strip()


def area_border(_id: int, ar: Iterable[Tuple[int, int]]) -> str:
    """Generates a fact for the border of an area."""
    borders = set()
    for r, c in ar:
        for dr, dc in ((0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            r1, c1 = r + dr, c + dc
            if (r1, c1) not in ar:
                borders.add((r, c))

    rule = "\n".join(f"area_border({_id}, {r}, {c})." for r, c in borders)
    return rule


def area_border_connected(_id: int, color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells connected to borders of an area.

    An adjacent rule and an area fact should be defined first.
    """
    tag = tag_encode("reachable", "area", "border", "adj", adj_type, color)
    initial = f"{tag}({_id}, R, C) :- area_border({_id}, R, C), {color}(R, C)."
    propagation = (
        f"{tag}({_id}, R, C) :- {tag}({_id}, R1, C1), area({_id}, R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    )
    constraint = f":- area({_id}, R, C), {color}(R, C), not {tag}({_id}, R, C)."

    return initial + "\n" + propagation + "\n" + constraint


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="x"))
    solver.add_program_line(avoid_adjacent_color(color="gray"))
    solver.add_program_line(avoid_diamond_pattern(color="gray"))
    solver.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))

        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="gray", _type="area", _id=i))

            if puzzle.param["fast_mode"] and data > len(ar) // 4:
                lmt_2x2 = int(puzzle.param["limit_2x2"])
                lmt_border = int(puzzle.param["limit_border"])
                solver.add_program_line(area_border(_id=i, ar=ar))
                solver.add_program_line(area_border_connected(_id=i, color="gray", adj_type="x"))
                solver.add_program_line(limit_area_2x2_rect(lmt_2x2, _id=i, color="gray"))
                solver.add_program_line(limit_border(lmt_border, ar, puzzle, _type="top", color="gray"))
                solver.add_program_line(limit_border(lmt_border, ar, puzzle, _type="bottom", color="gray"))
                solver.add_program_line(limit_border(lmt_border, ar, puzzle, _type="left", color="gray"))
                solver.add_program_line(limit_border(lmt_border, ar, puzzle, _type="right", color="gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    for r in range(puzzle.row):
        borders_in_row = [c for c in range(1, puzzle.col) if (r, c, Direction.LEFT) in puzzle.edge]
        for i in range(len(borders_in_row) - 1):
            b1, b2 = borders_in_row[i], borders_in_row[i + 1]
            solver.add_program_line(avoid_rect(1, b2 - b1 + 2, color="not gray", corner=(r, b1 - 1)))

    for c in range(puzzle.col):
        borders_in_col = [r for r in range(1, puzzle.row) if (r, c, Direction.TOP) in puzzle.edge]
        for i in range(len(borders_in_col) - 1):
            b1, b2 = borders_in_col[i], borders_in_col[i + 1]
            solver.add_program_line(avoid_rect(b2 - b1 + 2, 1, color="not gray", corner=(b1 - 1, c)))

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Heyawake",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7ZbPbhs3HITveoqAZx52Se7fm5vavbhOW7sIAkEwFGVTG5GhVLaadg2/ez6SwwpoA7RA2/QSrESNqOHwx+Estfc/H9b7ydYuvnxvK1tzhSGkt++a9K50Xd0+bKfxmT05PNzs9gBrX5yd2bfr7f20WIq1WjzOwzif2PmbcWlqY43jXZuVnb8fH+dvx/nUzpf8ZGxP33kmOeDpEb5Mv0f0PHfWFfhCGPgKuLndb7bT9Xnu+W5czlfWxHm+SqMjNHe7XyajOuL3ze7u9W3seL1+YDH3N7fv9cv94c3u3UHcevVk55Nc7uUnyvXHciPM5Ub0iXLjKv7jcofV0xO2/0DB1+My1v7jEfZHeDk+0l6ktk7tq9Sepdal9gqqnX1qv05tldomteeJczo+GtcF64bKjI4dJiRuqIU7sBfuwSHjvgK3wjW4E/bgQZjQVdIcKrD4Qw0Wf/Bg8WNI68JvwU64A6uGYQA3CaMNzppoW+8yH21w5qMNFr+G78SPd4jrhanB5RrQtt7ntaMNlqaD78V38L34Dn4Q38EPhd+Ds1dog1WDZ+0hrx1tsDS5XX0jvoffiB/gN+IH+I34Aa/a7BXaYNUQWHurtQc0W2k28QAQv4kHgfgN/E78Bn4nfotXnbxqqaFTDS1r77T2Fs1emh38XvwOfi9+B78Xn4x5ZSwdRsqYJ1deuUIbrLWTMa+MoW1DJW/7Dqya+wEsPhkLyhjaYNUQD0DlCm2w5iVjQRlDG5y9RRuca0bbBpf5aIMLnxqUsVD14Fw/84BzDcwDzjUwD1j65CcoP4yzIeTaGAeWvkM/SJ8sBWWJcTYoG4wDay6yEZQNxoGlT06CcsI4G7TvjANrLvY9aN8ZB5Y+GQglA3Hv1J//SEo/mS/Z4KxgL497qpwkr6riLXPpfufz930JNZzifw2n+F/DccWf6K3qd9Hb4lX0Vl756G3xirV7rcWzdi+vPGv32hfPvLqv+TzuS4g+F9+iz8U35m2Kb9FzzdtEz4uHzJv2iMP1ZTpin6c2pLZNR28Xz/C/ecpzJ5uxtybV8G8d+X9Z2xL74vPDn6/mS3+8VouluTzs3643E3/jp29+mp5d7PZ3663hqelpYX416b308SHsy4PU//QgFbeg+syPU//0vl/iLnff/MKa94fr9fVmtzU8i9vYzwH0x/7PXj2Hg7mZflt/WL+bzGrxEQ==",
        },
        {
            "url": "https://puzz.link/p?heyawake/19/15/201480mhg2i40a8s192816704r503gk0m2g2oa0a18085010k046g0003hu0104000400fbvgvo005fu1800o0000000800600000003s0003c-1c140411g81ah8233",
            "config": {"fast_mode": True},
            "test": False,
        },
        {
            "data": "m=edit&p=7VPLbtswELzrK4I970Ek9TJvbir34roPuwgCQQgUhamFyFArW33Q0L9nuSKgHgIURRE0h4LgYHY5JIePPX4dqt5ghimqDEMU1FQkUYURRongHvq2a06t0Re4HE77rieC+G61wvuqPZqg8KoyONuFtku0b3QBAhAkdQEl2g/6bN9qm6Pd0hBgRrn1JJJE85le8bhjl1NShMQ3nhO9Jlo3fd2am/WUea8Lu0Nw+7zi2Y7CoftmwPtwcd0dbhuXuK1OdJjjvvniR47DXfcweK0oR7TLye72CbtqtuvoZNexJ+y6Uzyz3UU5jnTtH8nwjS6c908zzWa61WfCjT6DTGiqyOix+WlALVzsQ9IIVl4zrhgl444WQqsYXzOGjDHjmjU5rS9iWjsNQUtaMV4QFxNPaZNMeS6JR15D+phMcJ6+4a/6VE48U15Pm1zxVpeMEWPCFlJ30j+6i78/7W/tFDLhwppb/LxxGRSwHfr7qjb0X/K7z+Zi0/WHqgUqzzGAH8C9oAvF6H/F/qOKdU8QvrS/+tLsUPXA3vysvlcPBsrgEQ==",
            "config": {"fast_mode": True, "limit_border": 1},
        },
        {
            "url": "https://puzz.link/p?heyawake/12/12/00000o0003063cc0o00030000000008020080a4a92a02008020000-2811111111",
            "config": {"fast_mode": True, "limit_2x2": 1},
            "test": False,
        },
    ],
    "parameters": {
        "fast_mode": {"name": "Fast Mode", "type": "checkbox", "default": False},
        "limit_border": {"name": "Border Limit", "type": "number", "default": 0},
        "limit_2x2": {"name": "2x2 Limit", "type": "number", "default": 0},
    },
}
