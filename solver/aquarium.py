"""The Aquarium solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type


def water_physics(color: str) -> str:
    """Return the water physics logic for the given color."""
    rule = "u_conn(R, C, C + 1) :- h_conn(R, C).\n"
    rule += "u_conn(R, C1, C2) :- v_conn(R, C1), v_conn(R, C2), u_conn(R + 1, C1, C2).\n"
    rule += "u_conn(R, C1, C3) :- u_conn(R, C1, C2), u_conn(R, C2, C3).\n"
    rule += "u_conn(R, C2, C1) :- u_conn(R, C1, C2).\n"
    rule += f":- {color}(R, C1), not {color}(R, C2), u_conn(R, C1, C2).\n"  # water level equality
    rule += f":- {color}(R, C), not {color}(R + 1, C), v_conn(R, C).\n"  # gravity check
    return rule


class AquariumSolver(Solver):
    """The Aquarium solver."""

    name = "Aquarium"
    category = "shade"
    aliases = ["aquarium"]
    examples = [
        {
            "data": "m=edit&p=7VZdb9owFH3nV1R+9oM/44S3rqN76eg2Ok1VhBBl6YoGogMyTan47zt2bkgDpO06rerDBHEOx/den2tf26x+5ONlxqXwXx1zvPExMg6PiqPwCPpcTNezrHvEj/P1zWIJwPn56Sm/Hs9WGe+kMriLYeeuSLrFMS/edVMmGWcKj2RDXnzs3hXvu0WPFwN0MS7BnZVGCrBXwy+h36OTkpQCuE8Y8BJwMl1OZtnorGQ+dNPigjM/zpvg7SGbL35mjHT435PF/GrqiavxGtmsbqa31LPKvy6+52w7BJvns/V0spgtlozUbnhxXKYwqFKwdQq6TkFvU9CHU1D/PoXkcAobLM8nJDHqpj6fzzWMazjo3m281jumpffUcC3XkGnliegeoT1h7xGxJ8w9ItlxMWaHkNLs+EgVN2wgRwZRl6E9Da0K7QU080KH9m1oRWhtaM+CTQ+pKOW4MshHoSSNqLG1XEVJiaMEJa9LHKsae96JEjv4OvJ1EjaW7E0TJ3GJE2ylhOInCdeyjIk318qVWEU1lgo4Iixhrwhjj0pZ25tSD95cW0O8g29MOAZOCGNcTfYa9obsjQG2xMsaS8TRsuZ1pSGusYZOQzqN1+PqcQ3ZGNnEluIb5G5dPQ+S9AjRxII0CD8PlTYLTOMK1cSiWrukgVVSrV3UxM6RjfVHHfGqiR3FcRp8ZY9aiml9nWliRzUQySaOFGHEjKq68rVkqA6hMyJtFjVjqWYsxrIU30IzzZsyiGOjGhuKibXeYqzv1tdjWl+8gclXqybW5KuRr6nG8nunigNtpqorrIUmrJNtTarE1bUqUGPS+278qei340loTWijsE2dP3ieeDQxSsJCpy3Pqb8/Hh7VlmLK5M4nel3MsJOyQb68Hk8y3Ai9r9+yo/5iOR/P8Kufz6+yZfUbl/Smw36x8KRYZ+/8/95+1fe2XyrxR7f3C+yKR+SkmHEcO8U5Z7f5aDxCTmHKDvLK8z2+vah3ukXVTXf3M7sfCD7g8rCoAQ6wJ/La8/19Xmz58D9H0f+cQwZPVCZNa49t7Ylaexz14N/BTqaitUe2zppq7dHPmVBUiz1sv8e32ZsW3j4c37bo2eMre71n/+J7EpfVsPMb",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="blue"))
        self.add_program_line(water_physics(color="blue"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))

            for r, c in ar:  # add connectivity facts
                if (r, c + 1) in ar and not puzzle.edge.get(Point(r, c + 1, Direction.LEFT)):
                    self.add_program_line(f"h_conn({r}, {c}).")  # horizontal connection (left to right)

                if (r + 1, c) in ar and not puzzle.edge.get(Point(r + 1, c, Direction.TOP)):
                    self.add_program_line(f"v_conn({r}, {c}).")  # vertical connection (top to bottom)

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
                self.add_program_line(count(num, color="blue", _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
                self.add_program_line(count(num, color="blue", _type="row", _id=r))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK and color != Color.BLUE)} blue({r}, {c}).")

        self.add_program_line(display(item="blue"))

        return self.program
