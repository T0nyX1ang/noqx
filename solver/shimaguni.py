"""The Shimaguni solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import area_color_connected


def adjacent_area_different_size(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to enforce that adjacent areas have different sizes.

    An adjacent area rule and an area rule should be defined first.
    """
    size_count = f"#count {{R, C: area(A, R, C), {color}(R, C) }} = N"
    size1_count = f"#count {{R, C: area(A1, R, C), {color}(R, C) }} = N1"
    return f":- area_adj_{adj_type}(A, A1), A < A1, {size_count}, {size1_count}, N = N1."


class ShimaguniSolver(Solver):
    """The Shimaguni solver."""

    name = "Shimaguni"
    category = "shade"
    aliases = ["islands"]
    examples = [
        {
            "data": "m=edit&p=7VZda9tKEH33rwj71MI+aL/09VLS1OlL6tzWuYQgjFEcJTG149SOSpHxf8+Z3dnohhtIS2lKodjaPRrPzh7NmVl586Wt141UCX1NLjHjY1XuL52n/kr4czK/WzTlntxv765XawApjw8P5WW92DSDir0mg21XlN2+7N6XlVBCCo1LiYnsPpbb7kPZDWU3xk9C5rAdBScNOOzhqf+d0EEwqgR4xBjwDHA2X88WzfQoWP4pq+5ECtrnrV9NUCxXXxvBPOh+tlqez8lwXt/hYTbX81v+ZdNerD637KsmO9ntB7rjJ+iani7BQJfQE3TpKX4x3WKy2yHtn0B4WlbE/d8e5j0cl1uMo3IrTIKlGlp7ZYQxj28zCvwGTNmgdPHIQVnyoFqhe8RUPvKZHw/9qP14go1lZ/z4zo+JH50fj7zPEHy0MlJrBNWoF2WBc8YoQSLrcQasGKM8jQ5Yw27ZrmG3bDcJsGWsgB1jDZwyxl6W97LALmIHjIf2GBxS5mARP+X4Dv4p+zv4ZOzj4JOxT4q9Mt4rpZZiewZuOXPL4JOzT4Y4BcfJYS/YnmOvgvdCS5ok+hTAUI9wAbtie5EDh73gCxz2gi9wyDN8pdFsVwo45AfrgMO+WAcc9sU6aTj/WAfMdu2AQ66wThobOGAdMHPA4WJcxODsAmf4AjMHC26Oa4A0oqr0GLVhoo7Ig4k6FtAu6kJacw1Y0przbElrjoP4D/XggHlfr6PjmI5055yTppGPQ43F2iB9Y204cIi1kYJDyhxScIh1kmJtrBN/pHLMHPY82qk2OCY0faiBAjELznmCvLG+XjvFdtIuak05p2b1GP7cO5h77dALhnsHM/B/tOAcYu61Qw6hTa8R5xAzMNcM+sVwT2EGpmdEc5/6Fj/wo/Vj6ls/oxPpO88sf1rl9KAhJg6wnz9ynuVWIWV0wj3+uD/PNhlUYtyuL+tZg5fH8OKq2Rut1st6gbtRuzxv1vEe7+7dQHwT/qoM/RX4+zr/Ta9zkiD5oZf6C/TEM3QqZBdd0x1LcdtO6+lshRpD7rxd/c/+4uzR1AJJX9ZX7c1879V8s6hvLjavxWRwDw==",
        },
        {"url": "https://puzz.link/p?shimaguni/10/10/tbqnmfcip5kb8m1e2o003v00vesf00v3v6sfzh3", "test": False},
        {
            "url": "https://puzz.link/p?shimaguni/15/12/55a19a6l11nhcnqlddnqkr5cmajmaoeahc3gqv3nftavvke414681sk3e7cekml25fok2o43g1s",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(area_color_connected(color="gray"))
        self.add_program_line(area_adjacent())
        self.add_program_line(adjacent_area_different_size(color="gray"))

        areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(areas.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            flag = True
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    flag = False
                    self.add_program_line(count(num, color="gray", _type="area", _id=i))

            if flag:
                self.add_program_line(count(("gt", 0), color="gray", _type="area", _id=i))

        for (r, c, d, _), draw in puzzle.edge.items():
            if d == Direction.TOP and r > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r - 1}, {c}).")

            if d == Direction.LEFT and c > 0 and draw:
                self.add_program_line(f":- gray({r}, {c}), gray({r}, {c - 1}).")

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"gray({r}, {c}).")
            else:
                self.add_program_line(f"not gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
