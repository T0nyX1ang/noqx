"""The Double Back solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, fill_line, grid
from noqx.rule.helper import fail_false, full_bfs, validate_type
from noqx.rule.neighbor import adjacent, area_border
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import count_area_pass, single_route


class DoubleBackSolver(Solver):
    """The Double Back solver."""

    name = "Double Back"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VRNb9pAEL3zK6I9zwHvV8E3mkIvNGlLoiqyEHKI06BCnQKuokX+732zHvDFUaW24lStdvQ883bneXZ2dz+qfFuQxzAD6lOCob2PM7E2zr6Mm9V+XaQXNKr2T+UWgOh6MqHHfL0repmw5r1DGKZhROF9mimtKM5EzSl8Sg/hQxrGFGYIKUrgmwIlijTguIVfYpzRZeNM+sBXggHvAJer7XJdLKaN52OahRtSnOdtXM1QbcqfhWqWxe9lublfseM+3+Nndk+rZ4nsqofyW6WOKWoKo0butEOuaeWak1zTLVf/C7nr1ffipUvpcF7XqPhnaF2kGcu+beGghbP0ULMktkm0d9FOotXR3oBKwUT7Ltp+tC7aaeSM04NKtKbEaJVqHKxGnxjfYAO/Fb8xwEawA3aCua+Eb8F3wrfgO+Fb8J3wLfhO+A58L3wHvxc/69GyVmMfbQWjf7Vr9RjxO851xLbN5Xl/2ceD44XjwfFHjpO8NZ87l+QyWhutj6V6wzU/26kozf8+HJAyfCgMUBCGJiKOmubofqs541KehvtzPO9lalZtH/Nlgbadon0vrsrtJl/ja/zw9fSF56LuqRcVZ4aak/3/gpz/BeHq98/8jvztBcpQWOl0CteknqtFvliW6DDU7hhE83cHcWm6A7hEr21nEHw1V3fw7DXDHZ73fgE=",
        },
        {
            "data": "m=edit&p=7VZNTxsxEL3nVyCfffDn2rs3SqGXFNqGqkKrKAohlKihoQmp0Eb57322x3GrBoHUCqlStazn7diZGc+bsVl9W4+XUy5F+NOeQ+Ix0sdX+Sq+gp7z2f182hzww/X9zWIJwPnZyQm/Hs9X015Lq4a9TVc33SHv3jQtU4zHV7Ih7943m+5t0w14N8AU4wa6PpBkXAEeF/gpzgd0lJRSAJ8SBrwAnMyWk/l01E+ad03bnXMW/LyKvw6Q3S6+T1n6WfyeLG4vZ0FxOb7HZlY3szuaWa2vFl/WLLvY8u4whdvfE64u4epduHp/uOpvhDuffZ0+7Iu0Hm63yPgHxDpq2hD2xwJ9gYNmw7RgjeFM6ySqJOoonErCJuGj8DIKKQ1Jl6QSJJMlaSuSyZasFMlgbRsyscEo43gRx5M4qjieI0Le6Ti+jqOIo41jP645RvhKKq4UXCnUlDTAnrAFrgk7rrQkjBLWKmElgA1h6A3ptQS2CRvYt2TfwKYlmxa+KvJl0RJOEIYvR75sDawTruDLka8KNh3ZdPDlyZeDTU82PXzV5Ms7rgXZ9B6Y4qwrriX5rbFG0poaa2ReUwOnGGAD2BJWwBVhA5z8wgbXitYgt5pyCxvAjrAFTrFBx7WRhOHLkC8cHNqmGLTBOWINYdi3ZN/ApiWbBjFYisFgXxXtS9nCb+Aocxo4yjxq5E1TDq0GR6ZwZLPeFh4DX+Q38mUzj/4nfsFdjiHwVWUeXeHdicJ14NFRPE4V3p0uvLtQJ67w6ymeeKSSvg68Vzt+weuOX/C64zfXRuSU6iFyKjLXyK0whV+Rea93NRP5zbUROM31IEP9ZH5tqQENrnXmSBTeA48m8wvuTIh5G47A0KZHcTRxrGL7unD8PPOA+vOTghmNeJAzVoVTLgAUW+hvHfaaEXShDpIuVJZOR8yT+2h1uiF/fey/pxv2WjZYL6/HkylulT5ul4PTxfJ2PMfX8dXn3Rdu822PPbD4tjr8c/D/gn/5Cz5kX7xYFz2zGZ4Ip0Viqft4d8bZ3Xo0Hk0WqDDkLk6mhnxkMvXo/kl0+f4JdP3jvtDov02+eM5whgx7PwA=",
        },
        {
            "url": "https://puzz.link/p?doubleback/23/9/051602u9ghhls666vh35bk1stt667e518hg0i48006800uuvnhvpge766m1oso0f3g3guvuu8e040000040000000000000000000000000000000000000",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="grid", adj_type="line"))
        self.add_program_line(single_route(color="grid"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

            # enforce the black cells (holes) to have edges on all sides
            puzzle.edge[Point(r, c, Direction.TOP)] = True
            puzzle.edge[Point(r, c, Direction.LEFT)] = True
            puzzle.edge[Point(r + 1, c, Direction.TOP)] = True
            puzzle.edge[Point(r, c + 1, Direction.LEFT)] = True

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            arb = tuple(
                filter(lambda x: puzzle.surface.get(Point(*x)) is None or puzzle.surface[Point(*x)] not in Color.DARK, ar)
            )
            if len(arb) == 0:
                continue  # drop holes

            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            self.add_program_line(count_area_pass(2, _id=i))

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
