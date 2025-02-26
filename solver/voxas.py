"""The Voxas solver."""

from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, general_shape
from noqx.solution import solver


def voxas_constraint(r: int, c: int, r1: int, c1: int, symbol_name: str) -> str:
    """Generate a constraint for the voxas puzzle."""

    tag = tag_encode("belong_to_shape", "voxas", "grid")

    rule = ""
    if symbol_name == "circle_SS__1":  # white circle, shape and orientation are the same
        rule += f":- {tag}({r}, {c}, T, V), {tag}({r1}, {c1}, T1, V1), |T - T1| + |V - V1| != 0."

    if symbol_name == "circle_SS__2":  # black circle, shape and orientation are different
        rule += f":- {tag}({r}, {c}, T, V), {tag}({r1}, {c1}, T1, V1), |T - T1| + |V - V1| != 2."

    if symbol_name == "circle_SS__5":  # gray circle, either shape are different or orientation are different
        rule += f":- {tag}({r}, {c}, T, V), {tag}({r1}, {c1}, T1, V1), |T - T1| + |V - V1| != 1."

    return rule


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(general_shape("voxas", 2, OMINOES[2]["I"], color="grid", adj_type="edge"))
    solver.add_program_line(general_shape("voxas", 3, OMINOES[3]["I"], color="grid", adj_type="edge"))
    solver.add_program_line(all_shapes("voxas", color="grid"))

    for (r, c, d, _), symbol_name in puzzle.symbol.items():
        validate_type(symbol_name, ("circle_SS__1", "circle_SS__2", "circle_SS__5"))
        fail_false(puzzle.edge.get(Point(r, c, d)) is True, f"Circle must be on an edge at ({r}, {c}).")

        if d == Direction.TOP and r > 0:
            solver.add_program_line(voxas_constraint(r, c, r - 1, c, symbol_name))

        if d == Direction.LEFT and c > 0:
            solver.add_program_line(voxas_constraint(r, c, r, c - 1, symbol_name))

    for (r, c, d, _), draw in puzzle.edge.items():
        solver.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))

    return solver.program


__metadata__ = {
    "name": "Voxas",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VVda9swFH3Pryh61oOlK8mJ37ou20uXbktHKcYEN/XWsBR3STOGQ/57j660uVlVCoV9wXB8dXJ9dXR0rz7WXzb1qpEq8z8aSrR4jBryq4eO3yw+p4vbZVMcyMPN7VW7ApDyZCI/1st1MyhjUDXYdqOiO5Td66IUWkh+lahk967Ydm+K7lx2U3wSUsF3DKSE1IDjHp7xd4+OglNlwBNgCt3OAeeL1XzZzKbTEPm2KLtTKfxAL7i7h+K6/dqIwMH/5+31xcI7LupbTGZ9tbiJX9aby/bzJsaqaie7w6B3nNBLvV4Pg16PftYbJ/Sr9Y6q3Q6Jfw/Fs6L04j/0cNjDabGFnbBVbM+LrTBWgUdjtD2J8LtH/EP41UN/7nke+q1O81tN8NuE34+b8qfHdWST/M6aJI9zaX6Xp/nzTCfj88yPm/CrLO0nz5PgpzzhR3FecYk021NUUHbE9iXbjK1le8wxYxRTa2xaAwHIB1qpfRI8tgYYghlbqd0oYDeSOo/xFn3vYwthzEM91og3KJzHpIAjpwGnjZwWMS7yOGjIo4YcGvIY79D3PnZIDvPg4PmOCfEGReG+2h9GAeNQoizyj4B9woHRStJhLLTAgR+tJAra0EqK+SHkag/rMEdS9APrEeJVmC9lCjhyKnDqyImcEEUeggYTNRhoiPkh5GoP+8XAPMMeZ4hXfr4o5hmX9IitYeu41Lnfys/e7M9bVU/KKTFrf3XsP/bf81WDUowvPzUHk3Z1XS9x2E6v6ptG4F7bDcQ3wW9J/pb8f9X9savOFyH72/bAE3JKLAeDg6I7keJmM6tn8xbLC9l77MNv149tXA3uAA==",
        }
    ],
}
