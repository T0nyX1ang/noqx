"""The Tentaisho (Spiral Galaxies) solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import extract_initial_edges, tag_encode
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
    solver.add_program_line(extract_initial_edges(puzzle.edge, puzzle.helper_x))

    reachables = []
    for (r, c), symbol_name in puzzle.symbol.items():
        reachables.append((r, c))
        _, _, category = symbol_name.split("__")

        if category == "0":
            solver.add_program_line(galaxy_constraint(r * 2 + 1, c * 2 + 1))

        if category == "1":
            solver.add_program_line(galaxy_constraint(r * 2 + 2, c * 2 + 2))
            solver.add_program_line(f"not edge_top({r + 1}, {c}).")
            solver.add_program_line(f"not edge_top({r + 1}, {c + 1}).")
            solver.add_program_line(f"not edge_left({r}, {c + 1}).")
            solver.add_program_line(f"not edge_left({r + 1}, {c + 1}).")

        if category == "2":
            solver.add_program_line(galaxy_constraint(r * 2 + 2, c * 2 + 1))
            solver.add_program_line(f"not edge_top({r + 1}, {c}).")

        if category == "3":
            solver.add_program_line(galaxy_constraint(r * 2 + 1, c * 2 + 2))
            solver.add_program_line(f"not edge_left({r}, {c + 1}).")

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
            "data": "m=edit&p=7VVNj9owEL3zK1Y++5CJ82Fyo1vay5ZtG6oViiIU2GxBBYUCqSoj/vvOjL1CbRy1UtUvaRU883geT57Hdnz43Fb7WkJAP6Ulenwi0NxCnXAL3DNdHzd1diVH7XHV7BFIeTuRD9XmUA8KF1QOTmaYmZE0r7NChEJyA1FK8y47mTeZmUmTY5eQEXI3iEDIEOH4Au+4n9C1JSFAPHEY4Qzhcr1fbup5nlvqbVaYqRT0ohc8nKDYNl9qYcfx/2WzXayJWFRHnMxhtd65nkN733xqXSyUZ2lGVu/4SS+9xelVF70ErV5CHr00jV/XW99/rA/twid2WJ7PWPX3KHeeFaT8wwXqC8yzk0hAZJEUSWidsi5ilzo3ZKc1u6ENgcCOgCC1HhLnbTSENjGoJ+/ilRuvbHKIKB7FTLITWmA7Q2EK+QJwwpcqYeFEjGk8dBIgHXbp2Etr1ORJoumV3WhQ/iygcMo+Pia+mx6our54Tfm78Sryz1XRunj4KOzhWaeH1xTf1ROHPaXvqUPcU+U49Zc5CWlensXqqWfSM98kxR3p47W/bmng15kCbmEfn9J6fZ8Ht+cr3qQh2ykeJWkU25dsA7Yx2xuOGbO9Y3vNNmKbcExKh/Enj2v3nPwmOYWyX/5vn/j/48pBIfJ2/1Ata/xUjvGjeTVp9ttqg//yVbWrBV5Q54H4KrgViq675zvr79xZtALBv3YUfiCnwL0AKUhzK8WunVfzZYN7C0vX1/HH9eNpLgeP",
        },
        {
            "url": "https://puzz.link/p?tentaisho/19/22/hafheneweo2ffneneyerfgezy0eg4fifhafnezgfnfmegepel3epfzzt6989ezq7ehfehfwfnezk2dezq4b88fzveweofznfhefezzu54ffzzmedb4b3ezuejflexezg4fl7ezel72eregfztflefzzheifhbeztewen9ekejemer6eret8fpe",
            "test": False,
        },
    ],
}
