"""The Lithersink solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges


def limit_adjacent_vertices(r: int, c: int) -> str:
    """Generate a rule that counts the adjacent vertices around a cell."""
    v_1 = f'edge({r}, {c}, "{Direction.TOP}")'
    v_2 = f'edge({r}, {c}, "{Direction.LEFT}")'
    v_3 = f'edge({r}, {c - 1}, "{Direction.TOP}")'
    v_4 = f'edge({r - 1}, {c}, "{Direction.LEFT}")'

    rule = f":- {{ {v_1}; {v_2}; {v_3}; {v_4} }} = 2.\n"
    rule += f":- {{ {v_1}; {v_2}; {v_3}; {v_4} }} = 0.\n"
    return rule


def border_color_connected(rows: int, cols: int) -> str:
    """A rule to ensure all the color cells are connected to the borders of the whole grid.

    This rule is specially designed for the lithersink puzzle.
    """
    adj_type = "edge"
    tag = tag_encode("reachable", "border", "adj", adj_type)
    borders = [(r, c) for r in range(-1, rows + 1) for c in range(-1, cols + 1) if r in [-1, rows] or c in [-1, cols]]
    initial = "\n".join(f"grid({r}, {c})." for r, c in borders) + "\n"
    initial += "\n".join(f"{tag}({r}, {c})." for r, c in borders)
    propagation = f"{tag}(R, C) :- {tag}(R1, C1), grid(R, C), adj_{adj_type}(R, C, R1, C1)."
    constraint = f":- grid(R, C), not {tag}(R, C)."
    return initial + "\n" + propagation + "\n" + constraint


def not_single_tree(rows: int, cols: int) -> str:
    """Generate a rule to avoid the case where all edges are connected as a single tree."""
    return f":- #count {{ R, C, D : edge(R, C, D) }} = {(rows + 1) * (cols + 1) - 1}."


class LithersinkSolver(Solver):
    """The Lithersink solver."""

    name = "Lithersink"
    category = "var"
    aliases = ["lithersink"]
    examples = [
        {
            "data": "m=edit&p=7Vbvb7JIEP7uX9Hs125yLCAiyX2wVnvtWWtbjVeJMWhRaUF6/LA9jP97Z1Z92UXaey9Nmrvkgowzz+zOzg7Ds8R/pk7kUqbgTzMp/MOlM5PfqmnwW9lffS/xXeuENtJkGUagUHrTbtO548cuvXpYdpph4/W88cfaTEYjdqGkl8rwqf10ehf8fulpEWt3zd5179pTF43fmme3RuvU6KXxIHHXtwE7exqM+vPecFFX/2p1R3o2ulGqV6P5L+vG4NeKvc9hXNlkdStr0OzCsolGKGFwq2RMs1trk11bWZdm9+AilI0pCVI/8WahH0bkgGUd0GCSCmorV4fcj1pzBzIF9O5eB/UB1JkXzXx30tkhPcvO+pTg2md8NqokCNcuLoZ5oT0Lg6mHwNRJoHzx0nshVANHnD6Gz+l+KBtvadbY7aD1kzuAIIcdoLrbAWolO8CNfXkH7uPCfStJvj7ebuG53EH6E8vGnQxy1czVe2sDsmttiMZgqgatBtMhmqbKpi6bVTCxL/dmTfaakqnjXDU3cXBuVhUwscn3pibNrcqhDDlJAyPnaRhyGjUMlUeuyWnUDNlbmFuXBpuYZL6QiXMFEwfnZh1Ll8+ty7ViihyLKfKOmYLBRRujCzYrxGNyMoxhyURb3gpTsYaijekK41WcL/h5Y4i23AqMP/y8kEyXO4fphXz1Qn5VjC/ahXi8BYT1DayfaMs9wQysp+gXmwSanfGWf+CyzaXKZR/eCJppXJ5zqXBZ5bLDx7S4HHLZ5FLn0uBjavhO/aO37uvpEB2fX90ExmUqVVVoBu1vU7S13akiX9X/Hjau2KQFFHjSDaPA8YEdu2kwdaODDWcTiUN/EqfR3Jm5E/fNmSXE2h2PokfCVjyGBPlh+OJ7q7IIB5cEeotVGLmlLgSRtj8Iha6SUNMweizk9Or4vrwX/ukgQbvDRYKSCE4OwXaiKHyVkMBJlhIgnJNSJHdVKGbiyCk6z05htSAvx7ZC3gi/4fWFF/b/D4l/64cEPiPlm4ntqzxrQ62BG2l2Q8lLOnEmUGgCX6sUHT/I8sj97bvgb0UYfUJRubMIlxAVoJ9wleAtwz+gJcFbxI84CJM9piFAS5gI0CIZAXTMRwAeURJgH7ASRi0SE2ZV5CZc6oiecCmRoWwS+16ydCMo2TMZV94B"
        },
        {"url": "https://puzz.link/p?lither/8/8/g02881d3667c63c338c6b086cid12185bd", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col, with_border=False))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(border_color_connected(puzzle.row, puzzle.col))
        self.add_program_line(not_single_tree(puzzle.row, puzzle.col))

        for r in range(puzzle.row + 1):
            for c in range(puzzle.col + 1):
                self.add_program_line(limit_adjacent_vertices(r, c))  # not very elegant, but works correctly

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
            self.add_program_line(count_adjacent_edges(int(num), (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
