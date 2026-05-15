"""The Fillmat solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, avoid_edge_crossover, general_shape


class FillmatSolver(Solver):
    """The Fillmat solver."""

    name = "Fillmat"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VRNT+MwEL3nV6A5zyG20zT1ZVWg5VLKshQhFEVVWgJUtAokzQq5yn/f8aQ0G6ml4kOglVaup2/meeTnicf5UxFnCQrX/lSA9E/DEwFPGfg83fUYzZbzRB9gt1jepxkBxLN+H2/jeZ444XpV5KxMR5sumhMdggTkKSBCc65X5lSbIZoLogAFxQaEBKAk2KvhFfMWHVVB4RIerjHBa4LTWTadJ+NBFfmpQzNCsPsccraFsEh/J1ClsT9NF5OZDUziJR0mv589rpm8uEkfCnjZokTTreT2tshVtVy1kau2y5WfITe5uUvyYrJNaycqS6r5L1I71qEVflnDoIYXelVaUStQrk39QUKqDwNKUEDUbodcuXF9j1y1cYWUjdVCBk3ea6aLVrvp+6K53m/9xZNEwUKv2fbZSrYjOgcaxfaYrcu2xXbAa3psr9gesfXY+rymbSvxplp9XA54tl6dgPpASJTSB632SgxV1YnN0fr3YpETQo/u7sEwzRbxnO7vsFhMkuzFp9eidOAZePKl8P4/IN/xgNj6u1/cGh/t1JBKu+kqNGcIj8U4Hk9TumdUP0tT820ngHIor70jj+g20cFOWniv0wppyXuz9+2tXlW+h95z7l3Kv/zb0ysYOX8A",
        },
        {
            "url": "https://puzz.link/p?fillmat/21/12/1b3e2d4d2h1i2d21p12b4z3b3e4j2m3e4b2e2d3c3c2b4h2b1g2d4n3h3b2o3b4d3c1e1a2f",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(general_shape("fillmat", 1, OMINOES[1]["."], color="grid", adj_type="edge"))
        self.add_program_line(general_shape("fillmat", 2, OMINOES[2]["I"], color="grid", adj_type="edge"))
        self.add_program_line(general_shape("fillmat", 3, OMINOES[3]["I"], color="grid", adj_type="edge"))
        self.add_program_line(general_shape("fillmat", 4, OMINOES[4]["I"], color="grid", adj_type="edge"))
        self.add_program_line(all_shapes("fillmat", color="grid"))
        self.add_program_line(avoid_edge_crossover())

        tag_be = tag_encode("belong_to_shape", "fillmat", "grid")
        self.add_program_line(
            f":- grid(R, C), grid(R1, C1), adj_4(R, C, R1, C1), not adj_edge(R, C, R1, C1), {tag_be}(R, C, N, _), {tag_be}(R1, C1, N, _)."
        )
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(f":- not {tag_be}({r}, {c}, {num}, _).")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
