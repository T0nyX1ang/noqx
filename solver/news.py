"""The NEWS solver."""

from typing import List

from noqx.puzzle import Point, Puzzle
from noqx.rule.common import area, count, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.solution import solver


def news_constraint() -> str:
    """Generate a constraint for NEWS."""
    mutual = "area(A, R, C), area(A, R1, C1)"
    rule = f":- {mutual}, number(R, C, 1), number(R1, C1, N1), N1 != 1, R1 <= R.\n"  # northest in area
    rule += f":- {mutual}, number(R, C, 2), number(R1, C1, N1), N1 != 2, C1 >= C.\n"  # eastest in area
    rule += f":- {mutual}, number(R, C, 3), number(R1, C1, N1), N1 != 3, C1 <= C.\n"  # westest in area
    rule += f":- {mutual}, number(R, C, 4), number(R1, C1, N1), N1 != 4, R1 >= R.\n"  # southest in area
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)

    news_dict = {"N": 1, "E": 2, "W": 3, "S": 4}
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(unique_num(color="grid", _type="row"))
    solver.add_program_line(unique_num(color="grid", _type="col"))
    solver.add_program_line(unique_num(color="grid", _type="area"))
    solver.add_program_line(news_constraint())

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(fill_num(_range=range(1, 5), color="white", _type="area", _id=i))
        solver.add_program_line(count(len(ar) - 2, color="white", _type="area", _id=i))

    for (r, c, d, _), symbol_name in puzzle.symbol.items():
        validate_direction(r, c, d)
        symbol, style = symbol_name.split("__")
        validate_type(symbol, ("ox_B", "ox_E"))
        fail_false(style in ["4", "7", "8"], f"Invalid symbol at ({r}, {c}).")
        solver.add_program_line(f"white({r}, {c}).")

    for (r, c, d, pos), letter in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        fail_false(letter in ("N", "E", "W", "S"), f"Clue at ({r}, {c}) must be in 'NEWS'.")
        solver.add_program_line(f"number({r}, {c}, {news_dict[str(letter)]}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


def refine(solution: Puzzle) -> Puzzle:
    """Refine the solution."""
    rev_news_dict = {1: "N", 2: "E", 3: "W", 4: "S"}
    for (r, c, d, pos), num in solution.text.items():
        solution.text[Point(r, c, d, pos)] = rev_news_dict[int(num)]
    return solution


__metadata__ = {
    "name": "NEWS",
    "category": "var",
    "examples": [
        {
            "data": "m=edit&p=7ZTPbtpAEMbvPEW05z3g/WMT30gKvaROW1JFkYWQSdyCCjIBXEWLePd8M15jNdCgICWnyvLo5/Hs7Dfj8a4ey2yZyxCX7si2DHCpMOQ7MIbvtr9uputZHp/JbrmeFEuAlNf9vvyZzVZ5K/VRw9bGnceuK93nOBWBkELhDsRQum/xxn2JXU+6AV4J2YHvqgpSwF6Dt/ye6LJyBm1w4hl4ByyeRhfV09c4dTdS0B4XvJJQzIs/ufAa6Pm+mI+n5BhnaxSymkwX/s2qfCh+lz42GG6l61ZSkwNSdSOVsJJKdEAqVeCl9t5B6vlwu0W7v0PsKE5J948GOw0O4g1swjZgexdvhIqQxsimj0KrPY996TH6pceaPc9e5nAvT7S3VxT+7YHMPotVbG9Qi3Sa7Se2bbaW7RXH9FBWYDHDFtkVxs6ohjXYeFZgqrZmhaqYNRj1MGP6FXQTB7ZhBaa+cE5i6GbGH6NRee03PsaArWeLnDvGXtQ7jiH2GjSYulyz9jEaa+t9LdXlYyhP6DkER7Uf+1Lf2Q+O6rWkx2u20ExfS6F5t9zCS7aGbcitjWiI3jRmglqYCow87SHo3W7sTvuqR+Wl9BV3Fyo8lYctCH/4lZ8lxXKezfDbJeV8nC+b58EkW+QC59y2JZ4E3ynaLs3/o++Djz5qffvkA/CdJvGInBSdxaxWPaqmQyzKUTa6LzBcaCAH6GMBSrrrw/5UJK9nPryQdjxp4WtK8lNL2B0db1lo/r3ww4cAJ5LIHpd0TjwD",
        }
    ],
}
