"""The Regional Yajilin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, direction, display, fill_line, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected


class YajilinRegionsSolver(Solver):
    """The Regional Yajilin solver."""

    name = "Regional Yajilin"
    category = "loop"
    aliases = ["yajilin-regions", "yajirin-regions", "regionalyajilin"]
    examples = [
        {
            "data": "m=edit&p=7VdtT+M4F/3Or0D+OpYmiZ3EiTRalbeRUOnAAstCharQBhpIGyZtgQ3iv8+xfbtt2pTdHaTV80irtu7JdY7vuUnviTv5PkvKlLuOfgvF8Y2XdJX5eCowH4deZ9k0T+Nt3ppNh0UJwPm3gwN+m+STlB9e3u/sPbSe91u/f/avhDjv3H663zs5vx9c/OaeONnn0unkanx0vLeTf/paXR0NW0/pfhocT4r+ME+TQVJdXRy+5OMDdTe8dXcPh7vqNhk7k+/qLHraOfnyZatLQq63Xqsorlq8+hp3mce4+bjsmlcn8Wt1FFcdXp1iinGJWBvIZdwD3F/ACzOv0a4Nug5wB1gAA14C9rOyn6e9to0cx93qjDOdZ8ewNWSj4illdglz3C9GN5kO3CRTXK/JMHukmclsUDzM6FwsyEazfJr1i7wodVDH3njVsiW0G0oQixI0tCVo1FCCruzDJeTZOH1pUh81q3/DnfkV+ntxV5dyvoBqAU/jV4wdM7rxK4sciQWkuSKRo/Riv9jrE7kejgThYIE9B9gjrNnzuGbjJ6yxWOIKzaXzpebqc5D+0og4MKNnxjNo5JUw454ZHTP6Zmybc/Yh2nM97nlY1sOvzxXAIWEJDBkG+8ARYfSSQGqDQ2CXMPpMSzU4AhYWew4wSjMYXC3bYHAlcT1wJXE9cCVxBbiSuMIF9glDsyTNApolaRbQLEmzBNcnrgTXJ64E1yeuBNcnrgTXn3NRr0/1SmgOSLOE5oA0S2gOSLMPbkBcH9yAuD64IXF9cEPi+uCGcy7qDaneAJpD0hxAc0iaA2gOSXOg/Yy4AbiKuCG4irghuIq4IbiKuCHqVVRvCM2KNIfQrEhzCM0RaVbgRsRV4EbEVeBGxFXgRsSFxwpnzg2BqV6lgEmzioBJcwSz1k1jMLgucSNwXeJG4Or2MRhc13KRB9hykQfY1os8wFYz8gBbzcgDbDUjDxe63QwG1yMuekFQLyAPMHHRC4J6AXmAbb3IwwX1AvIAW83IA2w1Iw8wcT1wBXHRC4J6AXmAiYteENQLyANM9aIXBPUC8gCTZvSCoF5AHi584gpwfeKiFwT1AvIAExe9IKgXkAeY6kUvCOoF5AEmzegFMe8F3N8/fz+4j16k9cNULoy17JpRmjEwlhNq0/ybtoq7xWK5bK4/53FMClSEXxBDRfqCCYN0aUDoQl2YsE74l9K7uAN6V1F/+f9/seutLjudlbdJP8UjsY1H43anKEdJjqPObHSTlvNjbFDYpMh7E3t2L31J+lMW243S8kwtNjZr1EJ5UTzqZ3DDCvOpWjC7Gxdl2jilg+ngbtNSeqphqZuiHKxoek7yvF6L2UTWQnbTUQtNS+wolo6Tsiyea5FRMh3WAksbqNpK6XjlYk6TusTkIVnJNlpcjrct9sLMR+8OsL36bzf5P7ub1HfJ+Yk95Ue2dh/14m51iqczr75x9jjrJT3UxPCfhb8Xh7n+o3jzOu25X2+ehIVvmLSu3jyJx8HaxL9+1U0fF+U7prqYXA03WCui77jr0mxTfIORLs2uxtdcU4tdN05EG7wT0VX7RGjdQRFcM1HENvioXnXVSrWqVTfVqdYMVada9tQuK9O7rBgn+fYfyX2GC8eut34A",
        },
        {
            "url": "https://puzz.link/p?yajilin-regions/11/18/c6c69alhlhg1lhhh4h91gdict8jomt4aemu3001i3tk00uuff1g3vovve81oiu2k1sfvmrto68g2g22g222g222111111111g11g11111h",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line(shade_cc(colors=["black", "white"]))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))
        self.add_program_line(grid_color_connected(color="white", adj_type="loop"))
        self.add_program_line(single_loop(color="white"))

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

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
