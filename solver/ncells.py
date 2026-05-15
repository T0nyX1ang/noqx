"""The N Cells solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.reachable import grid_branch_color_connected


def count_reachable_edge(target: int) -> str:
    """Generates a constraint for counting grids in a region divided by edges."""
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")

    return f":- grid(R0, C0), #count {{ R, C: {tag}(R0, C0, R, C) }} != {target}."


class NCellsSolver(Solver):
    """The N Cells solver."""

    name = "N Cells"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VhLbxoxEL7zKyKfffDbu3up0pT0kpK2SRVFK4QIoQ0qiBRCVW3Ef++sdwnEMHZSAn2oWuEM/jye2Znx5yHTb7PupE85o5xTmVD4C4/iCVXaUCuV+7D6OR/cDfvZAT2c3d2MJyBQenp8TD93h9N+I69XtRv3RZoVh7R4m+VEEOo+nLRp8SG7L95lRYsWZwARymHuBCROqACxuRQvHF5KR9UkZyC3ahnESxB7g0lv2O+cVDPvs7w4p6S089pplyIZjb/3SaXmvvfGo6tBOXHVvYOXmd4MbmtkOrsef52RhYk5LQ4rd5sb3JVLd+WDu3KX7g5vx5scTdvzOQT8I7jayfLS609LMVmKZ9n9vPToniizeMcqK0RZUiXqYSIpJ+TKROqpaOapaO5NGOapGO2tsMqzYp2VV8uJJPFUUumt4Ex4ZjiTnhJnam2N9kxz5geFMz8qnBt/RnB/H+m/Npf+e3O15k8V39V9tJ8CrlN/nyrEq2vMmj9mLT7mcXygKLgrjUs3HrtRuPEcKocW0o1v3MjcqN144tY03XjhxiM3Kjcat8aWtfes6tzeHaheiEuaQE0qXgtGVQJwWS2UteaEZCGk9WKhNRUaUi0pkcCB0rJKNulShjVydY22lWwZrIGNZDQouayo9vGj/425diMnzesv/YPWeDLqDoG3WrPRVX+y+A5XxLxBfhD3ySWoqP+3xt5vjTL4bM+nc1uyyCGuD0eUFqeU3M463U5vDEUGwathA7BFYSWDsEgpLME3V6Ct8c0ZwCoIAy2htm0ANkZsBpRRCKAZthUGWI1thRg31mAa8rnv8YI2sPeo0q8CGYL8qkB+ofQUXnoKSk8FSq/Mb4LCUgVgpVMsnkj6jUGCYAwST2MsWvfgusZd1wkVVgTjAv0KBkM5CovnxMowLADGT6zlQdfC8KIFwOC6K0C1q0YhtDlORYt2YjMMrQsCpMjhDgD8pQgE5aJ9VCl6RKK8HGH1yIWzDatHr6vIffS30tnv5YQIXUXILtJBROAnbI4nVHKgDIkTTglznFG4BW20FCVUi8SrxcG45wABnKIwAzZjuG3GwXPcNlchWAAPiwTPdwJBTQLVwgIw/KBEaFMilAa/PBENi3E21hNZg3Q4WiJbaawnQm2gW+HGMRtQBJJKgxcgULc0gRJSAVhjV8hO0x+n2G2O+05PxW7JYoeZ3jETPaEr+/WWL9i0xVq+WK8Q6TSe0OXgMY/BO/xpG+uw/sgufO//Gpk38nbjJw==",
        },
    ]
    parameters = {"region_size": {"name": "Region Size", "type": "number", "default": 5}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.param["region_size"].isdigit(), "Invalid region size.")
        size = int(puzzle.param["region_size"])
        fail_false(puzzle.row * puzzle.col % size == 0, "It's impossible to divide grid into regions of this size!")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(grid_branch_color_connected(color=None, adj_type="edge"))
        self.add_program_line(count_reachable_edge(size))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent_edges(num, (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
