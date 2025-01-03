"""The Anglers solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import tag_encode
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)

    assert len(puzzle.symbol), "No clues found."
    assert len(puzzle.text) == len(puzzle.symbol), "Unmatched clues."
    solver.add_program_line(defined(item="black"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("anglers(R, C) :- grid(R, C), not black(R, C).")
    solver.add_program_line(fill_path(color="anglers"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(single_loop(color="anglers", path=True))
    solver.add_program_line(avoid_unknown_src("anglers", adj_type="loop"))

    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert d == Direction.CENTER, "The symbol should be placed in the center."
        assert symbol_name == "tents__3", "Invalid symbol."
        solver.add_program_line(f"dead_end({r}, {c}).")

    tag = tag_encode("reachable", "grid", "src", "adj", "loop", "anglers")
    for (r, c), num in puzzle.text.items():
        if not (0 <= r < puzzle.row and 0 <= c < puzzle.col):  # coordinations out of bounds
            solver.add_program_line(f"grid({r}, {c}).")

        solver.add_program_line(f"dead_end({r}, {c}).")
        solver.add_program_line(grid_src_color_connected((r, c), color="anglers", adj_type="loop"))
        if isinstance(num, int):
            solver.add_program_line(count_reachable_src(num + 1, (r, c), color="anglers", adj_type="loop"))

        for (r1, c1), _ in puzzle.text.items():
            if (r1, c1) != (r, c):
                solver.add_program_line(f":- {tag}({r}, {c}, {r1}, {c1}).")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Anglers",
    "category": "loop",
    "aliases": ["anglerfish"],
    "examples": [
        {
            "data": "m=edit&p=7VNNi9swEL37Vyxz1sGy7NjWpaTbTS9u+pGUJRizOKmWmCbrrT9KUch/35mRg1Oyh7LQsocy6PH0JHmeRp72R182RiQYKhG+kBgqDHgEfsrDH2JZdTujr8S077Z1g0SIj7OZuC93rfFyOolReAebajsV9r3OQYKAAIeEQtjP+mA/aLsSdoFLIELUMrcpQHoz0lteJ3btROkjnw8c6QppZx661k0/6dwuBVCSt3yUKOzrnwYGEzTf1Pt1RcJwksW2/1Z/74dtsjgKO3U2s5NNSjDYVKNNos4msWdsknuyuamazc7cZS9yui47rHm7rR6fs5sWxyOW+wsavtM5ef860mSkC32AKAQdIp8Tl6f7upeBCS7m9FAnIY5JUKOQ+iSEoyB9RUp0psgJKW9OCiaT+oC4wpQqxTUlzh4NIvrA79LkUoqjSym5kBLyey5h2hknDxiXWAhhFeM7Rp8xYsx4zw3jLeM1Y8g44T0xlfIPi+3KfH7/v2QnV6nrOo745bzwclj0zX25MfijZdWDuZrXzb7c4Wze79emGeeLbfloAPv86MEv4IGll9jO/1v/37Y+ld5/bf/ka7ODXVJ4Tw==",
        },
        {
            "data": "m=edit&p=7ZRLi9swFIX3/hWD1ndhyfbE1qak00k3bvpIyhCMGZxUQ0yTeOpHKQr573PvtYvHTjYttEyhyDocHevxISFV35qsNCAVfV4ILkgsfuRz9SYBV7cry7zeGX0F06beFiUagPezGTxku8o4CY3EkjpHG2k7BftWJ0IKEAqrFCnYj/po32m7ArvAXwJ8zOK2k0J729s7/k/upg2li37eebQrtLU51FXb/KATuwRBi7zmoWTFvvhuRAdB7U2xX+cUdCM5rJovxdem6ybTE9hpixn/xKQFOkyvxyTbYpK7gEn0hLnJy83O3Me/RbrOatzzaps/XsKN0tMJt/sTAt/rhNg/9zbs7UIfUef6KLyQhr5ClvZMhK9GQTgOpArGiX89TibjeWUYjRIlh6OQSDLXCrkCH/958OxMRUBTDqPQO4sieRZJdT6ZjGjxYaZc90I2XgIBZ4ypWJe4o2A91jesLmvAGnOfW9Y71htWn/Wa+0zoTH7p1J7v1B/CSYLu+g7K5N/LUicRi6Z8yDYGb0ycH8zVvCj32Q5b82a/NmXfXmyzRyPwwTo54ofgikeP79//N+wvv2G09e5LuxMvDQdvaeo8AQ==",
        },
        {
            "data": "m=edit&p=7VRdb5swFH3nV1R+vg82hibxW5Y1e2HZRzJVEUIVYa6CRkrHxzQ54r/33gsTLevLJm3qpMnx0fHB5hyuY9df27SyoHz66TlIUNiCRcBdz0Lucmi7vCmsuYBl2xzLCgnAu/UabtOitl5MK7El3tktjFuCe2NioQQIH7sSCbgP5uzeGrcHt8VHAgLUon6Sj/RqpNf8nNiqF5VEvhk40j3Sxt41dT98b2K3A0Emr3gpUXEqv1kxhKBxVp4OOQnDShbr9nP5pR2mqaQDt+xjRj9iksEQU48xifYxiT0Tk9JTzCyvssLeRL+V9JA2WPP6mN8/F3eRdB2W+yMGvjExZf800vlIt+aMuDFnoRe01JcYpt8UEfhTRWn5kxRcTiVf6acSOij22aPPnHw0PNojoSS9Y6JpeslEC8l+os2mGvqs2c1n3OGHgtOMrxklY8gY8ZwrxmvGFWPAeMlzZlSqXyrm4w/+Q3HicDhVT9rs39MSLxbbtrpNM4t/5Ci/sxebsjqlBY427elgq3G8Pab3VuA90nniu+COW4/X0v+r5S9fLVR6+dLOxEuLg6c08R4A",
            "test": False,
        },
    ],
}
