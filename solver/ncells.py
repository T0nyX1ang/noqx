"""The N Cells solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.reachable import grid_branch_color_connected


def count_reachable_edge(target: int) -> str:
    """
    Generates a constraint for counting grids in a region divided by edges.

    An edge rule and a grid_branch_color_connected rule should be defined first.
    """
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")

    return f":- grid(R0, C0), #count {{ R, C: {tag}(R0, C0, R, C) }} != {target}."


class NCellsSolver(Solver):
    """The N Cells solver."""

    name = "N Cells"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7Vjfb+JGEH7nrzj5eR92vb9sv1TplfQl5dpeqtPJQogQ2kMlIiWhqhzlf79vx+ZwHMabKwfXVpXFMuw3uzOeGX875u6PzXQ9F0oKpYTOBL5xGZUJY53w2tBHNtfl4n45L16Js839h9UaghBvzs/Fr9Pl3XxQNlrjwUOVF9WZqL4vyiRNBH1UMhbVT8VD9UNRjUT1FlAiFOYuIKlEpBCHO/Ed4UF6XU8qCXnUyBDfQ5wt1rPlfHJRz/xYlNWlSIKdb2l1EJOb1Z/zpF5Gv2erm6tFmLia3uNm7j4sbhvkbnO9+n3T6Krxo6jOaneHe9zVO3eDWLsbpKO5u7xd7XM0Hz8+IuA/w9VJUQavf9mJ2U58WzxgHBUPiXHbe6yzkhgfJpCkTxNZmNCtibyzxMrOEqs6E440Wkuc7Wh407Hiyco3u4mM/GgtyXVHQ8m0Y0ZJ0mktUpIMPdEhX1qmlewGRcluVJQinfZMSnfd3kd3b1vp7n0r88yfOr7tfWw3BcqSTnufOsRtHffMH/csPu5pfFAUikrjPY3nNKY0XqJyRKVp/I5GSaOl8YJ0hjS+o/E1jYZGRzo+1N5nVefh7qB6EZc8Q00ahIMEh4gHAVzWCKHWSMi2Qt4op9aK1CLVWiQaHKg9tguyy3cydIDtdCyKJcheQgcb6WhQSl1T7dPL/jfmxoMyGV7/Nn81Wq1vpkvw1mhzczVfb3/jiHgcJH8l9Cl1OHH+PzVOfmqE4MsTP52HkkWJuH56REX1RiS3m8l0MluhyBC8BnaAPQsb3QunuYAKv7nBastvLgGbXhi0xNr2PbBz6X7AOMMAVnJbcYC33FaMcecdt0J/7n18QRvcfdTpxxHMwsiv6ckvSg8dFAuj9NBPsXDIb8bCaLV52NiciyeTfueYIDjHxNM5z9Y9XEdXwsKZSD0ouycu6Fc4GOWYoh/kYI+U9cEpYP6J9arXtX542wJwcNMVsKvrRqFvc56Ktu3EfhitCwPkzMPdA6gvRSAsF52iStlHJMrLEVaPHDiHsHr0uIqcR/9WOvu6nBChqwjZRTqICPyCzfmEagXKwFtmH6x4RlEeq9lS1KgWzVcLwbzngADnLCzBZpK3LfEHlOJtK9jm4RQ8nGZ8vjMENeupFtQaC+OFkqFNFPheAG+ezArPcTbXE3nHdDhWM1tZridibbBb8cY5GygCLbTjCxDUrV1PCSHLLIz3+K+Q/jjFHvK4H/WpOC5ZHDHTR2aiF3Rlf7/l623aYi1frFeIdBov6HL4mMfgI77axjqsf2QXfvK/RvCv4XjwEQ==",
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

        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent_edges(num, (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
