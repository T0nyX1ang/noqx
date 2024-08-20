"""The Firefly (Hotaru Beam) solver."""

from typing import List

from .core.common import direction, display, fill_path, grid
from .core.penpa import Puzzle
from .core.loop import directed_loop
from .core.neighbor import adjacent
from .core.reachable import grid_color_connected
from .core.solution import solver

drdc = {"1": (0, 1), "2": (1, 0), "3": (0, -1), "4": (-1, 0)}
dict_dir = {"1": "r", "2": "d", "3": "l", "4": "u"}


def convert_direction_to_edge() -> str:
    """Convert (directed) grid direction fact to edge fact."""
    rule = 'horizontal_line(R, C) :- grid_out(R, C, "r").\n'
    rule += 'horizontal_line(R, C) :- grid_in(R, C, "r").\n'
    rule += 'vertical_line(R, C) :- grid_out(R, C, "d").\n'
    rule += 'vertical_line(R, C) :- grid_in(R, C, "d").\n'
    return rule.strip()


def restrict_num_bend(r: int, c: int, num: int, color: str) -> str:
    """
    Generate a rule to restrict the number of bends in the path.

    A grid_in/grid_out rule should be defined first.
    """
    rule = f"reachable({r}, {c}, {r}, {c}).\n"
    rule += f"reachable({r}, {c}, R, C) :- {color}(R, C), grid(R1, C1), reachable({r}, {c}, R1, C1), adj_loop_directed(R1, C1, R, C).\n"
    rule += f'bend(R, C) :- {color}(R, C), grid_in(R, C, "l"), not grid_out(R, C, "r").\n'
    rule += f'bend(R, C) :- {color}(R, C), grid_in(R, C, "u"), not grid_out(R, C, "d").\n'
    rule += f'bend(R, C) :- {color}(R, C), grid_in(R, C, "r"), not grid_out(R, C, "l").\n'
    rule += f'bend(R, C) :- {color}(R, C), grid_in(R, C, "d"), not grid_out(R, C, "u").\n'
    rule += f":- #count{{ R, C: grid(R, C), reachable({r}, {c}, R, C), bend(R, C) }} != {num}.\n"

    rule += "firefly_all(R, C) :- firefly(R, C).\n"
    rule += "firefly_all(R, C) :- dead_end(R, C).\n"
    return rule


def solve(puzzle: Puzzle) -> List[str]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ firefly(R, C) } :- grid(R, C), not dead_end(R, C).")
    solver.add_program_line(fill_path(color="firefly", directed=True))
    solver.add_program_line(adjacent(_type="loop_directed"))
    solver.add_program_line(directed_loop(color="firefly"))
    solver.add_program_line(grid_color_connected(color="firefly_all", adj_type="loop_directed"))
    solver.add_program_line(convert_direction_to_edge())

    # warning: incompatible encoding with penpa+/puzz.link
    for (r, c), symbol_name in puzzle.symbol.items():
        shape, style, _ = symbol_name.split("__")
        if shape != "firefly":
            continue

        dr, dc = drdc[style]
        clue = puzzle.text.get((r, c))

        if isinstance(clue, int):
            solver.add_program_line(restrict_num_bend(r + dr + 1, c + dc + 1, clue, color="firefly"))

        solver.add_program_line(f"dead_end({r + 1}, {c + 1}).")
        solver.add_program_line(f'grid_out({r + 1}, {c + 1}, "{dict_dir[style]}").')
        solver.add_program_line(f'{{ grid_in({r + 1}, {c + 1}, D) }} :- direction(D), D != "{dict_dir[style]}".')

    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.add_program_line(display(item="vertical_line", size=2))
    solver.solve()

    return solver.solutions
