"""The Snake solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import count, display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route
from noqx.rule.shape import avoid_rect
from noqx.rule.variety import nori_adjacent


def exclude_checkboard_shape(color: str = "black") -> str:
    """Exclude checkboard-shape shading."""
    rule = f":- {color}(R, C), not {color}(R, C + 1), not {color}(R + 1, C), {color}(R + 1, C + 1).\n"
    rule += f":- not {color}(R, C), {color}(R, C + 1), {color}(R + 1, C), not {color}(R + 1, C + 1)."
    return rule


class SnakeSolver(Solver):
    """The Snake solver."""

    name = "Snake"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VXPj9o8EL3zV6x89iG2E/LjUtHt0gvNtg2fVihCKKRZgTY0NCFVZcT/vjPjbMNuLPVbVeW0MhnNex7bz2N7aH60WV1w4eJPBdzhAprnO/S5/pg+p2vz7aEsois+aQ+bqgaH89vplN9nZVOMUhwJbTk66jDSE64/RikTjDMJn2BLrr9ER/0p0guuE+hiPABuZoIkuDe9e0f96F0bUjjgx50P7gLcfFvnZbGaGeZzlOo5Z7jOexqNLttVPwvW6UCcV7v1Fol1doDNNJvtvutp2m/VQ9vFiuWJ64mRm1jkql4uukYueha5uIu/l1vuK5vQcHk6QcK/gtRVlKLq/3o36N0kOoKNoyNTIQ59ByrMqTBXAOH1UAEMeugClD0cA4Tb8gQDgOo39JznEIPPl/JxMrwlBgqB8f1aYoz9/ezSwf4zrHDCJzGwH0G7WsCuPJ96nieZhbiXASsEpgAmeUGTeguNkwzpAFcc0NKRVlrao5V1Senaoz1vSMP+p5QFSXYOx821IvuBrEPWIzujmBuyd2SvybpkxxTj44X5n1eK0h7AuYIwae7X+an8I22p55tSM2hvfFeCU5a09X2WF1Az4na3LuqruKp3WQk42WT7gkGZPo3YL0YfvVn3rXJfvHJj8p1X1e8LvK8/yEkhr/AC9S1n+3aVrfIKbhVkDXnfs/MqfA0fI09/HFC7qfLbAl4OvHiaoBKx5nv2gI/pEQ==",
        },
        {"url": "https://puzz.link/p?snake/11/11/00000000000000000000000000000000000000000957664857598o9", "test": False},
        {
            "url": "https://puzz.link/p?snake/15/15/13a3b00000a3d3a00000a3a4a00030a3a3a10000d3aca03001a3a3a10039a3d3a00100j3a39zp",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(shade_c(color="dead_end", _from="gray"))
        self.add_program_line(count(2, color="dead_end"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(exclude_checkboard_shape(color="gray"))
        self.add_program_line(avoid_rect(2, 2, color="gray"))
        self.add_program_line(fill_line(color="gray"))
        self.add_program_line(single_route(color="gray", path=True))
        self.add_program_line(grid_color_connected(color="gray", adj_type="line"))
        self.add_program_line(nori_adjacent(("le", 2), color="gray", adj_type=4))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
                self.add_program_line(count(num, color="gray", _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
                self.add_program_line(count(num, color="gray", _type="row", _id=r))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_L__1":
                self.add_program_line(f"gray({r}, {c}).")
                self.add_program_line(f"not dead_end({r}, {c}).")
            if symbol_name == "circle_L__2":
                self.add_program_line(f"gray({r}, {c}).")
                self.add_program_line(f"dead_end({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
