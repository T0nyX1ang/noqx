"""The Heyawake solver."""

from typing import Iterable, List, Tuple, Union

from .core.common import area, count, display, grid, shade_c
from .core.helper import full_bfs, tag_encode
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.penpa import Direction, Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


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
            "data": "m=edit&p=7ZZLbxs3HMTv+hQGzzzsktznzU3VXhz3YRdBIAiBomxqITLUylYfa/i750dyWB0aoKe2OQQrUaPVcPjncEjtw6+nzXGytYsv39vK1lxhCOntuya9K123u8f9NF7Yy9Pj3eEIsPa7a/t+s3+YFiuR1ouneRjnSzt/O65MbaxxvGuztvMP49P8cpyXdr7hJ2N77l1lkgMuz/BV+j2iF/lmXYGvhYGvgdvdcbuf3lzlO9+Pq/nWmjjOV6l3hOb+8NtkVEf8vj3cv93FG283j8zl4W73i355OL07fDiJW6+f7XyZy735RLn+XG6EudyIPlFunMW/XO6wfn7G9h8p+M24irX/dIb9Gd6MT7TXqa1T+zq136TWpfYWqp19ar9ObZXaJrVXibMcn4zrgnVDZUbHCpMRN9TCHdgL9+CQcV+BW+Ea3Al78CBM5ippDhVY/KEGiz94sPgxo3Xht2An3IFVwzCAm4TRBmdNtK13mY82OPPRBotfw3fixw3iemFqcLkGtK33ee5og6Xp4HvxHXwvvoMfxHfwQ+H34OwV2mDV4Jl7yHNHGyxNdqtvxPfwG/ED/Eb8AL8RP+BVm71CG6waAnNvNfeAZivNJu5/8Zt4DojfwO/Eb+B34rd41cmrlho61dAy905zb9HspdnB78Xv4Pfid/B78cmYV8bSWaSMeXLllSu0wZo7GfPKGNo2VPK278CquR/A4pOxoIyhDVYN8fxTrtAGa1wyFpQxtMHZW7TBuWa0bXCZjza48KlBGQtVD871Mw4418A44FwD44ClT36C8kM/G0KujX5g6Tv0g/TJUlCW6GeDskE/sMYiG0HZoB9Y+uQkKCf0s0HrTj+wxmLdg9adfmDpk4FQMhDXTvfz/0i5T+ZLNjgrWMvzmionyauqeMtY2u98/rUuoYZT/K/hFP9rOK74E71V/S56W7yK3sorH70tXjF3r7l45u7llWfuXuviGVf7ms/zuoToc/Et+lx8Y9ym+BY917hN9Lx4yLhpjThcX6Uj9kVqQ2rbdPR28Qz/j0/5fyxnhWPxieHvV/PlfrzWi5W5OR3fb7YT/9zLdz9PF9eH4/1mb3hQel6YP0x6r3x87Pry7PQ/PTvFJag+t731uZXDbjd305+b3zcfJrNefAQ=",
        },
        {
            "url": "https://puzz.link/p?heyawake/19/15/201480mhg2i40a8s192816704r503gk0m2g2oa0a18085010k046g0003hu0104000400fbvgvo005fu1800o0000000800600000003s0003c-1c140411g81ah8233",
            "config": {"fast_mode": True},
            "test": False,
        },
        {
            "data": "m=edit&p=7VNNa9wwEL37VyxznoMl+Wt126ZuL9vtx24JwZjgOErXxItb77pptfi/ZzQWuIdAKSU0hyL0eDN6kp4+5vhtqHqDGaaoMgxRUFORRBVGGCWCe+jbrjm1Ri9wNZz2XU8E8f0G76r2aILCi8rgbJfartC+1QUIQJDUBZRoP+qzfadtjnZLQ4AZ5daTSBLNZ3rJ445dTEkREt94TvSKaN30dWuu11Pmgy7sDsHt84pnOwqH7rsB78PFdXe4aVzipjrRWY775qsfOQ633f3gtaIc0a4mu9sn7KrZrqOTXceesOtO8cx2l+U40rV/IsPXunDeP880m+lWnwk3+gwyoakio7fmpwG1dLEPSSNYecX4hlEy7mghtIrxNWPIGDOuWZPT+iKmtdMQtKQV4yVxMfGUNsmU55J45DWkj8kE5+kX/qpP5cQz5fW0ySVvdcEYMSZsIXUn/aO7+PvT/tZOIROuq7nFzxuXQQHbob+rakP/Jb/9Yhabrj9ULVB5jgH8AO4FXShG/yv2H1Wse4Lwpf3Vl2aHqgf25mf1UN0bKINH",
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
