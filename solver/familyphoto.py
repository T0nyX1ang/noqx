"""The Family Photo solver."""

from typing import Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, grid_src_color_connected
from noqx.rule.shape import all_rect_region


def count_family_photo_size(num: int, src_cell: Tuple[int, int], adj_type: Union[int, str] = "edge") -> str:
    """Count the size of a family photo region."""
    src_r, src_c = src_cell
    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, None)
    return f":- #count {{ (R, C): black(R, C), {tag}({src_r}, {src_c}, R, C) }} != {num}."


class FamilyPhotoSolver(Solver):
    """The Family Photo solver."""

    name = "Family Photo"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7ZXtb6JOEMff+1c0+7ab/FgeFEguF2u1155a22q8SoxBi0oLrodgexj/984ueghse7/eQ3MvLoTN8JlldmZ2+bL6GtmBg3W4FB1LmMClqDK/Zcngt7S7um7oOeYRrkbhnAZgYHzZaOCp7a0cfHE7b9Zo9fG0+mWth4MBOZOic6l/37g/vvY/n7tKQBptvdPqtFx5Vv1UO7kq14/LnWjVC531lU9O7nuD7rTTnxnyt3p7oMaDS0m7GEz/W1d7H0rWLodhaRMbZlzF8ZlpIRlhfhM0xPGVuYlbZtzG8Q24ECZDjPzIC90J9WiA9ixugkUQlsGsp2af+5lVSyCRwG4ntgrmLZgTN5h4zqiZBOqYVtzFiK19wt9mJvLp2mGLwWv8eUL9scvA2A6hfau5u0RYAccquqMP0W4qGW5xXE0qqP/PCiDIvgJmJhUwS1ABK+zPVmAMt1vYnGuoYWRarJxeauqpeWNuYGybGySX2asKwpVkB5FGGFAhtx0oawxosAE7YCgMfEwBIepuSvIOhCZ8gdv9AjIUkBTdSjoqGxmatAIpkpCy9QpUFc7VxJTlV6SssALl5RZpRUiFVVSEESrZPuypLqK6cC7ve5EKIxjCzAgRhiBEsB5sX4NvoszHLhwcHCt8POWjxEeNj00+p87HPh9rfFT5WOZzKuzovelwHp6jn0sHqRq0x9ChxrKBSQVOh/LDFC25zBU4vbT3fR6WLFS/mzlHbRr4tgcK0I78sROkzzdze+kg0GG0ot5oFQVTe+KMnCd7EiIz+RUcejJswWNlkEfp0nMXogh7Vwa6swUNHKGLQQdyfyEUcwlCjWlwl8vp0fa8bC38J5lByXnNoDAAlTx4toOAPmaIb4fzDDhQ1EwkZ5FrZmhnU7Qf7NxqftqObQk9IX5bCpb//TT/8p8m2yjpndXpV8XSgoZ/FzYcX2K0jEb2CHqO4Lxh5lYr0lsdmv4bHO/eKf750eAVLUydeSxQRKCviOKBV8Rf0L8Db54XxI4lW9Q7oALJA5pXPUBF4QNY0D5gL8gfi5pXQJZVXgTZUgUdZEsdSqE1LD0D",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(f":- {{ upleft(R, C) }} != {len(puzzle.text)}.")

        for (r, c, d, label), _ in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"black({r}, {c}).")

            if (r + 1, c, d, label) in puzzle.symbol:
                self.add_program_line(f":- edge_top({r + 1}, {c}).")

            if (r, c + 1, d, label) in puzzle.symbol:
                self.add_program_line(f":- edge_left({r}, {c + 1}).")

        all_src = []
        tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))
            self.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_family_photo_size(num, (r, c), adj_type="edge"))

            all_src.append((r, c))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
