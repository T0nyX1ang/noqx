"""The Heyawake solver."""

import itertools
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


def avoid_area_2x2_rect(_id: int, color: str = "black") -> str:
    """Avoid 2x2 rectangle in areas."""
    rule = f":- area({_id}, R, C), area({_id}, R + 1, C), area({_id}, R, C + 1), area({_id}, R + 1, C + 1), not {color}(R, C), not {color}(R + 1, C), not {color}(R, C + 1), not {color}(R + 1, C + 1).\n"
    return rule


def avoid_area_isolated_inner_cell(_id: int, color: str = "black") -> str:
    """Avoid isolated non-border cells in areas."""
    rule = f":- area({_id}, R, C), area({_id}, R - 1, C - 1), area({_id}, R - 1, C + 1), area({_id}, R + 1, C - 1), area({_id}, R + 1, C + 1), {color}(R, C), not {color}(R - 1, C - 1), not {color}(R - 1, C + 1), not {color}(R + 1, C - 1), not {color}(R + 1, C + 1).\n"
    return rule


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


def calculate_penalty(_id: int, ar: Iterable[Tuple[int, int]], puzzle: Puzzle) -> int:
    """Calculate penalties of an area."""
    rows, cols = puzzle.row, puzzle.col

    def calculate_each_border_penalty(r: int = 0, c: int = 0) -> int:
        i, segment_border_penalty = 0, 0
        while i < cols:
            segment = 0
            while (r, i) in ar and i < cols:
                segment += 1
                i += 1

            segment_border_penalty += (segment + 1) // 2
            i += 1

        i = 0
        while i < rows:
            segment = 0
            while (i, c) in ar and i < cols:
                segment += 1
                i += 1

            segment_border_penalty += (segment + 1) // 2
            i += 1

        return segment_border_penalty

    loop_penalty = 0
    for r, c in itertools.product(range(rows), range(cols)):
        plus_segment = 0
        for dr, dc in ((0, 0), (0, 1), (1, 0), (1, 1)):
            r1, c1 = r + dr, c + dc
            if (r1, c1) not in ar and puzzle.surface.get((r1, c1)) in [1, 3, 4, 8]:
                plus_segment = 0
                break

            plus_segment += (r1, c1) in ar

        if plus_segment >= 2 and r + 1 < rows and c + 1 < cols:
            loop_penalty += 1

    border_penalty = 0
    border_penalty += calculate_each_border_penalty(0, 0)
    border_penalty += calculate_each_border_penalty(rows - 1, cols - 1)

    print("Area", _id, "has total penalty of", loop_penalty + border_penalty)

    return loop_penalty + border_penalty


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
        calculate_penalty(_id=i, ar=ar, puzzle=puzzle)

        print("Area", i, "has total shaded of", puzzle.text[rc] if rc else "N/A")

        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="gray", _type="area", _id=i))

            if puzzle.param["fast_mode"] and data > len(ar) // 4:
                solver.add_program_line(avoid_area_2x2_rect(_id=i, color="gray"))
                solver.add_program_line(avoid_area_isolated_inner_cell(_id=i, color="gray"))
                solver.add_program_line(area_border(_id=i, ar=ar))
                solver.add_program_line(area_border_connected(_id=i, color="gray", adj_type="x"))

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
