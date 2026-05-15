"""The Kuromenbun solver."""

from typing import List, Optional, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode
from noqx.rule.neighbor import adjacent


def area_src_color_connected(
    _id: int,
    src_cell: Tuple[int, int],
    exclude_cells: Optional[List[Tuple[int, int]]] = None,
    color: str = "black",
    adj_type: Union[int, str] = 4,
) -> str:
    """A rule to collect all the color cells that are reachable to a source cell in an area."""
    r, c = src_cell
    tag = tag_encode("reachable", "area", "src", "adj", adj_type, color)
    initial = f"{tag}({_id}, {r}, {c}, {r}, {c})."

    if exclude_cells:
        initial += "\n" + "\n".join(f"not {tag}({_id}, {r}, {c}, {exc_r}, {exc_c})." for exc_r, exc_c in exclude_cells)

    propagation = f"{tag}({_id}, {r}, {c}, R, C) :- {tag}({_id}, {r}, {c}, R1, C1), area({_id}, R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    return initial + "\n" + propagation


def count_menbun_adjacent_color(
    target: int, _id: int, src_cell: Tuple[int, int], color: str = "black", adj_type: Union[int, str] = 4
) -> str:
    """A rule to count the number of adjacent color cells to a connected component."""
    r, c = src_cell
    tag = tag_encode("reachable", "area", "src", "adj", adj_type, color)
    rule = f":- #count {{ R, C : {tag}({_id}, {r}, {c}, R0, C0), grid(R, C), not {color}(R, C), adj_{adj_type}(R0, C0, R, C) }} != {target}."
    return rule.replace("not not ", "")


class KuromenbunSolver(Solver):
    """The Kuromenbun solver."""

    name = "Kuromenbun"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVRb9o8FH3nV1R+9oPtxImdl6nr6F46+n2jU1VFCFGarmggOiDTFMR/77k3TrFQtW6aWvVhCpjDybnX5147zvp7PVlV0uNKnFRS40qc4q9L6aPCdTHbzKviSB7Xm7vlCkDK89NTeTuZryvZK4Ns1Ns2vmiOZfOxKIUWUhh8tRjJ5v9i23wqmr5shrglpBtJsajnm9l0OV+uBHMaurM20AD29/CS7xM6aUmtgAcBA14BTmer6bwan7XMf0XZXEhBc7/naIJisfxR0WTkjf5Pl4vrGRHXkw0qXN/N7oVMcGNd3yy/1UGqRzvZHLcVDLsK4OZXFSBJVwHBtgJCT1RAhb1sBX6022FxPqOGcVFSOV/20O3hsNhiHBRbYXxXfLuCItFEJBGREPEuIiwRWPKOSFkREZYVUYjlWaKkmSEii4j8QJErImxE8CyRwrHTaFrHOSLCs48oxDsi0j2h1WG5WmXE5DFz6F4bTuwiJuG5HzOju5p7fMXjKY+GxwssgWwSHj/wqHi0PJ6xpo+V0T6T2iOtQUafA8M8YwcMS4QdaQL2XhqNvgLjVxoySdhYaZI21iR5hDPgNr9JSIPCGTtpLNpC2Ko9TpHfYlUYQ5O28+K+NFna4iyVJg85c8zlg94h9hEj1oVYB40LfjxOJIVF7vJkwX8Gb1nwlsEzbRXGFNvlhE8fYn2CPEFPtZsOI9aEWINYE+Y1VEtXI2qxoRZLHoJeU56gV+itbr1pqkuFnhPf+VcJcMijkEeFWih/GvQp9PToMIY+jealJ4gx5rXBv4V/G/ygRuOD3kNPO50x9J702ESXvJVOeEx5zHiL5XQG/OYpgc5yYvLs2iPj77f2s95KLAm9pOLLvi1m1CvFsF7dTqYVTuj+zdfqaLBcLSZz/BvUi+tq1f3H23LXEz8Ff0usGwX/e4G+4RcoLZT6o9foKzwTz9gp0XDjZXMuxX09nozRbO7XkzzKJh4H0JN6HDQvqsfTfah/9W7ikBn1HgA=",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            excluded: List[Tuple[int, int]] = []
            for r, c in ar:
                num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
                if num is not None:
                    self.add_program_line(f"not gray({r}, {c}).")
                    self.add_program_line(area_src_color_connected(i, (r, c), exclude_cells=excluded, color="not gray"))
                    excluded.append((r, c))

                    if isinstance(num, int):
                        self.add_program_line(count_menbun_adjacent_color(num, i, (r, c), color="not gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
