"""Akari (Light up) solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent


def lightup(color: str = "black") -> str:
    """A rule specially designed for akari."""
    tag = tag_encode("reachable", "sun_moon__3", "branch", "adj", 4, color)
    initial = f"{tag}(R0, C0, R, C) :- grid(R, C), sun_moon__3(R, C), R0 = R, C0 = C."
    propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), {color}(R, C), adj_4(R, C, R1, C1), (R - R0) * (C - C0) = 0."
    constraint1 = f":- sun_moon__3(R0, C0), sun_moon__3(R, C), |R0 - R| + |C0 - C| != 0, {tag}(R0, C0, R, C)."
    constraint2 = f":- grid(R, C), not black(R, C), not sun_moon__3(R, C), {{ {tag}(R0, C0, R, C) }} = 0."

    return initial + "\n" + propagation + "\n" + constraint1 + "\n" + constraint2


class AkariSolver(Solver):
    """The Akari solver."""

    name = "Akari"
    category = "var"
    aliases = ["bijutsukan", "lightup"]
    examples = [
        {
            "data": "m=edit&p=7VTfa9swEH73XxH0rAfLsh1Hb1nX7CVLt6WjBGGM47nENK4zJx5DIf97706idmk2usE6BkPR3XefztKX04/91y5vSy58/MmEg4cWioR6kMTUfdeuq8O2VCM+7Q6bpgXA+dVsxm/z7b70tMtKvaOZKDPl5p3STDDOAuiCpdx8VEfzXpklN0sYYjwEbm6TAoCXPbyhcUQXlhQ+4IXFY4ArgEXVFtsym8MoMB+UNtec4Tpv6GuErG6+lczpwLho6nWFxDo/wJ/Zb6qdG9l3X5q7zuWK9MTN1MpdnZEre7kIrVxEP5G77+6zumnuf0tufpe31Tmlk/R0gop/Aq2Z0ij7cw+THi7VkcmAqZCzSJCLbTSW5BJLTiwpfMsKEVofOF46PnR8jDFMv3DT64CP7W7TMlo8hricZiOohyNw4cE4Chh8jUIGIQkaxihsGKPAwWwkdBij4CfLk/THGeAvCHUEuyI7IxuQvYYCciPJviXrk43IzinnkuwN2QuyIdmYcsa4BS/eJJ+pgDMJ5QAXRuSiCThb5qFSytISj0R/tv6QfC3t4/C0Rf8el3qaLbv2Ni9KuFCLrl6X7WjRtHW+hXi5yXclg0fs5LHvjDoUGN7E/+/a679rWH3/hRfn+e34O/dYQ2Gl4OaKs12X5VnRwLGCsmk4H2H8azxcufP50Xk+mvxgnud6Xr1q8IK43U69Bw==",
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
        self.add_program_line(defined(item="black"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line("{ sun_moon__3(R, C) } :- grid(R, C), not black(R, C).")
        self.add_program_line(adjacent())
        self.add_program_line(lightup(color="not black"))

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
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="sun_moon__3"))

        return self.program
