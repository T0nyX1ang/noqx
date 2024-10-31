"""The Kakuro solver."""

from typing import List, Tuple

from .core.common import area, display, fill_num, grid, unique_num
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    # Find sections and their corresponding clues
    # 'sum' is 0 when the clue is blank; this is because we need to check every run for duplicates.
    sums: List[Tuple[int, List[Tuple[int, int]]]] = []

    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name.startswith("kakuro") and (r, c) not in puzzle.sudoku:
            puzzle.sudoku[(r, c)] = {}  # set empty kakuro cell

    def end_run(start_coord: Tuple[int, int], coords: List[Tuple[int, int]], idx: int):
        if start_coord in puzzle.sudoku:
            value = puzzle.sudoku[start_coord]
            if len(coords) > 0:
                if len(value) == 0:
                    sums.append((0, coords))
                elif idx in value:
                    sums.append((int(value[idx]), coords))
            elif len(value) != 0 and idx in value:
                return False
        else:
            sums.append((0, coords))
        return True

    # Across sections
    for r in range(puzzle.row):
        start_coord = (r, -1)
        coords = []
        for c in range(puzzle.col):
            if (r, c) in puzzle.sudoku:
                if not end_run(start_coord, coords, 1):
                    return []
                start_coord = (r, c)
                coords = []
            else:
                coords.append((r, c))
        end_run(start_coord, coords, 1)

    # Down sections
    for c in range(puzzle.col):
        start_coord = (-1, c)
        coords = []
        for r in range(puzzle.row):
            if (r, c) in puzzle.sudoku:
                if not end_run(start_coord, coords, 2):
                    return []
                start_coord = (r, c)
                coords = []
            else:
                coords.append((r, c))
        end_run(start_coord, coords, 2)

    area_id = 0

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))

    for sum_clue, coord_list in sums:
        if len(coord_list) > 0:
            solver.add_program_line(area(_id=area_id, src_cells=coord_list))
            solver.add_program_line(fill_num(_range=range(1, 10), _type="area", _id=area_id))
            if sum_clue > 0:
                solver.add_program_line(f":- #sum {{ N: area({area_id}, R, C), number(R, C, N) }} != {sum_clue}.")
            area_id += 1

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(unique_num(_type="area", color="grid"))
    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Kakuro",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VZNb9swDL3nVxQ66yBK/r5lXbtLl25rh6IwjCHZMrRoAxdpMgwO8t9LUrKTKDwVKIZhg2OGfJTFR1KS/TB9WC9bDYZ+rtD4j1cCBd+2yPg24bq+Xz3OqxM9Xq/u2iUqWl+en+uf08fn+agOo5rRpiurbqy7D1WtQGll8QbV6O5ztek+Vt1Ed1foUhoQu/CDLKpnO/WG/aSdehAM6hPUnX/sFlVP3tufqrq71oqivONnSVWL9tdcBRZkf28Xs3sCZtMVpvJ8d/8UPM/rH+3DOoyFZqu7MZPtHQJlt6NMqqdMWkw55PSmlG2z3WLhvyDpb1VN/L/u1GKnXlUblBOWUG1UCQXPkCmd4JyltWTatDczMpNgOcPOMphZyY/23pK9ubfA4Bw0GJsfbJ7KYv+8nfJwt7MTng1z8Xae78+Otic6+EvHdiADgLRo/t4PiWfXx4eC+YQ8AUqermdrDecNgw3MbohuwUfr2Vr0HNgJcHTT2xnbQ3Rb+mx6dg4j7VfDHbYBXHi+55NgXkM1sXW32DruhtXDmsI1phwNgwij1GKM0okxSinGqGgxRo2MMUonxiilGKOmRFgixE2EuIkQNxXyTYV8UyHfVOCXCvwyqnOMCVwyoQa5wCUXuPBij7BCiFEK+YIRCIIRooARSo07TwKF4LgHBZB3whEo1BGsUHCQViJIywn3gARKj0srCvi8OQKleqZS7qlESVpCIK0hyCRK2VHlcWuf89lsWV7joa07x/I9S8MyZXnBY85Y3rA8ZZmwzHhMTsf+K14M/ox5Izq1898Zh1f692HNqFaT9WI2X55M2uVi+oiv5it+Le/Zd9OnucKvou1I/VZ8144+sv5/KP2xDyVqgnn1ruC3Z3f5b+xVXLZDN5rRCw==",
        },
        {
            "url": "https://puzz.link/p?kakuro/15/15/m-dm.ffl-7l9-mQjmIBmbam-anWZs.jSpBjo.7goP4lJ9m..nAjo74lf-.lUUrF9l7-qHNq-clKTrO4l.-clgIoibn.JbmHglfgo.gOo7NpA-.s7Hnb-m-fm-7m-7m-hl-4l.-Dm-Em46BfgJjhSK79acVZD",
            "test": False,
        },
    ],
}
