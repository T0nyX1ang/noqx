"""The Aqre solver."""

from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(4, 1, color="gray"))
    solver.add_program_line(avoid_rect(1, 4, color="gray"))
    solver.add_program_line(avoid_rect(4, 1, color="not gray"))
    solver.add_program_line(avoid_rect(1, 4, color="not gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
            if isinstance(num, int):
                solver.add_program_line(count(num, color="gray", _type="area", _id=i))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))

    return solver.program


__metadata__ = {
    "name": "Aqre",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VXPT9tMEL3nr0B73oNnfziOL1VKQy80tA0VQlYUmWBK9CUKOLiqHOV/5+14HJcKFdCnUlWqEo/fjmfHb97seje3VV4WmqLwt4nGHT9HCV8mifmK5He6uFsW6YEeVnfX6xJA65OjI32VLzdFL5OoaW9bD9J6qOv3aaZIaWVwkZrq+lO6rT+k9UjXEzxSOoHvuAkygKMOnvHzgA4bJ0XAY8GA54DzRTlfFrPjxvMxzepTrcJ73vLsANVq/a1QwiOM5+vVxSI4LvI7FLO5XtzIk011uf6vklia7nQ9bOhOHqFrO7oBNnQDeoRuqOI30x1MdzvI/hmEZ2kWuH/pYNLBSbqFHadbZS2mGvSaO6NsP2R6A2qtY/DguXMYJt0wefCUzE9jG8LDWpKxMz+MwYCYxznbI7aG7Slo6tqyfcc2YuvZHnPMCOwNGW1MrFKD1UUOGAQY97WxJHgAjDIDNhEwSDGG34nfwh9qY4ycTnJa5AxFBuysNh76MMamiFEMsCXS1njBBriZa8kDQz7GsbY2EtwHbrhZbC5rJY9xwM27kA9Y5hrMdTIXnK1wxjxgeZfDrvUNf+uQx0sehzy+yWOQc6+VAX/hxjoIN9ah1S3o0OqGnMY1NeLe6eODJqKbR4yXGI8Y38bg49Hq5tEX4YY7sHDw4BALhxgcYuEQ015n3IGl9gg6UKsnaqdWT/SC2r5AH5J4ssCiD9YJetP1iNp+oS8kuoW+UKs/5hqZC332vcNnct8jrA3o3mnO+mCRnvFSPWTr2Ma8hPthHz5zp6JaIaXSpNm2/3/rPMktQ6nhDHj483+fb9rL1KQqr/J5gU/m6PJrcTBel6t8idG4Wl0UZTvGibXrqe+Kr8yGA/DfIfaHDrHQguhFR9kr7Ikn6GRQ1/Z1faLVTTXLZ/M11hi0+6U/eqGfnh3/6urgo6Hy27JQ0949",
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
    ],
}
