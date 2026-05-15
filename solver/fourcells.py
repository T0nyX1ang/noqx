"""The FourCells solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape


class FourCellsSolver(Solver):
    """The FourCells solver."""

    name = "FourCells"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VXfb9owEH7nr6j8fA/+lZDkZWId7IWm22CqUBQhoNmKBgoDMk1G/O89X1LR2qkq1GmTpir49OU7X/zd2Zx3P6vZtgAR2p+KgIPAJ9QhjSCKafDmGS/3qyK5gF61vyu3CACuBwP4Nlvtik7WzMo7BxMnpgfmY5IxyYCGYDmYz8nBXCUmBTNCFwOB3BCRYCAR9k/whvwWXdak4IjTBiOcIFwst4tVMR3WzKckM2Ngdp33FG0hW5e/ClaH0fuiXM+XlpjP9pjM7m65aTy76rb8UTVzRX4E06vl9lvkqpNcC2u5FrXItVm8Xu5qU7YJjfPjEQv+BaVOk8yq/nqC0QmOkgPaNDkwHT/kWO8KC7RDhB4ROITgXZcR0mO8KKlcRocuE3CP8b7T9dbqenoib63I+04UeQwV590jJiY9Txj3O5K7UVK4UdKrj5SuZqnc3KV2s5DebkmvGrLrVlV6ucs6r0eM4u5airv1UV4WyttBFQiPebo6HkRBx3FCdkBWkh3jaQWjyH4gy8kGZIc0p0/2huwlWU02pDlde97P+ke8Xg6ebI2FiSNgWmvQ9g+kXtSYaUnd9vknePP/z/68k7H+7ffiIi2369kK23tarefF9uEdb9Jjh/1mNDKFIfrtcv3rl6stPj/vinUu0H/f7zIzAh2DuQa2qaaz6aLE04ZVfJ6fnMmnlq93pOn6bRNaAvunntnuFjJU53uwt7qeP9z0X94TbPF55x4=",
        },
        {"url": "https://puzz.link/p?fourcells/10/10/d3g1c3g1c3b1a3b1j3a13a3j1b1a3b1c3g1c3g1d", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row * puzzle.col % 4 == 0, "It's impossible to divide grid into regions of this size!")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))

        for i, o_shape in enumerate(OMINOES[4].values()):
            self.add_program_line(general_shape("omino_4", i, o_shape, color="grid", adj_type="edge"))

        self.add_program_line(all_shapes("omino_4", color="grid"))
        self.add_program_line(count_shape(target=puzzle.row * puzzle.col // 4, name="omino_4", color="grid"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent_edges(num, (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
