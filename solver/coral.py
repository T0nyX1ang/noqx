"""The Coral solver."""

from typing import List, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import border_color_connected, grid_color_connected
from noqx.rule.shape import avoid_rect


def len_segment(color: str = "black") -> str:
    """
    Generate a rule to get the length of segments.
    """
    rule = f"nth_horizontal(R, C, 1) :- {color}(R, C), not {color}(R, C - 1).\n"
    rule += f"nth_horizontal(R, C, N) :- {color}(R, C), nth_horizontal(R, C - 1, N - 1).\n"
    rule += f"nth_vertical(R, C, 1) :- {color}(R, C), not {color}(R - 1, C).\n"
    rule += f"nth_vertical(R, C, N) :- {color}(R, C), nth_vertical(R - 1, C, N - 1).\n"

    rule += f"len_horizontal(R, C, N) :- nth_horizontal(R, C, 1), nth_horizontal(R, C + N - 1, N), not {color}(R, C + N).\n"
    rule += f"len_vertical(R, C, N) :- nth_vertical(R, C, 1), nth_vertical(R + N - 1, C, N), not {color}(R + N, C).\n"

    return rule


class CoralSolver(Solver):
    """The Coral solver."""

    name = "Coral"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZdayM3FH33r1j0fB/0cTWj67d0u+lL6m2blLIYExzXy4Y6OHXiUib4v/dIuhNHaWB3aQkUyjDSOfOhe+85kmbuft8vd2tykVygkMiSw9HZRDF4cp0rp9Xj4vp+s56+oZP9/aftDoDo/ekpfVxu7taTecATkexi8jDIdDih4bvp3DhDxuN0ZkHDj9OH4fvpMKPhHLcMMa6d1Yc84Lsj/KXcz+htvegs8Ewx4AfA1fVutVlfntUrP0znwwWZHOeb8naG5mb7x9poHpmvtjdX1/nC1fIexdx9ur7VO3f7X7e/7c0Y4kDDSU33/IV0wzHd8JhueDld/6+ku7ndvpSoLA4HCP4TUr2cznPWPx9hOsLz6cMhZ/RgWPBqdrl4YqJvaMctjaD+SLuWpob2DjQ80hSaoRI3D6d25NQ374ptaR6Zj7RvRpbU0rZAZ+0z7prITtqSncRnvGty8UUxfsJDy/s2ni+yPOVP34cprljzobSnpfWlvYBzNITSfltaW9pY2rPyzDsYGjhR6CCJJ4Mey7irOHXENhaMnthzxZ6JOVTMgbjzFXeeOLmKk6OYhQNGT9FJxU6wM6SKsV/EWOOip9jXuOgpSo0bIraVXDC2FwNAIVtZiDhiZysBQHqixAvyS0pQHOfiCkF1nKsrBOXFXF4mABRzfYWgwJgLLAQVxk4zAKCYNAMA7HSaQYgQsVcRe4goKqJARKciYpvkoCIGiBhVRBTJvYqIGllURJQYnYqICqNXEVFgZBUR9UU1Dz2yUxFRXfdoHtSxOqaFbFZjWcSymoNFDlZzs9wabzvFeUL0iiGlTYqhsRXFUm3x6orTuC7bpXEd4jqNC/HYaVzHR60EcWW0Kosoo4mCyDLaKwgto/EiddJVRyGYHa2yeTqOJqLsaEd7UXe0o/EovJ0SthtJniz9SKCzTSOBAVZGItWxQgQZqJUxWyleMeJLUIzwwor5cd6jB1YrJa8HtRjFR1HrUXsUnRIovdP1hh7YKc5z1Cv2wEFxAGbFrFPlkL9EeVt4W1oubVe2iz5/Br7wQ4EtEhEZ+5N3ddRZGekfblSfzW6OuOX/49lh/7sXF5O5Od/vPi5Xa3y9Z/ubq/XuzWy7u1luDH6UDhPzpyln+cDw//9Or/7vlMW3X/UH9Qor4TPpzKFrXivDezK3+8vl5Wq7MfjzpnLDu7/dePX8sZgXk78A",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        top_clues = {}
        for c in range(puzzle.col):
            r1 = -1
            clue: List[Union[int, str]] = []
            while (r1, c, Direction.CENTER, "normal") in puzzle.text:
                clue.append(puzzle.text[Point(r1, c, Direction.CENTER, "normal")])
                r1 -= 1
            top_clues[c] = tuple(reversed(clue))

        left_clues = {}
        for r in range(puzzle.row):
            c1 = -1
            clue: List[Union[int, str]] = []
            while (r, c1, Direction.CENTER, "normal") in puzzle.text:
                clue.append(puzzle.text[Point(r, c1, Direction.CENTER, "normal")])
                c1 -= 1
            left_clues[r] = tuple(reversed(clue))

        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="black"))
        self.add_program_line(border_color_connected(rows=puzzle.row, cols=puzzle.col, color="not black"))
        self.add_program_line(avoid_rect(2, 2, color="black"))
        self.add_program_line(len_segment(color="black"))

        for r, clue in left_clues.items():
            if clue:
                count_dict = {}  # Replace collections.Counter with manual counting
                for num in clue:
                    count_dict[num] = count_dict.get(num, 0) + 1

                for num, count in count_dict.items():
                    self.add_program_line(f":- #count{{ C: grid({r}, C), len_horizontal({r}, C, {num}) }} != {count}.")

                forbidden_len = ",".join([f"N != {x}" for x in count_dict])
                self.add_program_line(f":- grid({r}, C), len_horizontal({r}, C, N), {forbidden_len}.")

        for c, clue in top_clues.items():
            if clue:
                count_dict = {}  # Replace collections.Counter with manual counting
                for num in clue:
                    count_dict[num] = count_dict.get(num, 0) + 1

                for num, count in count_dict.items():
                    self.add_program_line(f":- #count{{ R: grid(R, {c}), len_vertical(R, {c}, {num}) }} != {count}.")

                forbidden_len = ",".join([f"N != {x}" for x in count_dict])
                self.add_program_line(f":- grid(R, {c}), len_vertical(R, {c}, N), {forbidden_len}.")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
