"""The Sukoro Room solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, display, fill_num, grid, invert_c, unique_num
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_same_color
from noqx.rule.reachable import grid_color_connected


def num_count_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """Generate a constraint for counting the number of adjacent black cells."""
    return f":- number(R, C, N), N != #count {{ R1, C1 : adj_{adj_type}(R, C, R1, C1), {color}(R1, C1) }}."


class SukoroRoomSolver(Solver):
    """The Sukoro Room solver."""

    name = "Sukoro Room"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VRNb9swDL37VxQ66yBRdmP7lnZOL226LSmGQDACp/WWoAmcJfFQKPB/HynLUYq16AfQngZZxNMTST9TtLa/62JT8giHirngEgdAbGco6OnGeLFblukJ79e7ebVBwPn1YMB/FsttGWjnlQd7k6Smz81FqplknAFOyXJuvqV7c5WajJsRbjEukbtsnQBh5uEPu0/ovCWlQDx0GOEEYfUwPWtXX1NtxpzRO85sJEG2qv6UzGmg9W21mi2ImBU7/JDtfLF2O9v6rrqvWZe+4abfSh0+IVV5qeogVT0tFbzU7AOkJnnTYLm/o9hpqkn3jYexh6N035CmPQOgUIVa2jNhoSACPBHFjzwwTtroibUDa8HaMSbnRln7xVphbWTtpfXJ8J1SYFMJyVLAjALbS4DDgFhZnIQHKEXCpRQtlhgqE4eRh46Xj7HsUiqPoYc+scMxYpcHxBFGXvWOeCcTMKdy+RXyKvE8dPlRPjjNCvlQeKycjwSfk7B0/pJ0hk5z6HnCIvLlkRTbUJdRNc+tDa09tVXu0QG/qQWOD5RRCTUe9KE/GRVGh55535m/qFhDe9HQiF6H8kCz7O5XeTKsNqtiif/DsF7Nyo1fj+bFumR4ATUBe2B2aqwzD//fSZ98J1Hpxbvb8oN67gU52kw4dqW55mxdT4vpbYU9hXWzfPIM/5z/v/ynfy3+ZHnwFw==",
        },
        {"url": "https://puzz.link/p?sukororoom/10/10/nrnfdbp5timpmpdnns4svecvuufnvsbvtst7g1zzzn", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_num(_range=range(0, 5), color="white"))
        self.add_program_line(invert_c(color="white", invert="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(num_count_adjacent(color="black"))
        self.add_program_line(unique_num(color="black", _type="area"))
        self.add_program_line(area_same_color(color="black"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, (ar, _) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "ox_E__1":
                self.add_program_line(f"not white({r}, {c}).")
            if symbol_name in ("ox_E__4", "ox_E__7"):
                self.add_program_line(f"white({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
