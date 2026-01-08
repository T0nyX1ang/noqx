"""The Double Back solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, fill_line, grid
from noqx.rule.helper import fail_false, full_bfs
from noqx.rule.neighbor import adjacent, area_border
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import count_area_pass, single_route


class DoubleBackSolver(Solver):
    """The Double Back solver."""

    name = "Double Back"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VRRb9owEH7nVyA/3wOxEw/yxjrYC6PbylRVUYRCSFfUsHRApsqI/97Pl0t5STVplXiaLH/6cvfFdz6fvf9dZ7uCLIYZ0oACDG0tzyAMeQ5kLDaHsoj7NK4PD9UOhOh6OqX7rNwXvURUae/oRrEbk/scJ0or4hmolNy3+Oi+xG5C7gYuRQFsM7BAkQadnOkt+z27aozBAHwuHPQONN/s8rJYzhrL1zhxC1I+zkf+21O1rf4UqvmNv/Nqu9p4wyo7YDP7h82TePb1unqsRRukJ3LjJt1ZR7rmnK6nTbqedaTrd/HudMvNr+K5K9NRejqh4t+R6zJOfNo/znR4pjfxEThnDBjvGKeMmnEBKTnD+IlxwBgxzlgziY8q0JoCo1WscbAafWJsww3sodiNATfCI/BIuO8r0YfQR6IPoY9EH0IfiT6EPhJ9BL0VfQS7FbvPR8u/GuvoUDj6V7dxYTdij3yslkPTxrJ+fVnHQmNFY6GxrQa5cVwU45ZLcsUYMlou1Qdf84uditJ+76MhKeMPxRMUxFPDzHtNc3R/zTnxpXwd2Oq/8rSXqJt6d5/lBdp2hvbtz6vdNivxNVn/fP3Cc3HqqWfFM0HNKfz/glz+BfHVH1z4HXnvBUpQWOl0cteknupltswrdBhq1zrR/N1OXJpuBy7RW8sZON+M1e28eM1wh9W6qldl0V9l+aNKey8=",
        },
        {
            "data": "m=edit&p=7VZdTxs7EH3Pr0B+9sP6a7/eKBfuSwq9N1QIraIoCUuJCDc0IRXaKP+dM+MxuVWDQEJCqlRt1j4ZOzPHczx2Vt/X42WrTUYfV2r0eLwp+bVlzm8mz/nsYd7WB/pw/XCzWAJofXZyoq/H81Xba2TWsLfpqro71N3fdaOs0vwaNdTdP/Wm+1x3A90NMKS0h60PZJS2gMc7eMHjhI6i0WTAp4IBLwGns+V03o760fKlbrpzrSjOJ/41QXW3+NGq+DP+Pl3cTWZkmIwfsJjVzexeRlbrq8XtWuaa4VZ3h5Fufw9dt6NLMNIltIcureLddOez/9rHfUyr4XaLjP8LrqO6Idpfd7DcwUG9US5TtdfKudjlsau4K2zsQuxK7krDnTFe+iL2NjoyNnoyIboyIfoyeXRmcvKG4Kf1Bq3h9pLbE24tt+dgqDvH7V/cZtwGbvs85xj0rbHaWoSy2FPGA4Ml4wCM0IwLbR1oM8YWdqBC2GbAWAZj2L3YnQEGTcIe/mkpjOGTlkM4IFYusQJKosDyGSNWIbFCBYx0EM4Rq5BYOXwW4rNArFJiFfBZis8SsSqJVRbaZeKzLIGFZ5VrZyRuhTlG5lSYY9KcCjhygA/gGAs+gCMHl3ngGBc+tLMyB7l1klv4AIbUjANw5Aabdj7GhQ1YYuHgcCFycB7nSIhrx1xg8e/hM4hPDw5BOHisK5d1WdJRckUaJU1Jo6SjQ96c5DA4aCR5Jo0kFvqdjqSXxGW9JC76/+kL7RIH0itPOmJ+0r0gTSXnpCPVC2PSV+YX4JN0L2ifSFzStxQ+fKSKvSLdxQ59oeuzvtD1Wd+0N1hT2Q+saZa0Rm4zyTnpmyXdaT/EdbG+aW+Qpmk/oEacSfqS1mJ30NoljaBp0p109ElfaOeJMwr0gsv0iFvPbc7lW9Dx88YD6v0nhfIOfJAzldMpRwCbjerb0VoTgo32QbTRznLxiHl1HY2LN+TPT/j9bMNeowbr5fV42uJW6eN2OThdLO/Gc3w7vvr2/A23+banHhW/jaM/B38u+I+/4Cn72YdV0RuL4RU6DRIr1ae7M63u16PxaLrADkPueDAW5AuDsUb3D6LK9w+g6l+OhUL/ZfDDc4YzRF0t1pN5ezAZT2/VsPcE",
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

        for (r, c, d, _), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
