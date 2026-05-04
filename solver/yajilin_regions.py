"""The Regional Yajilin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route


class YajilinRegionsSolver(Solver):
    """The Regional Yajilin solver."""

    name = "Regional Yajilin"
    category = "route"
    aliases = ["yajilin-regions", "yajirin-regions", "regionalyajilin"]
    examples = [
        {
            "data": "m=edit&p=7Zbdb9MwFMXf+1cgP/sh9rVjOy9ojI2XMj42hFBVTV0poqKj0LUIper/zrFzSocoXxtCIKEu3omdX3yuk3udq/er0WKiTZX/JGr8x8+ZWA4b63JU/J1Nl7NJc0cfrJav5wsIrR8dH+tXo9nVRPcGvGzYW7epaQ90+6AZKKt0OYwa6vZJs24fNu2Jbk8xpLRDXx/KKG0hj3byeRnP6rDrNBX0CbRAQ76AHE8X49nkvN/1PG4G7ZlWeZ57hc5SXc4/TFR3i3I+nl9eTHPHxWiJaK5eT99x5Gr1cv5mxWtNRlez5XQ8n80XqtzPDDe6PehC6O8JQXYhyOcQZH8I9neEMJu+nXzc5z7td7/Bk3kK/+fNIIfybCfjTp426022mVvTrFWqHG7gyoqkKuab3e3WJxmLM6Gud9pW0JbaXevPtOm0XGOl3l3vKl6zyQuUTRyX1pb2DB51K6W9X9qqtL60/XLNEUxbY7W1uK3F22cEOlA76EjtoRM13nSpqAO0oUYWZKtFJ2jptK2gHTVYR9aCdWQtWEfWgnVkBawjKwbaU8Ozo2eBZ0fPAs+Onh1YT9aB9WQdWE/WgfVkHVi/ZRGvZ7wOnmt6dvBc07OD55qePdiarAdbk/VgA1kPNpD1YMOWRbyB8dbwHOi5hudAzzU8B3quc7UhW4ONZAPYSDaAjWSDzZWJGvFGxhvgOdJzgOdIzwGeEz1HsIlsBJvIRrCJbASbyKICSrVlAzTjjRGanmOCpueEUlrRcwJryCawhmwCa8gmsKZjMQ+0ozbQntpC19QCHagddOdZcgm3ZA1YSxa5IMwFzANNFrkgdst66EQNz8wFzANtqOGZuYB5oMlasEIWuSDMBcwDTRa5IG7LIl7mAuaBpmfkgjAXMA80PWNfEk9WwHqyyAVhLmAeaLLIBWEuYB5oxotcEOYC5oGmZ+SC1Lvn+/n9wXO0Kfvf5GKeS8thaV1p61JyQi6aP1lWVV5Ud7243qzGKSeICG+QQkR5waSoHBoUsjAHJl0l/KH1gXR7/pc//+/1DXsDdbpavBqNJ9gS+9ga75zMF5ejGc5OVpcXk8X2HB8om576qMqR9yBs4v+/Wf7ab5b8lKobfLnc5gPithk/aE+xB+j2kVbvVuejc8Sk8GWsv9ePFP6l/v336W+rwrcHUSi+MdjVjv2DKDpfDfzxVUe9GvY+AQ==",
        },
        {
            "url": "https://puzz.link/p?yajilin-regions/11/18/c6c69alhlhg1lhhh4h91gdict8jomt4aemu3001i3tk00uuff1g3vovve81oiu2k1sfvmrto68g2g22g222g222111111111g11g11111h",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(fill_line(color="not black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))
        self.add_program_line(grid_color_connected(color="not black", adj_type="line"))
        self.add_program_line(single_route(color="not black"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))

            if rc:
                num = puzzle.text[Point(*rc, Direction.CENTER, f"corner_{Direction.TOP_LEFT}")]
                if isinstance(num, int):
                    self.add_program_line(count(num, color="black", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"black({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
