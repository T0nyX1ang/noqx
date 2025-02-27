"""The View solver."""

from noqx.puzzle import Puzzle
from noqx.rule.common import display, fill_num, grid, invert_c
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_num_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def bulb_num_color_connected(color: str = "white", adj_type: int = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells starting from a bulb.

    An adjacent rule and a grid fact should be defined first.
    """
    tag = tag_encode("reachable", "bulb", "branch", "adj", adj_type, color)

    initial = f"{tag}(R, C, R, C) :- number(R, C, _)."
    bulb_constraint = f"{color}(R, C), adj_{adj_type}(R, C, R1, C1), (R - R0) * (C - C0) == 0"
    propagation = f"{tag}(R0, C0, R, C) :- number(R0, C0, _), {tag}(R0, C0, R1, C1), {bulb_constraint}."
    constraint = f":- number(R, C, N), {{ {tag}(R, C, _, _) }} != N + 1."
    return initial + "\n" + propagation + "\n" + constraint


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(fill_num(_range=range(0, puzzle.row + puzzle.col), color="white"))
    solver.add_program_line(invert_c(color="white", invert="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_num_adjacent())
    solver.add_program_line(bulb_num_color_connected(color="white"))

    for (r, c, d, _), symbol_name in puzzle.symbol.items():
        validate_direction(r, c, d)
        if symbol_name == "ox_E__1":
            solver.add_program_line(f"not white({r}, {c}).")
        if symbol_name in ("ox_E__4", "ox_E__7"):
            solver.add_program_line(f"white({r}, {c}).")

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))

    return solver.program


__metadata__ = {
    "name": "View",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VTBbtpAEL37K6I5z8G7tsHeG0mhF+q0hSpClmUZ6gqrIFOD02gR/56ZsRUHNTmkapJLtdqn92Zn8dvZWfa/mrwuMKThheiiouH5WqZ2I5luN+blYVOYCxw1h3VVE0G8nkzwR77ZF07SZaXO0UbGjtB+NAkoQNA0FaRov5ij/WRsjHZGS4CKYtM2SRMd9/RG1pldtUHlEo87TnRBdFXWq02RTdvIZ5PYOQJ/51J2M4VtdVtA54P1qtouSw4s8wMdZr8ud93Kvvle/Wy6XJWe0I5au4sn7Hq9XaatXWZP2OVTsN3qLhu/gtUoPZ2o5F/JbGYS9v2tp2FPZ+ZIGJsj6Ii2arpnuRXwgzMZaJKKG6HVg5D1gxxy9uBBRupsc3SerJRP2u80fV6JiYXgRFALzskjWk/wg6ArGAhOJWcseCN4JegLDiRnyKd8UR0e2wHdGu8vCQI+md9HXslxormYj0fwtjp1Eoib7bKoL+Kq3uYbarLZOt8VQC/55MAdyEw8Svb/P+53eNxcfvevW/t9XlpClaXOttcIuybLs1VFfUV1k/jwmfhL85+JB+rf/I4O/4i/eZXpDwJuy+I3pM49",
        },
        {"url": "https://puzz.link/p?view/9/9/g0i0t0i0q0h0i0p0i0q0g0i0j", "test": False},
    ],
}
