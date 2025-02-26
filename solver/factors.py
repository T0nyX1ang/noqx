"""The Rooms of Factors solver."""

from typing import Iterable, Tuple

from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, full_bfs
from noqx.solution import solver


def area_product_aggregate(_id: int, src_cells: Iterable[Tuple[int, int]]) -> str:
    """Generate a constraint to aggregate the product of the numbers in the area."""
    rule = ""
    for i, (r, c) in enumerate(src_cells):
        if i == 0:
            rule += f"area_product({_id}, {i}, N) :- number({r}, {c}, N).\n"
        else:
            rule += f"area_product({_id}, {i}, N1 * N2) :- area_product({_id}, {i - 1}, N1), number({r}, {c}, N2).\n"
    return rule.strip()


def number_exclusion(target: int, grid_size: int, _id: int) -> str:
    """Generate a constraint to exclude the number from the cells."""
    rule = ""
    for num in range(1, grid_size + 1):
        if target % num != 0:  # exclusion for non-factorable numbers
            rule += f":- area({_id}, R, C), number(R, C, {num}).\n"
    return rule.strip()


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    fail_false(puzzle.row == puzzle.col, "This puzzle must be square.")
    n = puzzle.row
    solver.add_program_line(grid(n, n))
    solver.add_program_line(fill_num(_range=range(1, n + 1)))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(unique_num(_type="col", color="grid"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(area_product_aggregate(_id=i, src_cells=ar))

        for r, c in ar:
            if Point(r, c, Direction.CENTER, "sudoku_0") in puzzle.text:
                num = puzzle.text[Point(r, c, Direction.CENTER, "sudoku_0")]
                fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
                solver.add_program_line(f":- not area_product({i}, {len(ar) - 1}, {num}).")
                solver.add_program_line(number_exclusion(int(num), grid_size=n, _id=i))

            if Point(r, c, Direction.CENTER, "normal") in puzzle.text:
                num = puzzle.text[Point(r, c, Direction.CENTER, "normal")]
                fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
                solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))

    return solver.program


__metadata__ = {
    "name": "Rooms of Factors",
    "category": "num",
    "aliases": ["roomsoffactors"],
    "examples": [
        {
            "data": "m=edit&p=7ZRfb9owFMXf+RSVn/0Q/wXyxjrYC2PrylRVUYQCTVc0ULpApimI795z7csom6Zqnbq9TFGuznV+do7ta2++NEVdSo/H9GQiFR7tfXiVteFN+Jkut6syPZODZntX1RBSvhuN5G2x2pSdjKm8s2v7aTuQ7Zs0E0pIofEqkcv2It21b9N2IttLfBJSoW0cIQ05PMqr8J3UeWxUCfQE2sRu15CLZb1YlbNxbHmfZu1UCvrPq9CbpFhXX0vBPihfVOv5khrmxRaT2dwt7/nLprmpPjfMqnwv28Gv7ZqjXZLRLqkf7fJ8XthuP9/vsewfYHiWZuT941H2jvIy3SFOQlTpTtheDyMoTY6E7WskGiWAxCUJEsuJpUSjGJB4bZGY+MVrGsCgVCixYbReTMLQoQ9+dh1+OQpRhziFI9maEF+HmIToQhwHZgiLitxpONMoImWgDWsMTVZIazCGGQ3GMEO/N8wYMJYZA8YyY51UzrHGRJyP2qGv574OjGfGgfHMeDBdZjyYLjN0drrMkAfN7RqMPrSD0V32Qz6ZMWAMM7SwhhmLk3nwb2kuj/xb5sm/Zd6Bd8w78I55h7m7g2cwnhkPxjPjwYS5YxOuwlach2hD9GGLulRSv1V0grYxEx5HIl4IgvYsnhFuoAlmdGHEhlimf1I/T04go9r5/mAtn6vzTiaGN5/Ks0lVr4sVjumkWc/L+pDjXtx3xDcR3gwLLO3/q/IfXZW0BckzLswXrcQn7GRYXdTqyfm5b2bFbFGh2LCIBOCSOzlPPwG4OR6dr1Pgr08Yp0/cFottVW9E3nkA",
        },
        {
            "url": "https://puzz.link/p?factors/15/15/77kfnev5ulvdbs9vs5tpnrfblfbalfcf6iuuuapp9jsceghsd7jnsffo7v7jvhjo9u3u3dkojbsguffds7us-84+780-1a=110*6db0-9c-87-14=518*378c+5dc-62-164+1ef+120-75-28+1ef-a5+118-7e+9e76-48-62-18+1f8+738+168+24c+5a0-28%aa8+144+384-2c2-96-27+6e4+104-14+160-5a-23*ebb0*15cc+4eca$22c6cc$22550$38f30+270-1c-9a-1be-96+738-f0-2d-60-82-a2+555+168+1b8-1e+3d4-20-7e-8f",
            "test": False,
        },
    ],
}
