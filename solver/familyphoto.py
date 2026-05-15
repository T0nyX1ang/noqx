"""The Family Photo solver."""

from typing import List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region, count_rect


def count_family_photo_size(num: int, src_cell: Tuple[int, int], adj_type: Union[int, str] = "edge") -> str:
    """Count the size of a family photo region."""
    src_r, src_c = src_cell
    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, None)
    return f":- #count {{ (R, C): black(R, C), {tag}({src_r}, {src_c}, {src_r}, C), {tag}({src_r}, {src_c}, R, {src_c}) }} != {num}."


class FamilyPhotoSolver(Solver):
    """The Family Photo solver."""

    name = "Family Photo"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VRLi9swEL7nVyxznoMl+X0p6TbpJZttmyzLYkxwsm5jauPUiUtRyH/vaOysWxC020fooQgNnz6NHt9oNPtPbdbkGFJTITooqClXcpdOxN3p27I4lHl8heP2sK0bAoi30ym+z8p9jqOkd0tHRx3Feoz6dZyABOQuIEX9Nj7qm1jPUS9oClCkCFVbHopNXdYNnDk9IyQAJcHJAO953qDrjhQO4XmPCT4Q3BTNpsxXs455Eyd6iWDOfsmrDYSq/pxDt4zHm7paF4ZYZwdSuN8WO0BFE/v2sf7YwvmEE+pxp2DykwrUoEA9KVB2BfKvK4jS04ke5x1pWMWJkXM3wHCAi/h4Mtc6gvTNUgUYdC8InjCES3frCd8zhAfo9kSkDPFiIIRwe5duDW0t+ICH8wESz6JvuojK6Du2CwUox8oqG+tafT0761pZz8b6djawslYVgXWHwLeyoY0Nrb6RNQ6RdYfIejMhrFsIYTmPnm/KjyjZLilxUCu2r9g6bD22M/aZsL1ne83WZeuzT2BS71nJ+W0e/dp1wPUoPFFIGv0IRUDZoX54xUT6XCSH5l12nI4SmDx+yK/mdVNlJVWAeVut82YYL7bZLgeqw6cRfAHuiUL5vzT/46XZPJRz4T/wu18yoYA/fR/Utwi7dpWtKOZA+YZm2g2c50544R+YuHikqDiko68=",
        },
        {
            "data": "m=edit&p=7VVLj5swEL7nV6zm7IMfYB63dJv0kqaPZLVaIbQiWdqggtiSUFWO+O+1h6Rs0Fz2sFIqVY4nH5+H8Xy2B+9/tlmTM8HdT4XM/tvmiRC7DDV2fmrr4lDm8Q2btodd3VjA2Kf5nH3Lyn3OJsnJLZ0cTRSbKTMf4gQkMOwCUma+xEfzMTYzZlZ2CJhIGVRteSi2dVk3cObMwiIBTFo4G+A9jjt025OCW7w8YQsfLNwWzbbMHxc98zlOzJqBm/sdvu0gVPWvHPrX8HlbV5vCEZvsYBXud8UzMGUH9u1T/aOF8wwdM9PXKVCDAvVXgaIVyDdXEKVdZzfnq9XwGCdOzt0AwwGu4mPn0jqCUtDvoeh3EDzfEWogdHBenhMRyDERjYgwGgUVXDvGe8EIPfaRauwjw1EuwudjRsuLOFaWQHEPTpzzluxywUH5JBuQbESxPhnXlxSrBcmSvoFHsmRmYUixETlbRMaNyHUQnBQnOBlZcDK04GTOQpBJC0nHxrNJ0PSUHu3t0Sp9TdN0gppeE03EtkdvjgdQol3bgmNGoX2PlqP10S7QZ4b2Hu0tWg+tRp/AleyrivplDbxROonqL5LL5v97XDpJYPb0Pb9Z1k2VlfZru2yrTd4Mz6td9pyDvfO6CfwG7Ili8v81eOXXoNsofm11c23p2EpOJ38A",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(count_rect(len(puzzle.text)))

        for (r, c, d, label), _ in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"black({r}, {c}).")

            if (r + 1, c, d, label) in puzzle.symbol:
                self.add_program_line(f':- edge({r + 1}, {c}, "{Direction.TOP}").')

            if (r, c + 1, d, label) in puzzle.symbol:
                self.add_program_line(f':- edge({r}, {c + 1}, "{Direction.LEFT}").')

        all_src: List[Tuple[int, int]] = []
        tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_family_photo_size(num, (r, c), adj_type="edge"))

            all_src.append((r, c))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
