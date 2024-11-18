"""The Tentaisho (Spiral Galaxies) solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_src_color_connected
from noqx.solution import solver


def galaxy_constraint(glxr: int, glxc: int) -> str:
    """Generate a constraint for spiral galaxies."""
    r, c = (glxr - 1) // 2, (glxc - 1) // 2
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")
    rule = f":- grid(R, C), {tag}({r}, {c}, R, C), not {tag}({r}, {c}, {glxr} - R - 1, {glxc} - C - 1)."
    rule += f":- grid(R, C), {tag}({r}, {c}, R, C), edge_top(R, C), not edge_top({glxr} - R, {glxc} - C - 1).\n"
    rule += f":- grid(R, C), {tag}({r}, {c}, R, C), edge_left(R, C), not edge_left({glxr} - R - 1, {glxc} - C).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))

    reachables = []
    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert symbol_name.startswith("circle_SS"), "Invalid symbol type."

        if d == Direction.CENTER:
            reachables.append((r, c))
            solver.add_program_line(galaxy_constraint(r * 2 + 1, c * 2 + 1))

        if d == Direction.TOP_LEFT:
            reachables.append((r - 1, c - 1))
            solver.add_program_line(galaxy_constraint(r * 2, c * 2))
            solver.add_program_line(f"not edge_top({r}, {c - 1}).")
            solver.add_program_line(f"not edge_top({r}, {c}).")
            solver.add_program_line(f"not edge_left({r - 1}, {c}).")
            solver.add_program_line(f"not edge_left({r}, {c}).")

        if d == Direction.TOP:
            reachables.append((r - 1, c))
            solver.add_program_line(galaxy_constraint(r * 2, c * 2 + 1))
            solver.add_program_line(f"not edge_top({r}, {c}).")

        if d == Direction.LEFT:
            reachables.append((r, c - 1))
            solver.add_program_line(galaxy_constraint(r * 2 + 1, c * 2))
            solver.add_program_line(f"not edge_left({r}, {c}).")

    assert len(reachables) > 0, "Please provide at least one clue."

    for r, c in reachables:
        excluded = [(r1, c1) for r1, c1 in reachables if (r1, c1) != (r, c)]
        solver.add_program_line(grid_src_color_connected((r, c), exclude_cells=excluded, adj_type="edge", color=None))

    for (r, c), color_code in puzzle.surface.items():
        solver.add_program_line(f"hole({r}, {c}).")

        for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
            prefix = "not " if ((r1, c1), color_code) in puzzle.surface.items() else ""
            direc = "left" if c1 != c else "top"
            solver.add_program_line(f"{prefix}edge_{direc}({r2}, {c2}).")

    for r, c, d in puzzle.edge:
        solver.add_program_line(f":- not edge_{d.value}({r}, {c}).")

    for r, c, d in puzzle.helper_x:
        solver.add_program_line(f":- edge_{d.value}({r}, {c}).")

    tag = tag_encode("reachable", "grid", "src", "adj", "edge")
    spawn_points = ", ".join(f"not {tag}({r}, {c}, R, C)" for r, c in reachables)
    solver.add_program_line(f":- grid(R, C), not hole(R, C), {spawn_points}.")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Tentaisho",
    "category": "region",
    "aliases": ["spiralgalaxies"],
    "examples": [
        {
            "data": "m=edit&p=7VZfb9NADH/vp5ju+R7uX5JL3soovIwOyNBURVGVdhmr6JTRLgil6nef7cuoIHcb2tAQEkpj/2I7zs++f91+batNzaXAn7YcNFxGWrqVjekW/XW2ul3X2REft7dXzQYA56dTflmtt/Wo6IPK0a5Ls27Mu7dZwRTjdEtW8u5DtuveZd2Mdzm4GDdgOwEkGVcAJwd4Tn5Ex84oBeBpjwHOAC5Xm+W6nue5M73Piu6MM/zQK3odIbtuvtXMvUfPy+Z6sULDorqFYrZXq5ves20vmi9tHyvLPe/Gju/kni9+peerD3wROr6IPHyxjOfzrS8+19t24SOblvs9dP0j0J1nBTL/dID2APNsx2LJMsNZrJzSThlSSa9SUtaSSl2IFO4NKRKnZdxrFy2VSyz1ve7jdf++dsmlwXggM812ICXJGRDTYC8kFHzoEjSORZDGY44FmNXQHHnNFjh5klj85DBaan8WqaFknz1C+zC9xO764i3mH8Zr469V47h47EYF7MTTY7cYP+QTqUDrA32IAl2OEn+bY4V1eQYr0M84UG+cwIz02a2/b4nw80wkTGGfPcHx+jUPTM83NEkVyTNYSrzTJF+TFCQjkicUMyF5TvKYpCEZU0yCi/E3l+twnTyNDosELJjUwiBJaC4BBd0kgNMOgZYJ17h8NWILGBz60UoK7Q6Nn6/o37OVo4Ll7eayWtawy05gvz2aNpvrag1P+VV1UzM42/Yj9p3RXWg8Kf8fd3/nuMMREC+8ip67qAuYCzKRvDvl7KadV/NlA3MLWveAYwITSsG/MCNY0J1ypZ/oNkoFHJEIJTSCq8j8wYSP1Pfg937sWkG328j8btgNAw4RYAvbZsBhhoW/+PyD3bgc3QE=",
        },
        {
            "url": "https://puzz.link/p?tentaisho/19/22/hafheneweo2ffneneyerfgezy0eg4fifhafnezgfnfmegepel3epfzzt6989ezq7ehfehfwfnezk2dezq4b88fzveweofznfhefezzu54ffzzmedb4b3ezuejflexezg4fl7ezel72eregfztflefzzheifhbeztewen9ekejemer6eret8fpe",
            "test": False,
        },
    ],
}
