"""The Firefly (Hotaru Beam) solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import defined, display, fill_line, grid
from noqx.rule.helper import validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import convert_line_to_edge, directed_route, route_turning

drdc = {"1": (0, 1), "2": (1, 0), "3": (0, -1), "4": (-1, 0)}
dict_dir = {"1": Direction.RIGHT, "2": Direction.BOTTOM, "3": Direction.LEFT, "4": Direction.TOP}


def restrict_num_bend(r: int, c: int, num: int, color: str) -> str:
    """Generate a rule to restrict the number of bends in the path."""
    rule = f"reachable({r}, {c}, {r}, {c}).\n"
    rule += f"reachable({r}, {c}, R, C) :- {color}(R, C), grid(R1, C1), reachable({r}, {c}, R1, C1), adj_line_directed(R, C, R1, C1).\n"
    rule += f":- #count{{ R, C: grid(R, C), reachable({r}, {c}, R, C), turning(R, C) }} != {num}.\n"
    return rule


def directed_to_undirected_line() -> str:
    """A rule to convert directed line adjacency to undirected line adjacency."""
    rule = "firefly_all(R, C) :- firefly(R, C).\n"
    rule += "firefly_all(R, C) :- path_start(R, C).\n"
    rule += "adj_line(R, C, R1, C1) :- adj_line_directed(R, C, R1, C1).\n"
    rule += "adj_line(R1, C1, R, C) :- adj_line_directed(R, C, R1, C1).\n"
    return rule


class FireflySolver(Solver):
    """The Firefly (Hotaru Beam) solver."""

    name = "Hotaru Beam"
    category = "route"
    aliases = ["hotaru", "hotarubeam", "firefly"]
    examples = [
        {
            "data": "m=edit&p=7VbfT9s8FH3vX1H5aZP8kMT5/cZY9710ZRtMCEVVlZYwqrUKX9pMzFX/d66Pw2JsUAVIPKE0V7fH914f2ye2N/+3ZVNxP1Q/kXKP+/REiYc3TGK8XvecLberKh/yo3Z7XTfkcH4y4VflalMNCpVIz3Swk1kuj7j8Ly9YwHj3Trn8nu/k11xOuDylJkaxXI7J8xkPyB317jnalXesQd8jf6L9mNwLchfLZrGqZmNd6FteyDPOVD+fkK1ctq7/VEyn4f+iXs+XCpiXWxrL5np507Vs2sv6d9vF+tM9l0ea7ugRuqKnq1xNV3mP0FWjeDXd6vJXdfsY02y639OM/yCus7xQtH/2btq7p/mO7CTfMREHKpdocCpA9UScKkAYSBLaSIokE8m8+8nqkNATCqHl7pHIygr9zEYCu3IYIMusI8AwNJAQWWZMBM4GoMdpFk5Q2KScOnQy347JEqtwhqQeiHwM3KgSBbFCIgMRoGfUjULEGECEGTXLxCBjAsjxDCRBiJmUPuyJlt3H4l/8W/yAs6tlU12t/kKenQIo/CEKFQgbhRJCG4Ua7FitCLuuVoXNQSvDrqvV4cRCIU5vUInTG5TiVIBanFjMjsMBsnFiIR0nFvJxYiEhhy90ZMdqMTkoBGWPQovK5qCF5VSAupxYKMxFVQWbr5aawwFye9gbie0LJBfAntEWxKWA/QzrwUawY8SMYM9hj2FD2BgxidrEnrXNmap/GR0Wp7RqWao+j4DORpo+cZBiESX6GHSed7y7HhRsRIfZcFI363JFR9qkXc+r5v4/XR/2A3bL8JIEfR6+3yje/kahZt974w/utd9/Icdqk+JRyrg84eymnZWzRU0ao7k70Djqv/KnmlOPi+zp7APNB4rH6vZNsn5JNu1Tzy375itHO+P9ATH8cF1vy6Ydzqty/ZFNB3c=",
        },
        {"url": "https://puzz.link/p?firefly/10/10/4.40g20c32j1.b3.h32d41a23c4.d3.b2.g3.j2.a3.e1.d1.b10h30", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="path_start"))
        self.add_program_line(defined(item="firefly_all"))
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line("{ firefly(R, C) } :- grid(R, C), not path_start(R, C).")
        self.add_program_line(fill_line(color="firefly", directed=True))
        self.add_program_line(adjacent(_type="line_directed"))
        self.add_program_line(directed_route(color="firefly"))
        self.add_program_line(route_turning(color="firefly", directed=True))
        self.add_program_line(directed_to_undirected_line())
        self.add_program_line(grid_color_connected(color="firefly_all", adj_type="line"))
        self.add_program_line(convert_line_to_edge(directed=True))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            shape, style = symbol_name.split("__")
            if shape != "firefly":  # pragma: no cover
                continue  # warning: incompatible encoding with penpa+/puzz.link

            dr, dc = drdc[style]
            clue = puzzle.text.get(Point(r, c, Direction.TOP_LEFT, "normal"))  # the text is also placed in the top-left corner

            if isinstance(clue, int):
                self.add_program_line(restrict_num_bend(r + dr, c + dc, clue, color="firefly"))

            self.add_program_line(f"path_start({r}, {c}).")
            self.add_program_line(f'line_out({r}, {c}, "{dict_dir[style]}").')
            self.add_program_line(f'{{ line_in({r}, {c}, D) }} :- direction(D), D != "{dict_dir[style]}".')

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
