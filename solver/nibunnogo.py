"""The Nibun-nogo solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_covering
from noqx.rule.reachable import grid_branch_color_connected


def constrain_branch_size(max_size: int, adj_type: int = 4, color: str = "gray") -> str:
    """Constrain the size of branches."""
    tag = tag_encode("reachable", "grid", "branch", "adj", adj_type, color)
    return f":- grid(R0, C0), {color}(R0, C0), #count {{ R, C: {tag}(R0, C0, R, C) }} > {max_size}."


class NibunNogoSolver(Solver):
    """The Nibun-nogo solver."""

    name = "Nibun-nogo"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7Zb/T9pAFMB/568w96uXrN/A0mRZENHpsKJAmDSEFCxQbakrLboS/3ffvRZpe6fbks1syQI9Hp/37u59ad919S22Q4fKEvuqOoVf+Giyjpei1/CSsk/PjTzH2KONOFoEIQiUXph0Znsrh55dL9rNoPFw1Pi61qPhUD6R4lNpcHt8u3/lfzl11VA+NvXOeefcVeaNz83Dy1prv9aJV/3IWV/68uFtf9ibdQbzuvK9ZQ61ZHghVc+Gsw/rRv9jxcpcGFU2Sd1IGjQ5MSwiE0oUuGQyosmlsUnOjcSkSRdUhOrA2qmRAmJrJw5Qz6RmCmUJZDOVayBegzh1w6nnjNupYcewkh4lbJ9DnM1E4gdrh2R+sP/TwJ+4DEzsCDK1Wrj3mWYV3wR3cWYrs6mxF7nTwAtCBhl7okkjDaG7DYHtnIWg7kJgYhoCkwQhsGnFEGDH3xtCXRzCE5TnCoIYGxaLp78T9Z3YNTYwmsaGKKrMpkowNy0iEI0RKOoL0dBGyxO1bFOtbVO7JTWFI/XyLJ2z0XEdNU8OyjZ19CdHVBltch6qCpJPcDdtiaqXIlU1jDS/joa75zxUq5xNGunLOpBIGdN5/ZJOUBTu3SynPMbECjDLLo9xYx5jngWYJZvHmHEBFq+NuecxFoDDaRV4jInnMWZfgIWepHUQYIE11OIYK6Lg2IN7niYqjkc4SjhWcWyjTQvHAY5NHDUca2hzwJ6an3yuiCoRQ2fJIIaSPmT5O+QP+Wap6bFR/FT/PTaqWKQbhzN76kDTM2N/4oR7ZhD6tkfg5CGrwBuvUv3YebSnETHSwy+vIUYUxhla4hIFKy8I7j13KVpgqypAd74MQkeoYtC5mb+2FFMJlpoE4U3Jpwfb84qh4GtBAaX3eAFFIZwUuf92GAYPBeLb0aIAcqdKYSVnWcplZBddtO/s0m7+Lh1PFfJI8LIUqsA7C1Ty/3vCX/2ewIol/dLbwjs0sh+4Y0HGodUlF5Tcx2N7DDFhEpHLJa6O3t17fCyC8I0WtVOWsaBTAX2jWeW0Iv5KX8ppy5xrQsxZvg8BFbQioOVuBIhvSAC5ngTslbbEVi13JuZVuTmxrbj+xLbKtyhrVHkG",
        },
        {"url": "https://pzplus.tck.mn/p.html?nibunnogo/10/10/i16ai3ch22aidj7cjch6bmce53drbg6ddibch2dagcib", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_branch_color_connected(color="gray"))
        self.add_program_line(grid_branch_color_connected(color="not gray"))
        self.add_program_line(constrain_branch_size(max_size=5, color="gray"))
        self.add_program_line(constrain_branch_size(max_size=5, color="not gray"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_covering(num, (r, c), Direction.TOP_LEFT, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
