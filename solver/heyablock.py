"""The Heyablock solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import area_color_connected, grid_color_connected
from noqx.rule.shape import avoid_rect


class HeyablockSolver(Solver):
    """The Heyablock solver."""

    name = "Heyablock"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVdT9tAEHzPr0D3fA/3aZ/9UlEa+kKhbUAVsqIoBFOiJgpNSFU5yn/v7HnNEYQKVVWqSlXwMTs+7+7N2Herr+vxspZa0Z8NEv/xczrEy4QsXop/p9PbWV3uyf317fViCSDlyeGhvBrPVnWv4lnD3qYpymZfNm/LSmghhcGlxVA2H8pN865s+rIZ4JaQAdxRO8kA9hP8FO8TOmhJrYCPGQOeA06my8msHh21zPuyak6loDqv49MExXzxrRbcB8WTxfxiSsTF+BaLWV1Pb/jOan25+LIWXYmtbPbbdgePtGtTu/auXft4u+bPt1sMt1vI/hENj8qKej9LMCQ4KDdb6msjrMKjFl5HZ4Q1CE0KAyV+Je4IT4S7CzO1Mz1zCH0Ks527WqkHsduprZ15EGcP4nDvefSv4yrO43gYRxPHUyxSNjaOb+Ko4ujjeBTn9LF2o600JhelwbupPXDBOJfGasYFsG2xAe+YN+Ad81YDe8bI6TinA++Zd+B9x6OW51oOOTPO6cFnzHvwecejVs61MuTMOWcGPjCfgw/M56gVuFaOnIFzBvAF8wF80fG5tIprhQKYcxbgNfMFeN3ymAvsGVvgNifmSmuYh7bWdLwHLhgjJ2uLucDMQ1vrOh61WFvMBeacFrxnHtpa1hZzgbkWtLWdtpY8UqyzSt6RL/SyRWySj+SRc4xd8pT8opcx4uyev/Q+BMbYJl2nJ3nB+YNJHpH+gfMHl/wiLwLnj1tt5xHyB84fwj0fsa6C11VgXUWnG2nuGLvkBelsMsZZ8oU0N4FxSB6R/lax5ir5RV5Yw9gA07q2tO3RJ3UQRxfHLH5qOe02z9yP4k4UpIiat5vT73/iT/ZW2fak2/35f48b9ioxWC+vxpMaB0P/8nO9d7xYzsczRMfr+UW97GKcy9ue+C7iFbdX9/+o/ktHNVmgfunAfoFv4ol2KqiLDbE5keJmPRqPJgu8Y9DuZzy+sufOf/HVYhMY9n4A",
        },
        {"url": "https://puzz.link/p?heyablock/10/10/498g17buntfqsh12247obovv003o00vv3o3o726h22j2h4g6g2", "test": False},
        {
            "url": "https://puzz.link/p?heyablock/15/10/4i894gi914i2944i894gi914i294000vvv000vvv000vvv000vvv0001122222024024311331235234",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(area_color_connected(color="gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            flag = True
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    flag = False
                    self.add_program_line(count(num, color="gray", _type="area", _id=i))

            if flag:
                self.add_program_line(count(("gt", 0), color="gray", _type="area", _id=i))

        for r in range(puzzle.row):
            borders_in_row = [c for c in range(1, puzzle.col) if Point(r, c, Direction.LEFT) in puzzle.edge]
            for i in range(len(borders_in_row) - 1):
                b1, b2 = borders_in_row[i], borders_in_row[i + 1]
                self.add_program_line(avoid_rect(1, b2 - b1 + 2, color="not gray", corner=(r, b1 - 1)))

        for c in range(puzzle.col):
            borders_in_col = [r for r in range(1, puzzle.row) if Point(r, c, Direction.TOP) in puzzle.edge]
            for i in range(len(borders_in_col) - 1):
                b1, b2 = borders_in_col[i], borders_in_col[i + 1]
                self.add_program_line(avoid_rect(b2 - b1 + 2, 1, color="not gray", corner=(b1 - 1, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            if d == Direction.TOP and r > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r - 1}, {c}).")

            if d == Direction.LEFT and c > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r}, {c - 1}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
