"""The Firefly (Hotaru Beam) solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import direction, display, fill_path, grid
from noqx.rule.loop import directed_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver

drdc = {"1": (0, 1), "2": (1, 0), "3": (0, -1), "4": (-1, 0)}
dict_dir = {"1": "r", "2": "d", "3": "l", "4": "u"}


def convert_direction_to_edge() -> str:
    """Convert (directed) grid direction fact to edge fact."""
    rule = 'edge_top(R, C) :- grid_out(R, C, "r").\n'
    rule += 'edge_top(R, C) :- grid_in(R, C, "r").\n'
    rule += 'edge_left(R, C) :- grid_out(R, C, "d").\n'
    rule += 'edge_left(R, C) :- grid_in(R, C, "d").\n'
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


def solve(puzzle: Puzzle) -> List[Solution]:
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

    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert d == Direction.TOP_LEFT, "The symbol should be placed in the center."
        shape, style = symbol_name.split("__")
        if shape != "firefly":  # pragma: no cover
            continue  # warning: incompatible encoding with penpa+/puzz.link

        dr, dc = drdc[style]
        clue = puzzle.text.get((r - 1, c - 1))  # the text is also placed in the top-left corner

        if isinstance(clue, int):
            solver.add_program_line(restrict_num_bend(r + dr, c + dc, clue, color="firefly"))

        solver.add_program_line(f"dead_end({r}, {c}).")
        solver.add_program_line(f'grid_out({r}, {c}, "{dict_dir[style]}").')
        solver.add_program_line(f'{{ grid_in({r}, {c}, D) }} :- direction(D), D != "{dict_dir[style]}".')

    solver.add_program_line(display(item="edge_top", size=2))
    solver.add_program_line(display(item="edge_left", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Hotaru Beam",
    "category": "loop",
    "aliases": ["hotaru", "hotarubeam", "firefly"],
    "examples": [
        {
            "data": "m=edit&p=7VbNbts8ELz7KQyeWoAH/VC/tzR1e3GVtkkRBIJhyI7SGLWhVLaKlIbfPcuh8okhEwTFhwY9BLIWq+HuckiOSW5/dlVbc1+oX5hyj/v0RImHVyQxXq9/zla7dZ2P+VG3u25acjg/KfhVtd7Wo1Il0jMb7WWWyyMuP+YlCxjv3xmXX/K9/JTLgstTamIUy+WUPJ/xgNzJ4J6jXXnHGvQ98gvtx+RekLtctct1PZ/qQp/zUp5xpvp5h2zlsk3zq2Y6Dd/LZrNYKWBR7Wgs2+vVTd+y7S6bH10f688OXB5pupNH6IYDXeVqusp7hK4axf+mW19+r28fY5rNDgea8a/EdZ6Xiva3wU0H9zTfky3yPQvjQOUSDU4FqF4YpwoIDSQRNpIiyUQy736yekR4oUJouQcksrKEn9lIYFcWAbLMOiEYCgMRyDJjInA2AD1Os3CCwibl1KGT+XZMlliFMyQNQORj4EaVKIgVEhlICHpG3UggxgAizKhZJgYZE0COZyAJQsyk9GFPtOw+Fv/iv8UPOLtatfXV+jfk2SuAwh+iUEFoo1CCsFGowY7VirDralXYHLQy7LpaHU4sFOL0BpU4vUEpTgWoxYnF7DgcIBsnFtJxYiEfJxYScvhCR3asFpODQlD2KLSobA5aWE4FqMuJhcJcVFWw+WqpORwgt4e9kdg+QHIB7BltQVyGsO9hPdgIdoqYCew57DGsgI0Rk6hN7I+2OVP1f4lOGSX6yHOeV7y/CpRsQgfXuGjaTbWm46voNou6vf+mq8JhxG4ZXpKbz8Xr7eHlbw9q9r1/7c/1DJ1STtWGxKOUcXnC2U03r+bLhjRGc/dM40QdeAHddukYfaI59XiYPZ39TPNTxV98DmmPut+Wx2+um13VduNFXW3estnoDg==",
        }
    ],
}
