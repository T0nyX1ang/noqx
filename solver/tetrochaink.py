"""The Tetro Chain-K solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false
from noqx.rule.neighbor import adjacent, count_covering
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, avoid_same_omino_adjacent, general_shape


class TetroChainKSolver(Solver):
    """The Tetro Chain-K solver."""

    name = "Tetro Chain-K"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZtb+JGEP7Or6j2661U7/olxlI/EI5c75oQcoAoWBYyxATn7Dg1Nrka8d9vZm2EX9aoqnpqK52Mh+GZYd52/ax3f6Ru7FGm4Ec1KXzDpTFT3Nw0xK0U18RPAs/6ifbSZBvFoFB6P6QbN9h59NN8e9uPem/ve7/vzWSxYB+U9KMye755fvc5/O2jr8bsZmiO7kZ3Pn/q/dq/fjAG74xRupsm3v4hZNfP08VkM5o9dfmfg+FCyxb3iv5psfl535v+0rGLEpzOIetaWY9mHyybMEIJh5sRh2YP1iG7s7I5zcZgIpQ5lIRpkPjrKIhicsKy2/yPHNTBWZ0JO2r9HGQK6MNCB3UO6tqP14G3HI9zz5FlZxNKMPm1+DuqJIz2HmbD4vD3OgpXPgIrN4Hx7bb+K6EqGHbpY/QlLVyZc6RZL29hfGrBvNwCBDm1gGreAmqSFrDeUgu3/3wHXed4hNX5DD0sLRvbmZ5V86yOrQPIoZBMyLl1IIYOYTjkqoyYMJUBzho454bUn6sa4HoT11riaFdyXEdcEkfvyvErjC+p50qVxzfbcHl8VVGk/irDfiW4xqVxdAXnJsPl/eoivgzH9Wrm1Vvmr6voL8Hb6tRwPs15Ggzn08xrcJx/M47BMY4Ml9dvGC1xDNl8YO/eiB3MhZzABqeZKuR7IRUhdSFvhc9AyJmQfSE1IQ3hc4WPyF98iGBPEMvELUAs3nyivlNttpofEdVL//9hTscm4zTeuGsPaG68dV89AqcL2UXBcpfjS++ru06IlR9wZQuxkjgtoJc0XHlAziWvIIpeA/9FFuBkqoD+00sUe1ITgt7jU1soNElCraL4sVbTmxsE1VbE0V+B8s1dgZIYmL/0243j6K2ChG6yrQClU6ISyXupzTJxqyW6X9xatvA8jmOHfCXitlXKcf1+vAn8l98EcKWUv/8+IA7I7L5g9lwRyL/DuTYsBTAf1vGaLt0lLIOYmxSHgVz0Zy3+dVwrcF7D9RZ/I8c1oyVvPU6Rt+GvOa3r8r2mL572KL7AvGdjHZYQMKAXOLhkleEtdFuy1vEGt2KxTXoFVMKwgNZJFqAmzwLYoFrAWtgWo9YJF6uqcy6matAupiozr+10vgE=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="gray", adj_type=8, grid_size=(puzzle.row, puzzle.col)))

        self.add_program_line(all_shapes("omino_4", color="gray"))
        self.add_program_line(avoid_same_omino_adjacent(4, color="gray", adj_type=4))
        for i, o_shape in enumerate(OMINOES[4].values()):
            self.add_program_line(general_shape("omino_4", i, o_shape, color="gray", _type="grid", adj_type=4))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(
                not (d == Direction.CENTER and symbol_name == "circle_SS__5"),
                f"Gray circle cannot be placed in the center of ({r}, {c}).",
            )
            target = 2 if d == Direction.TOP_LEFT else 1

            if d == Direction.CENTER and symbol_name == "circle_SS__1":
                self.add_program_line(f"not gray({r}, {c}).")

            if d == Direction.CENTER and symbol_name == "circle_SS__2":
                self.add_program_line(f"gray({r}, {c}).")

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__1":
                self.add_program_line(count_covering(("lt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__2":
                self.add_program_line(count_covering(("gt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__5":
                self.add_program_line(count_covering(target, (r, c), d, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
