"""The San-Anko solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Point, Puzzle
from noqx.rule.common import defined, display, fill_num, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, general_shape


def ensure_same_number_adjacent(adj_type: int = 4) -> str:
    """A rule to ensure two adjacent cells having the same number."""
    return f":- number(R, C, N), number(R1, C1, N1), adj_{adj_type}(R, C, R1, C1), N != N1."


class SanAnkoSolver(Solver):
    """The San-Anko solver."""

    name = "San-Anko"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VffT9swEH7vX4H87Ic4TpOQN8ZgLyxslAmhqKpCF0S1VmFpM6FU/O/cnc9rYtOxSfshpCmN7Xzf9erP39Vu11/bsqmkCvClUwk9XJFK6Q7TmO6Ar8vFZlllB/Ko3dzVDQykPD89lbflcl3JUcFh09G2O8y6I9m9ywqhhBQh3EpMZfcx23bvs24iuwlQQkaAnZmgEIYnu+EV8Tg6NqAKYJybcSTFBaa7hsf5opkvq9kZRADyISu6SymQfEMZcChW9bdK8FzweV6vbhYI3JQbULS+W9wzs24/119ajoWEYtUuN4t5vawbBBF7lN2RkZE/I0PvZODQyMDRMzLCnoz6YXbyByQcPi/hESy6ABGzrEA9n3bDdDecZFuhQ5HBamttuth0CXWJ4RLDJYZLDJcGplPUKRVxP+Y+5f7Q9KFJpUKTS42ZHzMfMx8jD1PLeWoFlhYSKBwnacvDADClQQTOuBBxD6CIqAfA9AcAKhgkpbkPQkjFEEEdg08mRQ5C7+pnRnU9BHSqbAvtNbWX4IrsNLVvqQ2oHVN7RjEn1F5Re0xtRG1MMQn6+pPO20UG42yt0iQj0tED0Joe0J+00Lh4IOZ7cQtaBtVHUrSgh/xGpYU229nwGr8+bDoqxKRtbst5BV/yvF3dVM1BXjercgnPk7vyvhKw6z6OxIOgu9Bgh/6/Eb+CjRjtCn7pS/lv9oUCikWHsjuX4r6dlTPQQWVBuHZwWGfCYwcHfwhPHHxs8MTNHzPu5k8Yd/OnjLv5YfURTwMHxyIgQrkEFAAScHK5DGuGs8xlWDWcEC7DuuGkcBlWDiegy7B2OEtchtXDmeIyrB/OFpfhFYCT1LWQlwBOH5fhNfBd32d7uM/3cJ/xIev3nAlZvudMaL33UlnzvQ9n7V4VaZbulZ3e677e67627nuuaOu+54q27nuuaOu+54q27ntVpq37XpVp675XZZF136uyiNYgh9nLwXm/i6C35jJKXwgAcT8KgKpwPbZl5HmP+LWPUx7A3SJ6AfecYhz+8bj4X9mA4RfLdPQE",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(fill_num(_range=range(1, 4), color="not black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(ensure_same_number_adjacent(adj_type=4))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(all_shapes("omino_3", color="black"))

        for i, o_shape in enumerate(OMINOES[3].values()):
            self.add_program_line(general_shape("omino_3", i, o_shape, color="black", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")

            if Point(r, c) in puzzle.surface:
                self.add_program_line(f":- #sum {{ N, R, C: number(R, C, N), |{r} - R| + |{c} - C| = 1 }} != {num}.")
            else:
                self.add_program_line(f"number({r}, {c}, {num}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "ox_E__1":
                self.add_program_line(f"black({r}, {c}).")
            if symbol_name in ("ox_E__4", "ox_E__7"):
                self.add_program_line(f"not black({r}, {c}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
