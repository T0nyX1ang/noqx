"""The Border Block solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


def border_block_constraint() -> str:
    """Generate a border block constraint."""
    mutual = "edge_left(R, C); edge_left(R - 1, C); edge_top(R, C); edge_top(R, C - 1)"
    rule = f":- ndot(R, C), {{ {mutual} }} = 1.\n"
    rule += f":- ndot(R, C), {{ {mutual} }} > 2.\n"  # 0 or 2 connected edges
    rule += f":- dot(R, C), {{ {mutual} }} < 3.\n"
    return rule.strip()


class BorderBlockSolver(Solver):
    """The Border Block solver."""

    name = "Border Block"
    category = "region"
    aliases = ["borderblock"]
    examples = [
        {
            "data": "m=edit&p=7ZVvb+I4EIff8ykqv62ljRMIIdJpRSnttktTWkBsiRAKNEDaBHMhod0gvntnHGj+EHq3d6fqTjpBzOQZZzwzNr+sfg8t36ZMwq+iUfiFT5lp4pI1VVzS7tN1AtfWT2g9DObcB4PSW4NOLXdl0+uHeavB6y/n9R9rLRgM2KUUXkn9p4un03vv+5Wj+OzC0No37RtHntW/Nc7u1Oap2g5XvcBe33ns7Kk36E7b/VlN/tk0BuVocCtVrgfTL+t677eSuUthWNpENT2q0+hSN4lMqLgYGdLoTt9EN3pk0KgDLkLZkBIvdANnwl3ukz2LWmAxQmUwm4nZF360GjFkEtjGzgbzAcyJ409ce9TpxKitm1GXElz8TDyOJvH42sbV4DlxP+He2EEwtgJo32ruLAlVwLEKH/lzuJvKhlsa1eMSmn+yBAiyLwHNuAS0CkrAylIltP75CmrD7RZ25x5qGOkmltNLTC0xO/oGRkPfEIXti4+3kJRVBLCj70DLzVDLCJQEVBUE5RSo5B6pVhFUElCTEKgJYJIgqSCMiYdSURir5XJjsoykmiKKWDu1FCuL9L6miZjzTqAVTDTkARoiKzhdho5nDhpwXLyAV7A/RfzI/CqmXMQxqQKuHZmvHclTOxKnhjt9yBWpKA4040K0RBZjF44NjRQxnotREmNFjC0xpynGvhgbYiyLURVzqnjwfulopnflr6VDVAZ7U9NEE0FEoVDlD1M0lVh/s5/Kf48NSyZpPs7sE4P7nuWCjhihN7b95L4zt5Y2ATknK+6OVqE/tSb2yH61JgHR4zdK2pNhCxErg1zOl66zKIqwd2WgM1tw3y50IbQh9yOh0FUQasz9x1xOL5brZmsRL9sMig9+BgU+aG3q3vJ9/pIhnhXMMyCly5lI9iLXzMDKpmg9W7nVvKQd2xJ5JeIyFSr//+79t797caekT5a5v6u6JjQclJJGt5Qsw5E1gm4TOGoUHe/SeeD+9CrEf4P7HwhV4szjArkC+oFipbxF/Ig4pbx5fqBEmOyhGAEt0COgeUkCdKhKAA+ECdgRbcKoeXnCrPIKhUsdiBQuldYpc1h6Aw==",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="dot"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(f"vertex(0..{puzzle.row}, 0..{puzzle.col}).")
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))
        self.add_program_line("ndot(R, C) :- vertex(R, C), not dot(R, C).")
        self.add_program_line(border_block_constraint())

        for (r, c, d, _), _ in puzzle.symbol.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            self.add_program_line(f"dot({r}, {c}).")

        tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
        for (r, c, d, pos), letter in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            if letter != "?":
                self.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))

            for (r1, c1, _, _), letter1 in puzzle.text.items():
                if (r1, c1) == (r, c) or letter == "?" or letter1 == "?":
                    continue
                if letter1 == letter:
                    self.add_program_line(f":- not {tag}({r}, {c}, {r1}, {c1}).")
                else:
                    self.add_program_line(f":- {tag}({r}, {c}, {r1}, {c1}).")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
