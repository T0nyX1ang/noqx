"""The Kazunori Room solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import area, display, fill_num, grid
from noqx.rule.helper import fail_false, full_bfs, validate_type
from noqx.rule.neighbor import adjacent


def number_appear_twice() -> str:
    """Generate a constraint for a number appearing twice in an area."""
    return ":- area(A, _, _), number(_, _, N), #count { R, C : area(A, R, C), number(R, C, N) } > 2."


def avoid_2x2_number() -> str:
    """Generate a constraint for avoiding 2x2 number cells."""
    return ":- number(R, C, N), number(R + 1, C, N), number(R, C + 1, N), number(R + 1, C + 1, N)."


def area_num_adjacent(adj_type: int = 4) -> str:
    """Generate a constraint to ensure adjacent cells with the same number in an area."""
    return f":- area(A, R, C), number(R, C, N), #count {{ R1, C1: area(A, R1, C1), number(R1, C1, N), adj_{adj_type}(R, C, R1, C1) }} != 1."


class KazunoriSolver(Solver):
    """The Kazunori Room solver."""

    name = "Kazunori"
    category = "num"
    aliases = ["kazunoriroom"]
    examples = [
        {
            "data": "m=edit&p=7VVPT9tOEL3nU6A9z2H/edf2jVJ+vVC3/UGFkGVFIbglaqLQhFSVo3x33uyuGzCqEKqgl8ry7PN4dvbN8+x6/X0zWbWUkyeTkySFy1hNRlqyToVbputsdjtvywM63NxeL1cARB8q+jKZr9tRnYKa0bYryu6QundlLZQgoXEr0VD3qdx278uuou4UrwQp+E5ikAY83sPz8J7RUXQqCVwBO0EO8AJwOltN5+34JCb6WNbdGQle502YzVAslj9akXjw83S5uJyx43Jyi1rW17Ob9Ga9uVp+26RY1eyoO/w9XbOnyzDSZTSkm+p5YbpFs9tB9v9BeFzWzP3zHuZ7eFpuYatyK4zUPNdCTYKmSGhU9siTP/IUQ492Q48xQ49VQ0/22DNc3WZy6HFDztYP81j/kA/KVaHoi2D/C1YHewZNqDPBvg1WBpsFexJijiGVcgUpDzIabZzlD3EGQQJGjEt+C3+PPTZUDtqMc02qsBEXlrQEVWCMpFlqxioHjjkxkjYosJ+bQ9iADfJArpAnA455MAL7hD3ypzwSOe9jHblhBI75MWKtmB+x4JBiFMdE/hiBU4w2wLEWjMA9H+afagdWRdKnQE6ZckrklH1dzDnWrrxFjakWh3p90oqxS7U71O6SP2N/wjzXJw4emnAbBIz8PmmSI6bXyrOe/Vxeq8+P4+8XxrdziSf7uf00muI8tMZRsDZYF1rG8yZ73jaMu4cPiXBE/nm3Pkmv1lDkwQW1XvK5GdXi+Opre1AtV4vJHMdXtVlctqv+Gf+L3Uj8FOGu8XnJ/vuF/KVfCH8C+awOfoWOfYJODXXR0/d2EYmbzXgyni7RbLJ5dbrYY83oDg==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(number_appear_twice())
        self.add_program_line(avoid_2x2_number())
        self.add_program_line(area_num_adjacent(adj_type=4))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            fail_false(len(ar) % 2 == 0, f"Area {i} must have an even number of cells.")
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(fill_num(_range=range(1, len(ar) // 2 + 1), _type="area", _id=i))

        for (r, c, d, label), num in puzzle.text.items():
            validate_type(label, "normal")

            if d == Direction.CENTER:
                fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
                self.add_program_line(f"number({r}, {c}, {num}).")

            if d == Direction.TOP and r > 0 and isinstance(num, int):
                self.add_program_line(f":- number({r}, {c}, N), number({r - 1}, {c}, N1), N + N1 != {num}.")

            if d == Direction.LEFT and c > 0 and isinstance(num, int):
                self.add_program_line(f":- number({r}, {c}, N), number({r}, {c - 1}, N1), N + N1 != {num}.")

        self.add_program_line(display(item="number", size=3))

        return self.program
