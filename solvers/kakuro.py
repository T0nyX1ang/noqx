"""The Kakuro solver."""

from typing import List, Tuple

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import area, display, grid
from .utilsx.rule import fill_num, unique_num
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    # Find sections and their corresponding clues
    # 'sum' is 0 when the clue is blank; this is because we need to check every run for duplicates.
    sums: List[Tuple[int, List[Tuple[int, int]]]] = []

    def end_run(start_coord: Tuple[int, int], coords: List[Tuple[int, int]], idx: int):
        if start_coord in E.clues:
            value = E.clues[start_coord]
            if len(coords) > 0:
                if value == "black":
                    sums.append((0, coords))
                elif isinstance(value, list):
                    sums.append((value[idx], coords))
            elif value != "black" and value[idx] != 0:
                return False
        else:
            sums.append((0, coords))
        return True

    # Across sections
    for r in range(E.R):
        start_coord = (r, -1)
        coords = []
        for c in range(E.C):
            if (r, c) in E.clues:
                if not end_run(start_coord, coords, 0):
                    return []
                start_coord = (r, c)
                coords = []
            else:
                coords.append((r, c))
        end_run(start_coord, coords, 0)

    # Down sections
    for c in range(E.C):
        start_coord = (-1, c)
        coords = []
        for r in range(E.R):
            if (r, c) in E.clues:
                if not end_run(start_coord, coords, 1):
                    return []
                start_coord = (r, c)
                coords = []
            else:
                coords.append((r, c))
        end_run(start_coord, coords, 1)

    area_id = 0

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))

    for sum_clue, coord_list in sums:
        if len(coord_list) > 0:
            solver.add_program_line(area(_id=area_id, src_cells=coord_list))
            solver.add_program_line(fill_num(_range=range(1, 10), _type="area", _id=area_id))
            if sum_clue > 0:
                solver.add_program_line(f":- #sum {{ N: area({area_id}, R, C), number(R, C, N) }} != {sum_clue}.")
            area_id += 1

    solver.add_program_line(unique_num(_type="area", color="grid"))
    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
