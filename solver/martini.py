"""The Martini solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode, target_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import area_color_connected, grid_color_connected, grid_src_color_connected


def count_reachable_src_white_circle(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4):
    """Generate a constraint to count the reachable white circles starting from a source."""

    src_r, src_c = src_cell

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    rop, num = target_encode(target)

    return f":- #count{{ R, C: {tag}({src_r}, {src_c}, R, C), white_circle(R, C) }} {rop} {num}."


class MartiniSolver(Solver):
    """The Martini solver."""

    name = "Martini"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VTRbtMwFH3PV0x+9kPs6zhdXlAZLS+lA1qEpiiq0ixjFa0y0gYhV/l37nXchbWeBpMYLyiyc3J87XtybN/ttyavS67xgQEPucBHam2bUMq20D3z1W5dJmd82OxuqxoB55fjMb/J19sySF1UFuzNeWKG3LxNUiYYZxKbYBk3H5K9eZeYKTczHGJ8gNykC5IIRz38bMcJXXSkCBFPO6wRXiEsVnWxLhcTHEXmfZKaOWeU57WdTZBtqu8lczrou6g2yxURy3yHP7O9Xd25kW1zXX1tXKzIWm6GndyZRy70cuFeLvjlyr8v9zxrW7T9IwpeJClp/9TDQQ9nyb4lXXsmFU3FnRHd3jAZE/EK3XWEkkRAH6GOIyJ1RGh9NCWWBz8tgbmFVXBFCmhM8oe2dLrECRv7WFC+Fazuk1gF3lj/CtrLejVEXr3am83acxIbe/SiRWNrlLT9HHePG7D9G9uHto9sP7ExI7RUCMkF+Yqp8c0FOAyI1YEXD2MkOAyIlcN478FhsDWgw1QPIocjxPrA0/puHQV9PM2FyOEIse6wwNoiHZa654FqjsOKcNxhjZq106wxl3a5NPQaNOlxuTTm0m4dqmMx4ZbuKVl1YXtle20tjOl6/OYFYs4wwNegu02/nuvnbd2T2lLaqvsnej7OgpTNmvomL0qsJKPrL+XZtKo3+Rq/ps1mWdaHbyzkbcB+MNtSdJqr/7X9H9V22oLwjyr8C5zJJ+Sk6C6eWnPJ2V2zyBdFhWcMvbM8PMI/Eg+n8S/+t3gJs+An",
        },
        {
            "data": "m=edit&p=7Zdbbxs3EIXf/SuCfebD8jK86M117b646cUOikAQAsdRGqM2lEp2UcjQf+8Z7qFWUoQWLVAkD4GgnU+zs8NDckiuVr8/3SznxkZjvfHZ9MbiE0M04p2xNpfh0vNzffd4P5+8MKdPjx8WS4AxP1xcmPc396v5yZRRs5PndZmsT836u8m0s53pHL62m5n1T5Pn9feT9blZX+FWZzJ8l0OQA56P+Eu9r3Q2OG0PfkkGvgbe3i1v7+dvLgfPj5Pp+tp02s439WnF7mHxx7yjDv19u3h4e6eOtzeP6Mzqw91H3lk9vVv89tS1JjZmfTrIvToi149y/VauPy7X/f9yy2yzwbD/DMFvJlPV/mrEPOLV5Hmjup674PRRzIwd5qaLsXWdjhQOHNkdOKw7DLGuHHrK4VMu7sdAkK2yXjdZ8O+NVRcEXnforYo/iU39UW845s1HWyvpmHfo7BF3OeouR1O7/mhPhiH5NLrqO4jGQF3U4XL1eo2JNWtfr9/Wa1+vUq+XNeYcA+tjwApHF5AO1oR+YFgTHNn5fQ5+4OB22ILd+Kz2qLKAIzmC09BWTGiXnNPWD4u2yE45kzPy5zGnY36nvJO/cVCd1BygJzA+ID60GMRHcgRnclamBmgTaoMFU0OAtsiYqLzjbzqDai7kYoL0jIc/MybnbU5YI+wvrJGWR+Mj80TkyWRswdIXPgu2Q35YsCVbsCM7MOdLehMS9SRwIRdlS7bbPDUmNcZcJ851Qg0UcnHbtjziPXN6zUltsCZ4su/HMVF/awuaA/PAgqkZp1HwTT/mVDinXka2YC9sF2zJSaCnsQNTZ3H7bXmytzusmqkNB2AQ+kW56YG2RE7KrL0EnYnaoCEk1lhCjaU0xhTGl4AxDJwvsCd7ZSELODIGh7JNIze/BwtZwGwX1kghl2iiHRjWxG1OjzyeecDsIyyYejD+wj4K+jsyaoDjIKgTYZ3UenasVYdaZQ3AglmrGHPhmOuLhnCcRew+sw5rftaqoJ5xb2TWNixiyKjDyDqERX/p1xebwDHE+m3rDhZMzVi/wjUIa4RrUHQN7uTf6tG1wxoTXReFY1IwVpxr0blmTcKO84KckesadqtZdK9o7UZl6sT+I3GHuXcJ9rGRkT+3/Gg3s90MPdz/Y4+XvN6RHdiTPbjFBLCQBcz6wd4buU/CgjM5m9j2tOy2+SViTDIZ5wh+szbAPEcEGvB7ZOqBBXMMoUeoBxbMPuKcEp5NsMhPjtpfP8bwXIMFMw/OFOF5ITg79jgyPirTHxHPc6TWUmOMibimR5lz4dK23oLOSzsrkSfkxtgTYjuzlLk/ZOxLHLeAMdxj9hEWfnJWbs+GMb/un3XNbvQ1VV8Hzuo11GusrwlJ3w7/1fvj7kvbf3sj+Uc5U1SL/duPfL3/Oe/PTqbd1dPy/c3tHP9Jzt/9On/xcrF8uLnHr7PFw8fF6u5x3uHv4Oak+7Or36nHg+HrP8TP9A9Rp6D/0tb5lyYHO8/s5C8=",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(area_color_connected(color="gray", adj_type=4))
        self.add_program_line(grid_color_connected(color="gray", adj_type=8))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)

            if symbol_name == "circle_L__1":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"white_circle({r}, {c}).")

            if symbol_name == "circle_L__2":
                self.add_program_line(f"gray({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color="not gray", adj_type=4))
                self.add_program_line(count_reachable_src_white_circle(num, src_cell=(r, c), color="not gray"))

        for (r, c, d, _), draw in puzzle.edge.items():
            if d == Direction.TOP and r > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r - 1}, {c}).")

            if d == Direction.LEFT and c > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r}, {c - 1}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
