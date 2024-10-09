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
                solver.add_program_line(area_border(_id=i, ar=ar))
                solver.add_program_line(area_border_connected(_id=i, color="gray", adj_type="x"))
                solver.add_program_line(limit_area_2x2_rect(limit=1, _id=i, color="gray"))
                solver.add_program_line(limit_border(limit=1, ar=ar, puzzle=puzzle, _type="top", color="gray"))
                solver.add_program_line(limit_border(limit=1, ar=ar, puzzle=puzzle, _type="bottom", color="gray"))
                solver.add_program_line(limit_border(limit=1, ar=ar, puzzle=puzzle, _type="left", color="gray"))
                solver.add_program_line(limit_border(limit=1, ar=ar, puzzle=puzzle, _type="right", color="gray"))

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
