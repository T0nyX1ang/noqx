"""The Slitherlink solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, target_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import convert_line_to_edge, separate_item_from_route, single_route


def passed_vertex() -> str:
    """Generate a rule to get the cell that passed by the route."""
    rule = f'passed_vertex(R, C) :- edge(R, C, "{Direction.TOP}").\n'
    rule += f'passed_vertex(R, C) :- edge(R, C, "{Direction.LEFT}").\n'
    rule += f'passed_vertex(R, C) :- grid(R, C), edge(R, C - 1, "{Direction.TOP}").\n'
    rule += f'passed_vertex(R, C) :- grid(R, C), edge(R - 1, C, "{Direction.LEFT}").\n'
    return rule


def count_adjacent_vertices(target: int, src_cell: Tuple[int, int]) -> str:
    """Generate a rule that counts the adjacent vertices around a cell."""
    src_r, src_c = src_cell
    rop, num = target_encode(target)
    v_1 = f"passed_vertex({src_r}, {src_c})"
    v_2 = f"passed_vertex({src_r + 1}, {src_c})"
    v_3 = f"passed_vertex({src_r}, {src_c + 1})"
    v_4 = f"passed_vertex({src_r + 1}, {src_c + 1})"
    return f":- {{ {v_1}; {v_2}; {v_3}; {v_4} }} {rop} {num}."


def count_adjacent_segments(target: int, src_cell: Tuple[int, int]) -> str:
    """Generate a rule that counts the adjacent segments around a cell."""
    rop, num = target_encode(target)

    # segment count = vertex count - edge count
    vertex_count = count_adjacent_vertices(target, src_cell).replace(f"{rop} {num}.", "= C1").replace(":-", "")
    edge_count = count_adjacent_edges(target, src_cell).replace(f"{rop} {num}.", "= C2").replace(":-", "")
    return f":- {vertex_count}, {edge_count}, C1 - C2 {rop} {num}."


class SlitherlinkSolver(Solver):
    """The Slitherlink solver."""

    name = "Slitherlink"
    category = "route"
    aliases = ["slither", "tslither", "touchslither", "vslither", "vertexslither", "swslither", "sheepwolfslither"]
    examples = [
        {
            "data": "m=edit&p=7VVNb9swDL37VxQ68yBZ8ucta5NdsnRbMxSFEQRO6q7GbLhz4qFQkP8+irbjCXA3DC2KHgrFxKMeJfOJprL72aR1BgEOGQIHgUNyRY/Pza8fy3xfZPEZTJr9fVUjALiczeAuLXYZOEkXtnIOOor1BPTHOGGSARP4uGwF+kt80J9ivQB9hRQDgXNzRBjgIpwO8Jp4g87bScERLzqM8AbhNq+3RbaetzOf40QvgZn3fKDVBrKy+pWxdhn526rc5GZik+5Rze4+f+iYXXNb/WjY6RWsbIp9vq2KqmZdtkfQk1bCdESCHCTIkwQ5LsF9CQnZ7ffscSz7aDz7I1bmK+a/jhMj5dsAwwFexYejSfPAXA9XSvwacEvc0I3QFSdXGtYdXB9dPriBzdprFbeClbCCVWAFezbrR1ZWgbTdyAoOubVVKKzgUNqssl1bfiQsNvpTPh6YoGO7ITsj65Jd4qmClmQvyHKyHtk5xUzJXpM9J6vI+hQTmLr8V+Wenw7WHvVFIVYu9FsgpAKhcFZ2WPbYw3m/xaqP+aeexFV00/TDe3lv5SRsii1ytqjqMi2wURZNucnq3seL6uiwR0YPVVq9311v9+4yVeKv3AfPbcsED/vUOaAvgT0063SN0hj+UcJAy7/QbX+N09in4wT27VMbqifSefWzw1tg5fwG",
        },
        {
            "data": "m=edit&p=7VVLj9MwEL7nV6x89sGPOrFzK0vhUsKjRdUqqlZtN7AViQJpg1ap8t8ZT1oo48JeQFoJ5Hg0+Twznoft2X1pV03BHQxtueAShrYCpx35TxzHfLsvi/SKj9v9fd0Aw/nrjH9YlbuCR/lRahkdOpd2Y969THOmGWcSpmJL3r1ND92rtMt4N4MlxiVgU+BAQAM7GVgF7ALXPXg9SApgs2Hda90Au9k2m7K4nQ4ab9K8m3Pmt3mGKp5lVf21YIMa/m/qar31wHq1h1h299vPx5Vde1d/atn3LVjVlvvtpi7rhh2d7Xk3HiKY/D4C/UgE6k9EUNx9LB4uOe8uO99DXd6B+7dp7iN5/4OdpYfe+3ZgyrKhZtJXDewod8rIEdDSAzPG7QnQFDBUJSbACG2oM0B5YOGTdEI01UkoYAMdR5w31BMTU4mEGjGW+GYcFYkFEYlpPHFCchIHRhJqJFEU0IGOIWatIgHaEZWgETtaLmfoNo7Wy1kKBOFIQc+FFLRiUtDTJUVoSGJixJmQlKEQTZaUOkAcRZQIDClaOqnooZEqDtWC2HTgkQ480rR+UtODIjW9cHL0c0Lgpkq8rzdIXyBVSOdwnXmnkT5HKpAapFOUmSBdIL1GOkIao0yC1J6ehl8/GfbC6/HXPeujXFlsT+fDPC1kGeVsAk/zVVY31aqEBzprq3XRnP6hPfYRe2A4c8WVgSbxv2U+0ZbpiyQeb5z/9KWE85wvo28=",
            "config": {"swslither": True},
        },
        {
            "data": "m=edit&p=7VTfb4IwEH7nr1j63AfaghTenNO9uJ+6GEOIQa2TTIMDWZYa/vcdpxNrTJYly+bDUvrlu95d76MHzV+LOFPUhyEktSmDIaSNUzrVY+9GP1kvVHBBm8V6nmZAKL3rdOgsXuTKCndRkbXRfqCbVF8HIRGEEgaTk4jqh2CjbwIySZfjhFDdAz+hDBxdYBDFgbZrOkB/xVrbRWYDv91xoEOgkySbLNSou125D0Ldp6QqdonZFSXL9E2RbRraWwGwMI7X8Eb5PFntPHkxTV8K8lmipLr5hWZRaxZ7zeK0Zv4TmtX0Wb2fkutHZQln/wiCR0FYaX+qqaxpL9iUlaQN4T6kcmg3pMNuwgWT7U1HgClq88jrGbmuawS7nhHs+oa3wYzchhnsmYWkGSxNVdKsKz3D9IWR65teZptbM1salRnjps2PbedgPzhThic7ROwgcsQ+HDzVAvEK0UZ0EbsY00YcILYQHcQGxnhV677V3F+QE3KJl8XhcM9rJbJC0iuyWTxR8Mu00uUqzZO1InBJlRZ5Jzixhc7/vfWX91bVB/vcPvBzkwO/XGR9AA==",
            "config": {"tslither": True},
        },
        {
            "data": "m=edit&p=7VTLbsIwELznK5DPPji2E0hulNJeaPqiQihCiEdaoiZKm0eFjPj3rjeB1BKXSqjiUDkezdhre8d2XHxWizyiXSiiRxm1oQgmsbpMf4cyjssk8ju0X5WbLAdC6X1AXxdJEVErbKJm1k55vupTdeuHRBBKbKiczKh69HfqzlcBVc/QRagNbSNgEMCBDls6wX7NBnWjzYAHDQc6BbqK81USzUd1y4MfqjElep0rHK0pSbOviNTDUK+ydBnrhuWiBDPFJv5oeopqnb1X5LgESaukjFdZkuWkyXZPVb+2MDxhQbQWxNGCOG2Bn8NCtH6Ltqey905nv4eTeYL8536orby0tNfSZ3+312nuCJcwksNlgClhQu6CtFvZM6RgRrB0TdkzpMOMsQ4HKY/SNYO7Oli00gzuSkN6zJTcmMqTxrreT0dg2kbrU8QbRI44hp2hSiBeIzJEB3GEMUPECeIAUSK6GNPVe/ur3f+DdEIu8V8/FOf8amaFZAi3tBNkebpI4K4GVbqM8oOGt2JvkS3Biocs/5+Py30+9CmxS7vGl5YO/Fgz6xs=",
            "config": {"vslither": True},
        },
        {
            "url": "http://pzv.jp/p.html?slither/25/15/i5di5di6bg3ad13dc13bd3cg5bi7ci7dhai6bi6ci7b02bd33cc23d8ci8ai6cibh6di6bi7dg1ca31ab10dc3dg6bi6ai6chai7ci7ci8d33dc33cc20d8bi7di7cidh8di5ci6cg3dd03cb02ad3dg6bi7ci6bg",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?tslither/7/7/negdh42bmckaaci",
            "config": {"tslither": True},
            "test": False,
        },
        {
            "url": "https://puzz.link/p?vslither/9/8/1239123em1239123em1239123em1239223em",
            "config": {"vslither": True},
            "test": False,
        },
    ]
    parameters = {
        "swslither": {"name": "Sheep/Wolf Variant", "type": "checkbox", "default": False},
        "tslither": {"name": "Touch Variant", "type": "checkbox", "default": False},
        "vslither": {"name": "Vertex Variant", "type": "checkbox", "default": False},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(convert_line_to_edge())

        if puzzle.param["vslither"] or puzzle.param["tslither"]:
            self.add_program_line(passed_vertex())

        if puzzle.param["swslither"]:
            self.add_program_line(separate_item_from_route(inside_item="sheep", outside_item="wolf"))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if puzzle.param["swslither"] and clue == "W":
                self.add_program_line(f"wolf({r}, {c}).")
            elif puzzle.param["swslither"] and clue == "S":
                self.add_program_line(f"sheep({r}, {c}).")
            else:
                fail_false(isinstance(clue, int), "Clue should be an integer or wolf/sheep with varient enabled.")

                if puzzle.param["vslither"]:
                    self.add_program_line(count_adjacent_vertices(int(clue), (r, c)))
                elif puzzle.param["tslither"]:
                    self.add_program_line(count_adjacent_segments(int(clue), (r, c)))
                else:
                    self.add_program_line(count_adjacent_edges(int(clue), (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
