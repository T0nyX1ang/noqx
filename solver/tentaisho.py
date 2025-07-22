"""The Tentaisho (Spiral Galaxies) solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false, tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_src_color_connected


def galaxy_constraint(glxr: int, glxc: int) -> str:
    """Generate a constraint for spiral galaxies."""
    r, c = (glxr - 1) // 2, (glxc - 1) // 2
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")
    rule = f":- grid(R, C), {tag}({r}, {c}, R, C), not {tag}({r}, {c}, {glxr} - R - 1, {glxc} - C - 1)."
    rule += f":- grid(R, C), {tag}({r}, {c}, R, C), edge_top(R, C), not edge_top({glxr} - R, {glxc} - C - 1).\n"
    rule += f":- grid(R, C), {tag}({r}, {c}, R, C), edge_left(R, C), not edge_left({glxr} - R - 1, {glxc} - C).\n"
    return rule


class TentaishoSolver(Solver):
    """The Tentaisho (Spiral Galaxies) solver."""

    name = "Tentaisho"
    category = "region"
    aliases = ["spiralgalaxies"]
    examples = [
        {
            "data": "m=edit&p=7VZfb9NADH/vp5ju+R7uX5JL3soovIwOyNBURVGVdhmr6JTRLgil6nef7cuoIHcb2tAQEkpj/2I7zs++f91+batNzaXAn7YcNFxGWrqVjekW/XW2ul3X2REft7dXzQYA56dTflmtt/Wo6IPK0a5Ls27Mu7dZwRTjdEtW8u5DtuveZd2Mdzm4GDdgOwEkGVcAJwd4Tn5Ex84oBeBpjwHOAC5Xm+W6nue5M73Piu6MM/zQK3odIbtuvtXMvUfPy+Z6sULDorqFYrZXq5ves20vmi9tHyvLPe/Gju/kni9+peerD3wROr6IPHyxjOfzrS8+19t24SOblvs9dP0j0J1nBTL/dID2APNsx2LJMsNZrJzSThlSSa9SUtaSSl2IFO4NKRKnZdxrFy2VSyz1ve7jdf++dsmlwXggM812ICXJGRDTYC8kFHzoEjSORZDGY44FmNXQHHnNFjh5klj85DBaan8WqaFknz1C+zC9xO764i3mH8Zr469V47h47EYF7MTTY7cYP+QTqUDrA32IAl2OEn+bY4V1eQYr0M84UG+cwIz02a2/b4nw80wkTGGfPcHx+jUPTM83NEkVyTNYSrzTJF+TFCQjkicUMyF5TvKYpCEZU0yCi/E3l+twnTyNDosELJjUwiBJaC4BBd0kgNMOgZYJ17h8NWILGBz60UoK7Q6Nn6/o37OVo4Ll7eayWtawy05gvz2aNpvrag1P+VV1UzM42/Yj9p3RXWg8Kf8fd3/nuMMREC+8ip67qAuYCzKRvDvl7KadV/NlA3MLWveAYwITSsG/MCNY0J1ypZ/oNkoFHJEIJTSCq8j8wYSP1Pfg937sWkG328j8btgNAw4RYAvbZsBhhoW/+PyD3bgc3QE=",
        },
        {
            "url": "https://puzz.link/p?tentaisho/19/22/hafheneweo2ffneneyerfgezy0eg4fifhafnezgfnfmegepel3epfzzt6989ezq7ehfehfwfnezk2dezq4b88fzveweofznfhefezzu54ffzzmedb4b3ezuejflexezg4fl7ezel72eregfztflefzzheifhbeztewen9ekejemer6eret8fpe",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))

        reachables = []
        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(symbol_name.startswith("circle_SS"), "Invalid symbol type.")

            if d == Direction.CENTER:
                reachables.append((r, c))
                self.add_program_line(galaxy_constraint(r * 2 + 1, c * 2 + 1))

            if d == Direction.TOP_LEFT:
                reachables.append((r - 1, c - 1))
                self.add_program_line(galaxy_constraint(r * 2, c * 2))
                self.add_program_line(f"not edge_top({r}, {c - 1}).")
                self.add_program_line(f"not edge_top({r}, {c}).")
                self.add_program_line(f"not edge_left({r - 1}, {c}).")
                self.add_program_line(f"not edge_left({r}, {c}).")

            if d == Direction.TOP:
                reachables.append((r - 1, c))
                self.add_program_line(galaxy_constraint(r * 2, c * 2 + 1))
                self.add_program_line(f"not edge_top({r}, {c}).")

            if d == Direction.LEFT:
                reachables.append((r, c - 1))
                self.add_program_line(galaxy_constraint(r * 2 + 1, c * 2))
                self.add_program_line(f"not edge_left({r}, {c}).")

        fail_false(len(reachables) > 0, "Please provide at least one clue.")
        for r, c in reachables:
            excluded = [(r1, c1) for r1, c1 in reachables if (r1, c1) != (r, c)]
            self.add_program_line(grid_src_color_connected((r, c), exclude_cells=excluded, adj_type="edge", color=None))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

            for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
                direc = "left" if c1 != c else "top"
                self.add_program_line(f"{prefix}edge_{direc}({r2}, {c2}).")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        tag = tag_encode("reachable", "grid", "src", "adj", "edge")
        spawn_points = ", ".join(f"not {tag}({r}, {c}, R, C)" for r, c in reachables)
        self.add_program_line(f":- grid(R, C), not hole(R, C), {spawn_points}.")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
