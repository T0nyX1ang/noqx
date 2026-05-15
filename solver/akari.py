"""The Akari solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent


def lightup() -> str:
    """A rule specially designed for akari."""
    tag = tag_encode("reachable", "sun_moon__3", "branch", "adj", 4, None)
    initial = f"{tag}(R0, C0, R, C) :- grid(R, C), sun_moon__3(R, C), R0 = R, C0 = C."
    propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), grid(R, C), adj_4(R, C, R1, C1), (R - R0) * (C - C0) = 0."
    constraint1 = f":- sun_moon__3(R0, C0), sun_moon__3(R, C), |R0 - R| + |C0 - C| != 0, {tag}(R0, C0, R, C)."
    constraint2 = f":- grid(R, C), not sun_moon__3(R, C), {{ {tag}(R0, C0, R, C) }} = 0."

    return initial + "\n" + propagation + "\n" + constraint1 + "\n" + constraint2


class AkariSolver(Solver):
    """The Akari solver."""

    name = "Akari"
    category = "var"
    aliases = ["bijutsukan", "lightup"]
    examples = [
        {
            "data": "m=edit&p=7VbbbuIwEH3nKyq/1tLGuXCJtA8phW67lNICYiFCKNAAaRPM5kK7Qf33ju20JJBU7Up7k1Yh45kzZnzGMScE3yPLtzGR2EepYhjhUkmV33K1zG8puXpO6Nr6ETaicEl9cDC+ajbx3HIDG18Ml606NR5OjW+bajgakTMpOpcGd8274xvv67mj+KTZrnYuO5eOvDC+1E+uy43jcicK+qG9ufbIyV1/1Jt3Boua/KPRHqnx6ErSLkbzTxuj/7lkJhzGpW1c02MDx2e6iQjCSIaboDGOr/VtfKnHXRx3IYWwClhLTJLBbezcAc8zry5AIoHfFn4F3CG4M8efufakBVlAOroZ9zBi65zwbzMXeXRjo4QHi2fUmzoMmFohbFWwdNZJJohu6X2UzIWCyIvc0JlRl/oMZNgTjg3RwjCnBWXXAnNFC8x7o4UgWk08Slc/1YJ1b/lOHvtaPvsneDI3wH+im6yV/s6t7tyuvkWKjHQVI43woSyiisKHqgBrAiSSQAlRxSgnuJLgaoKXWQzl20l5U8YVcSr4MiZ5DdlyJjqCPUoAtnAqzwikvs2IpEJOKB0zYumYEUxV40TTMSOcWZ5Tf60ALRB9C3bIbZNbmdsebCCOFW5PuZW41bht8TkNbgfc1rlVuS3zORX2CN79kCSkyxipGh+0Ggxif9MUEW9PYedjd9B+EW9TEdqUvbR/DxuXTNSN/Lk1s+HX1Y68qe0ftanvWS7E3aW1thGoHAqoOwnEvIn9aM1CpAuhTWcy2IrXykAupWvXWeVVeEllQGexor6dm2KgfbsoKsVSOaWm1L/d4/RguW62F/4SykBCfDNQCGqUji3fpw8ZxLPCZQZIqXCmkr3a28zQylIU2pepvduOpxJ6RPyGow8vy/+vpL/3lcSekvROzTvUtz8jwSZstkJwfIXROppYE+gJwR8fbMI5Ussfw0E08+dr+bhWK6hTwOcAhxOci8OxKO5rWMC/GFeUj+EfqPPbTwPXF+q/Ifa75D6cI/mAvqH6qWweXiDwqew+fqDmjOyhoAOao+mA7ss6QIfKDuCBuANWoO+s6r7EM1b7Ks+WOhB6tlRa619UZ1x6Bg==",
        },
        {
            "url": "https://puzz.link/p?akari/17/17/g666.g6.g6.x6.x6.x6.obl6.gbi6cv.gblcmbl7cv6bi66blam6.x.gbv.gcv66.g666.g.g",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?akari/20/20/................................h............h1...h............i...i...........i1.bg........t.....i6cn...hbibi1b..kbl1b0.g6bgc..l..k.j1.l..hciam...i6.q...v0...bs....b.b..h2..h....i..h..i..h....i..h..b..h....h1..h...h..h....................../",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="sun_moon__3"))
        self.add_program_line(adjacent())
        self.add_program_line(lightup())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="sun_moon__3"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(symbol_name, "sun_moon__3")
            self.add_program_line(f"sun_moon__3({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"hole({r}, {c}).")

            if color == Color.WHITE:
                self.add_program_line(f"not sun_moon__3({r}, {c}).")

        self.add_program_line(display(item="sun_moon__3"))

        return self.program
