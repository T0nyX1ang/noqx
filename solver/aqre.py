"""The Aqre solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect


class AqreSolver(Solver):
    """The Aqre solver."""

    name = "Aqre"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVRb9MwEH7vr5j87IfYZ6dOXtAYHS+jA1qEpqiqui5jFa0y2gWhVP3vfHYuNUUT24QYQkJpLp/Pd9cv39nx5ks9W5dSJf5HTuKJyygXbu3ScCd8jRd3yzI/ksf13U21BpDy/PRUXs+Wm7JXcNSkt22yvDmWzeu8EEpIoXErMZHNu3zbvMmbgWxGmBLSwXfWBmnAQYQfw7xHJ61TJcBDxoAXgPPFer4sp2et521eNGMp/P+8DNkeilX1tRTMw4/n1epy4R2Xszu8zOZmccszm/qq+lyL7i92sjlu6Y7uoUuRLu3p0v109Z+nm012O8j+HoSneeG5f4jQRTjKtzvPayuIkKrR69AZQX1f6YWIjuxg3hgMXRy6g1mlfxqTD0/i2OgfxmCgAo+LYE+D1cGOQVM2FOyrYJNgbbBnIWYA9lppqXUqco3VpQywY9yXmhTjDJharBNgwxh+w36C37CfUNNwTUJNwzUNSW37jLEpUh0wKSVJW8YaOGVsgTPGqSRKGPeBFWMHzHW0AXaMkUucq5FrOBeciTkjD5j/y2DXWsMYdSzXMahjM35fG7XS4K+zqANzCzp0unkdOt2M18EytlEf6zVh3SxiLMdYxNguJo26WfSFueEJzBwsOKTMIQWHlDmkaq8znsD87gl0UJ2eeHfV6YleqK4v0EdxvCJg1gfrBL2JPVJdv9AX5WJfVKc/cjXnQp9978jFHmFtkDFR86DPzn8Q/FI9CdYEm4Yl3Pf78JE7VewXjshdu21/f+s8yK2g9gw4vOy/55v0CjGq19ezeYlP5uDqU3k0rNar2RKjYb26LNfdGCfWrie+iXAX5A/A/4fYXzrEfAuSJx1lz7AnHqBTQF3qy+Zcitt6OpvOK6wxaPdLf/JEv3p0/LOrg4/GpPcd",
        },
        {
            "url": "https://puzz.link/p?aqre/18/18/aba2qqg6mi2nhodt6jfc57m8qt96l6a1828b1j6ucn7p5bspeseknpl0od86h00o00svvhe3e41s3g8r2gr3v9u0241vvvrufs3gf3soc0m1g21c3o3k3sn000s0g1g1g22g11g2g22g1g2212g1g1112233355g555355g3g3g355",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?aqre/21/17/144g3ab85s7kb44ql7sl61gc600ccc66cc66ic69c286i1g9cfu6nlltag1a4g1420081q5816tq1dvmh850l248h00g0321300001800kkbkaa18552l2lllllcdhkbvvk2fv404g7411g0115111339001112000182",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?aqre/25/18/g60o30c1g4000014o20vtofvvrgvu971vt1e30o0820g0gs1o1g2fg2g8v8d0hm1q138jk32r7cfdn6ouo0280000000vvvvvvuvo194fis9001014000vu07svufnsvv0nu80fu4nvfvq1u0011s000707to603oo0c000vvvvvg2g2g2h346g31gf1221g11311dg22451-10c9g36420505",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(4, 1, color="gray"))
        self.add_program_line(avoid_rect(1, 4, color="gray"))
        self.add_program_line(avoid_rect(4, 1, color="not gray"))
        self.add_program_line(avoid_rect(1, 4, color="not gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count(num, color="gray", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
