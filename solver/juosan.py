"""The Juosan solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs


def jousan_constraint():
    """Constrain consecutive lines. Black for horizontal, not black for vertical lines."""
    rule = ":- grid(R, C), grid(R + 2, C), black(R, C), black(R + 1, C), black(R + 2, C).\n"
    rule += ":- grid(R, C), grid(R, C + 2), not black(R, C), not black(R, C + 1), not black(R, C + 2).\n"
    rule += f'line_io(R, C, "{Direction.LEFT}") :- grid(R, C), black(R, C).\n'
    rule += f'line_io(R, C, "{Direction.TOP}") :- grid(R, C), not black(R, C).'
    rule += f'line_io(R, C, "{Direction.RIGHT}") :- line_io(R, C, "{Direction.LEFT}").\n'
    rule += f'line_io(R, C, "{Direction.BOTTOM}") :- line_io(R, C, "{Direction.TOP}").\n'
    return rule


def count_lines(area_id: int, num1: int, num2: int = 0):
    """Limit the number of horizontal or vertical lines."""
    rule = f"count_area({area_id}, N) :- #count{{ R, C: area({area_id}, R, C), black(R, C) }} = N.\n"
    rule += f":- not count_area({area_id}, {num1}), not count_area({area_id}, {num2})."
    return rule


class JuosanSolver(Solver):
    """The Juosan solver."""

    name = "Juosan"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VdtT9tIEP7Or6j2a1c6r9dev0inU0qh1x4EaEE5EqHIBAOhDuacGHpG/e99Zj1u4iRQCdTjTjolWT87MzszOzPenUz/KpMilcqhrw4lnvh4KrQ/NzT25/DncDzL0viV7JSzy7wAkHJve1ueJ9k0lR+OL3c2887d286ft+Gs31fvnPK907vavnr9cfLH+7Eu1HY33N/d3x27F53fN98cmK3XZr+cHs3S24OJenN11D883+9dRO7fW92+V/X3HP9D//yX287RrxsD9uFk476K4qojq3fxQLhC2p8SJ7I6iO+r3bjqyuoTWEIq0HaAlJAu4NYc9iyf0GZNVA5wF1jXy44BR+NilKXDnZqyHw+qQynIzhu7mqCY5LepqFXY+SifnI6JcJrMEKrp5fiGOdPyLP9csiwUikmZzcajPMsLIhLtq6w69RZ6a7ag51sgWG+B0PIWeI8/eQvR+i18RXo+YhPDeED7OZrDcA4/xfcYu3ZU8b2IHA8KPBuWSLnApsauA0y1aSckVDOUowwmmieaJg3HIzGXJ8ECRzmkTfxWh18pn3gsqAzxag+UCkkFK3e9cK7CXRTT1qFm4pPbPPGsQ6QAGzy229y2o2vHQ0RBVtqOb+3o2NG3446V2UJYXKWl6wYidlHkygeOGOOt1PCEsOsAwxGLA+l6inEErGusIUNhsdgDxpYIe6D7TPcUsM8Ydn2260Heb+RhlyJA2AfdMN2Hb4Z98+FDwD74OEECxIWwga2AbRk6WZgewG7IdgOXThvG0B+y/gD6Q9YfwIeIfQghH7F8CJmIZXBiaUq2xSEw2wojYI5JBBnFMlEAzD5HkFG1DHQA1z5rRwHXfmrHA659wzqpXaYjX5rzhXXAjQxscb6wDrj2B+uAa5+xTmrOHdYBswxypzl3WAdc7xfrpPbZT+ROc+6wDphlkEfNeYQOYI4n1YDmmEMP6mBeD039UN69ph4QW7Zra8BraoPqrakBqhOWp1wb1mOQX9PUAPJlOP4GdgO2G1BtsDzlPWjqAXbpDW7yHrDdkGqGdUZYGzW5gz8R+xOhxrgebB4dji3lkesBz+/1gCcwx5muQq4H5ByY40l5VE1+qWaa/CJfqskj1QDrcakGFvLC76PNBccWT84pXvqeffU37ejZ0dgjIaBj8wkH63NOn9od4TnoBFzES0thVCQNHcn6ES8HKFhqIdof/79HO9kYiF6SZbj8uuXkNC1edfNikmQCHYiY5tlwWhbnySgdpl+S0UzEdRO0yGnRrq2OFinL85tsfL1OQ8NqEccX13mRrmURMT27eEgVsdaoOs2LsyWf7mjHrb3YBrFFqruKFmlWoGVYmCdFkd+1KJNkdtkiLLQXLU3p9VIwZ0nbxeRzsmRtMg/H1w3xRdgf3b/S+79d/Je3i5Qq50XOtqcftQNE/PvJKKs9KW7KYTLE1gT+oEjLNrggDC6IB9kh2NGT2Y8qf55rP1jt4Xb0cMM9jW20lgb96kusfibbicDGC/9Tgvq48h8m9DnF9DzbL+l505CssP/x88JeQ3nxSE8wZy6T13QGoD7SHCxw19Ef6AMWuMv0lUufnF2990Fdc/WDunz7g7TaAIC40gOA9kAbQFqXOwHyarkZIFMr/QCZWmwJBuKqzKfJtTjZ+AY=",
        },
        {
            "url": "https://puzz.link/p?juosan/21/12/4ql08qtg9qt59ul5bunltnn9tntd72ta72h636h5b641bm04vmcvjo0fu1vo3s6fhuv1u0gf7fvpjo0fvjro0fs3vu0tvvgg33g42554342h553444g2g24211g121g2221341225h121g252442224465g25g1g2425g273",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())
        self.add_program_line(jousan_constraint())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, f"corner_{Direction.TOP_LEFT}"))
                if isinstance(num, int):
                    self.add_program_line(count_lines(i, num, len(ar) - num))

        for (r, c, d, _), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
