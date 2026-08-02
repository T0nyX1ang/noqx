"""The Yajitatami solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, count_reachable_src
from noqx.rule.shape import all_rect_region, avoid_edge_crossover


def yaji_region_count(target: int, src_cell: Tuple[int, int], arrow_direction: str) -> str:
    """Generates a constraint for counting the number of {color} cells in a row / col."""
    src_r, src_c = src_cell
    rule = ""

    if arrow_direction == Direction.LEFT:
        rule += f':- not edge({src_r}, {src_c}, "{Direction.LEFT}").\n'
        rule += f':- #count {{ C1 : edge({src_r}, C1, "{Direction.LEFT}"), C1 <= {src_c} }} != {target}.'

    if arrow_direction == Direction.RIGHT:
        rule += f':- not edge({src_r}, {src_c + 1}, "{Direction.LEFT}").\n'
        rule += f':- #count {{ C1 : edge({src_r}, C1, "{Direction.LEFT}"), C1 > {src_c} }} != {target}.'

    if arrow_direction == Direction.TOP:
        rule += f':- not edge({src_r}, {src_c}, "{Direction.TOP}").\n'
        rule += f':- #count {{ R1 : edge(R1, {src_c}, "{Direction.TOP}"), R1 <= {src_r} }} != {target}.'

    if arrow_direction == Direction.BOTTOM:
        rule += f':- not edge({src_r + 1}, {src_c}, "{Direction.TOP}").\n'
        rule += f':- #count {{ R1 : edge(R1, {src_c}, "{Direction.TOP}"), R1 > {src_r} }} != {target}.'
    return rule


def rect_constraint() -> str:
    """Generate a cell relevant constraint for rectangles with the width/height of 1."""

    rule = f':- rect(R, C, "{Direction.TOP_LEFT}"), rect(R + 1, C, "{Direction.LEFT}"), rect(R, C + 1, "{Direction.TOP}").\n'
    rule += f':- grid(R, C), rect(R, C, "{Direction.TOP_LEFT}"), #count {{ R1, C1: adj_edge(R, C, R1, C1) }} = 0.'
    return rule


class YajitatamiSolver(Solver):
    """The Yajitatami solver."""

    name = "Yajitatami"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VXNbxo/EL3zV0Q+z8EfC/txqWgKvaSkv4QqilYIAdk2qIs2XdiqWpT/PW/G5kcKkdJDi1Spsjx+fh7G88b2sv7WzOqCEjSXkCaD5iIr3epUug5tvNyURXZG/WZzX9UARJfDIX2eleuCOnlwm3S2bZq1fWrfZ7myiqQbNaH2v2zbfsjaEbXXWFLkwF0AGUUWcLCHN7LO6NyTRgOPfEBD6orD3WK6WNaLsphegAXzMcvbMSlefCsRGKpV9b1QPozMF9VqvmRiPttA0fp++RBW1s1d9bUJvgioVk25WS6qsqqZZO6R2r6XMdjJ4J2DDFYUZDD0Mhi9IIPV/WEJ6csSHnFEVxAxzXLW82kPkz28zrYqsipzpCInQzeWoZfKkHrS6C5G+I/gb+GRKzf1h2Q5Hwe3XL15TnW193J7qocgBz+Me0decQj/nEo8pfdUcpxEipQPKKOhjTk+lR1nQhr/c9Blsi3srdihWCt2jDJR68S+E6vFdsVeiM8ANTGxI5MgsMUGSRcYwgT3gJEr45j5HY4I84Dx2zgK/gl8ICRgq1FGYIxkDcQwNni1BhVnbCOy1scR7Py+GMlGKBvjCHEijolkbyTlc7GRJI5EOFkuBW+ijcccwCFZA8eeqI35yvzipfJX5TcU1hkUJk2OMz9IK7co9E8NxT7lfNLJ1eDuS3E2qurVrMRDHTWreVHv5vhiPnbUDyU9x4lT9O8j+hd8RPm49Ilv/au3/ZV0clQcD4faS1IPzXQ2hSiFP+2Tp4l3Oek8AQ==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(rect_constraint())
        self.add_program_line(avoid_edge_crossover())

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

            if isinstance(clue, int) and label.startswith("arrow"):
                arrow_direction = label.split("_")[1]
                self.add_program_line(count_reachable_src(clue, (r, c), main_type="bulb", color=None, adj_type="edge"))
                self.add_program_line(yaji_region_count(clue + 1, (r, c), arrow_direction))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
