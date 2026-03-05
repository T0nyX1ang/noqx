"""The Hinge solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode
from noqx.rule.neighbor import adjacent, area_border


def hinge_symmetry(color: str = "black") -> str:
    """Generate the symmetry rule of Hinge."""
    rule = f'symmetry(R, C, R0, C0, "H") :- grid(R, C), {color}(R, C), {color}(R - 1, C), edge(R, C, {Direction.TOP}), symmetry_axis(R, C, R0, C0, "H").\n'
    rule += f'symmetry(R, C, R0, C0, "V") :- grid(R, C), {color}(R, C), {color}(R, C - 1), edge(R, C, {Direction.LEFT}), symmetry_axis(R, C, R0, C0, "V").\n'
    rule += f"symmetry(R, C, R0, C0, D) :- grid(R, C), {color}(R, C), adj_4(R, C, R1, C1), symmetry(R1, C1, R0, C0, D).\n"

    rule += f":- grid(R, C), {color}(R, C), symmetry(R, C, R0, C0, D0), symmetry(R, C, R1, C1, D1), (R0, C0, D0) != (R1, C1, D1).\n"
    rule += f":- grid(R, C), {color}(R, C), not symmetry(R, C, _, _, _).\n"

    rule += ':- symmetry(R, C, R0, C0, "H"), not symmetry(R0 * 2 - 1 - R, C, R0, C0, "H").\n'
    rule += ':- symmetry(R, C, R0, C0, "V"), not symmetry(R, C0 * 2 - 1 - C, R0, C0, "V").\n'
    return rule


def hinge_avoid_isolated_edge(rows: int, cols: int, color: str = "black", adj_type: int = 8) -> str:
    """A rule to avoid the region border not continuously separating a block."""
    tag = tag_encode("reachable", "border", "adj", adj_type, color)
    borders = [(r, c) for r in range(rows) for c in range(cols) if r in [0, rows - 1] or c in [0, cols - 1]]
    initial = "\n".join(f"{tag}({r}, {c}) :- {color}({r}, {c})." for r, c in borders)
    propagation = f"{tag}(R, C) :- {tag}(R1, C1), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    constraint = f":- grid(R, C), area_border(_, R, C, _), {color}(R, C), not {tag}(R, C)."
    return initial + "\n" + propagation + "\n" + constraint


class HingeSolver(Solver):
    """The Hinge solver."""

    name = "Hinge"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZZfbxJBFMXf+RTNPs/D/N8ZXkytrS+Vqq0xDSGEUmqJECoUY5bw3T0zHJgGNdUYa2IM7MzZ3y53ztw7O+zi03IwHwml0tcEIQWUsM7nQymdD8nPxfh+MmofiMPl/e1sDiHE2cmJuBlMFqNWl3f1WqsmtptD0bxsdytViUrjUFVPNG/aq+ZVuzkXzTkuVSKAnW5u0pDHRb7P15M62kAloTvUkJeQw/F8OBn1TzfkdbvbXIgqjfM8/zrJajr7PKroI50PZ9OrcQJXg3tMZnE7vuOVxfJ69nFZbYdYi+bwx3ZNsWt2ds337eo/bzf21muk/S0M99vd5P1dkaHI8/ZqnXytKqPTTy28bGpTmZCALsCqPeD1PrB5eFlIkImEB8An8KyAmIEvQMl6z4ky+yMrt+9W1ftmVO0S2ZnBPFWe7WVuT3Krc3uBZIjG5PZFbmVuXW5P8z3HyJGuldBpII01XGtoQ22gLbWFdtQO2lN76Jq6hg7UATpSR6FTypJ2UmjPON4VHsAjeXTCqA1HL4zecPTCWHIL7sgdeE1egwdX/Af6CUEYuZkXesQPjA9uyA24JbfgntyDc17ohYnk0QgrH3DOFz080E9IfhR12ns0tYZmnID4wVLbnX/00J7aQ9e7/OjI/EfkP9YlJ5ZjWYxlWVOLunhqr0u9LGrqWCMXd7U2CmMpxlR1yZVHTMZBX/KT5kU/6IVVqswlMicxgnMtBeRHciyJexTvUeCG3IBbcgvuyT041w96aI7r4dnTs4dnv/Wc6sg4zhZtENMxpgY35BJc02cEl8wPao1zauSQa0BHPDuRuY1pDavdHHHOmPCpqTVqZOjfgDtyl9Yz8+aQT8c8O+TZbddnKFpjzRjOUYLr7drG3LdrUiInsi4eZMrVOm3j6dE/yq3Nrc9bQp12z5/cX/POGpKpTcxOjvObW9Gj3rpG53/u/Y/7d2mv1a3Ol/ObwXCEv8Tj6w+jg85sPh1McNZZTq9G8+053kjWrepLlY+uSS84/19S/tJLSiqB/KVXlSd4eh6x00V28Xw1Z6K6W/YH/eEMawy5y9x8w5/cPR7/Xusr",
        },
        {
            "url": "https://puzz.link/p?hinge/14/12/k1ag51905514k4kgii2i8qa29800a010000rtg060s007o0007o30e0o0cfjg00-2bh26262626g2h",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(hinge_symmetry(color="gray"))
        self.add_program_line(hinge_avoid_isolated_edge(puzzle.row, puzzle.col, color="not gray", adj_type=8))

        # horizontal symmetry axis check
        for r in range(1, puzzle.row):
            c = 0
            while c < puzzle.col:
                if Point(r, c, Direction.TOP) in puzzle.edge:
                    c0 = c
                    while c < puzzle.col and Point(r, c, Direction.TOP) in puzzle.edge:
                        self.add_program_line(f"edge({r}, {c}, {Direction.TOP}).")
                        self.add_program_line(f'symmetry_axis({r}, {c}, {r}, {c0}, "H").')
                        c += 1
                c += 1

        # vertical symmetry axis check
        for c in range(1, puzzle.col):
            r = 0
            while r < puzzle.row:
                if Point(r, c, Direction.LEFT) in puzzle.edge:
                    r0 = r
                    while r < puzzle.row and Point(r, c, Direction.LEFT) in puzzle.edge:
                        self.add_program_line(f"edge({r}, {c}, {Direction.LEFT}).")
                        self.add_program_line(f'symmetry_axis({r}, {c}, {r0}, {c}, "V").')
                        r += 1
                r += 1

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count(num, color="gray", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
