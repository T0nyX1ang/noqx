"""The Snake solver."""

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def exclude_checkboard_shape(color: str = "black") -> str:
    """Exclude checkboard-shape shading."""
    rule = f":- {color}(R, C), not {color}(R, C + 1), not {color}(R + 1, C), {color}(R + 1, C + 1).\n"
    rule += f":- not {color}(R, C), {color}(R, C + 1), {color}(R + 1, C), not {color}(R + 1, C + 1)."
    return rule


def simple_shade_path(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a rule to ensure the shaded path is a simple path.

    An adjacent rule should be defined first.
    """
    adj_count = f"#count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }}"

    constraint = f"pass_by_loop(R, C) :- grid(R, C), {color}(R, C), {adj_count} = 2.\n"
    constraint += f"dead_end(R, C) :- grid(R, C), {color}(R, C), {adj_count} = 1.\n"
    constraint += ":- { dead_end(R, C) } != 2.\n"
    constraint += f":- grid(R, C), {color}(R, C), not pass_by_loop(R, C), not dead_end(R, C).\n"
    return constraint


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(grid_color_connected(color="gray"))
    solver.add_program_line(exclude_checkboard_shape(color="gray"))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))
    solver.add_program_line(simple_shade_path(color="gray"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")

        if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
            solver.add_program_line(count(num, color="gray", _type="col", _id=c))

        if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
            solver.add_program_line(count(num, color="gray", _type="row", _id=r))

    for (r, c, d, _), symbol_name in puzzle.symbol.items():
        validate_direction(r, c, d)
        if symbol_name == "circle_L__1":
            solver.add_program_line(f"gray({r}, {c}).")
            solver.add_program_line(f":- dead_end({r}, {c}).")
        if symbol_name == "circle_L__2":
            solver.add_program_line(f"gray({r}, {c}).")
            solver.add_program_line(f":- not dead_end({r}, {c}).")

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))

    return solver.program


__metadata__ = {
    "name": "Snake",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VXPj9o8EL3zV6x89iG2E/LjUtHt0gvNtg2fVihCKKRZgTY0NCFVZcT/vjPjbMNuLPVbVeW0MhnNex7bz2N7aH60WV1w4eJPBdzhAprnO/S5/pg+p2vz7aEsois+aQ+bqgaH89vplN9nZVOMUhwJbTk66jDSE64/RikTjDMJn2BLrr9ER/0p0guuE+hiPABuZoIkuDe9e0f96F0bUjjgx50P7gLcfFvnZbGaGeZzlOo5Z7jOexqNLttVPwvW6UCcV7v1Fol1doDNNJvtvutp2m/VQ9vFiuWJ64mRm1jkql4uukYueha5uIu/l1vuK5vQcHk6QcK/gtRVlKLq/3o36N0kOoKNoyNTIQ59ByrMqTBXAOH1UAEMeugClD0cA4Tb8gQDgOo39JznEIPPl/JxMrwlBgqB8f1aYoz9/ezSwf4zrHDCJzGwH0G7WsCuPJ96nieZhbiXASsEpgAmeUGTeguNkwzpAFcc0NKRVlrao5V1Senaoz1vSMP+p5QFSXYOx821IvuBrEPWIzujmBuyd2SvybpkxxTj44X5n1eK0h7AuYIwae7X+an8I22p55tSM2hvfFeCU5a09X2WF1Az4na3LuqruKp3WQk42WT7gkGZPo3YL0YfvVn3rXJfvHJj8p1X1e8LvK8/yEkhr/AC9S1n+3aVrfIKbhVkDXnfs/MqfA0fI09/HFC7qfLbAl4OvHiaoBKx5nv2gI/pEQ==",
        },
        {"url": "https://puzz.link/p?snake/11/11/00000000000000000000000000000000000000000957664857598o9", "test": False},
        {
            "url": "https://puzz.link/p?snake/15/15/13a3b00000a3d3a00000a3a4a00030a3a3a10000d3aca03001a3a3a10039a3d3a00100j3a39zp",
            "test": False,
        },
    ],
}
