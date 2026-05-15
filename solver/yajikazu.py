"""The Yajilin-Kazusan solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.variety import yaji_count


class YajiKazuSolver(Solver):
    """The Yajilin-Kazusan solver."""

    name = "Yajilin-Kazusan"
    category = "shade"
    aliases = ["yk", "yajisan-kazusan"]
    examples = [
        {
            "data": "m=edit&p=7Vbdb5swEH/nr6j8fA/+gGB4y7pmL1m6LZmqCiFEGFWjEdGRME2O+N93PqOFFSp1D2ulabJ8On6+j5/ts83hW5s3JQgfIlAaOAhsQcjxg4MWmjrv22Z3rMr4Aubt8b5uUAG4XizgLq8OpZf0Vql3MlFs5mDexQmTDKgLloL5GJ/M+9iswKxxiIFGbImaYCBRvTqrNzRutUsHCo76ygUUqN6iWuyaoiqzpUM+xInZALN53pC3Vdm+/l4yF4K+i3q/3Vlgmx9xMof73UM/cmi/1F/b3lakHZi5o7ueoKvOdNUvumqarvz7dKO063DZPyHhLE4s989nVZ/VdXzqLK8T86V19TOFbOwOYUQ/sJDM5ACKKEEmzlDALcSHVjN/5DijWGoYPgyd1SBWGDkSA0etRo5ROIZ6XgNHwcWImODK5Ry4CiEcxofYbMKuTzuMJ/XYTkZjTHHH7zdsgouayKsmcvh8AhMTmB4tqJiF4/mGarRjQsuxnY4erQFWj6AauiW5IClJbrDEwCiSb0lykgHJJdlckbwheUnSJzkjm9AW6TPLmNllkliOODvtavoFuCV4RYonW/Bvj6VewtZtc5cXJd5Bq3a/LZuLVd3s84rhpd957Aejnig09/+/A6/0Dtgt4H/0Grz+qU5wdYMQzDWwhzbLs6KuGP5KgMXxzD3GX5w9Hv3U+wk=",
        },
        {
            "url": "https://puzz.link/p?yajikazu/9/9/301040104010103040201030101030103040301030101020304010203030401040404040301010304010401030402030402020203040203040302020204040304020402040201010402020102020402040",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_color_adjacent(color="gray"))
        self.add_program_line(grid_color_connected(color="not gray"))
        self.add_program_line(count(("gt", 0), color="gray", _type="grid"))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            fail_false(isinstance(clue, int) and label.startswith("arrow"), "Please set all NUMBER to arrow sub.")
            arrow_direction = label.split("_")[1]
            self.add_program_line(yaji_count(int(clue), (r, c), arrow_direction, color="gray", unshade_src=False))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
