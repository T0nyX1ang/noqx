"""The Family Photo solver."""

from typing import Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region


def count_family_photo_size(num: int, src_cell: Tuple[int, int], adj_type: Union[int, str] = "edge") -> str:
    """Count the size of a family photo region."""
    src_r, src_c = src_cell
    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, None)
    return f":- #count {{ (R, C): black(R, C), {tag}({src_r}, {src_c}, {src_r}, C), {tag}({src_r}, {src_c}, R, {src_c}) }} != {num}."


class FamilyPhotoSolver(Solver):
    """The Family Photo solver."""

    name = "Family Photo"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7ZXtb6JOEMff+1c0+7abHMuDAsnlF2u1155a22q8SoxBi0oLrodgexj/984ueghse9d7aH4vLoTJ8Jl1dmZYv6y+RnbgYB0uRccSJnApqsxvWTL4Le2urht6jnmEq1E4pwE4GF82GnhqeysHX9zOmzVafTytflnr4WBAzqToXOrfN+6Pr/3P564SkEZb77Q6LVeeVT/VTq7K9eNyJ1r1Qmd95ZOT+96gO+30Z4b8rd4eqPHgUtIuBtMP62rvY8na1TAsbWLDjKs4PjMtJCPMb4KGOL4yN3HLjNs4voEQwmSIkR95oTuhHg3QnsVN8AjCMrj11O3zOPNqCSQS+O2dD+4tuBM3mHjOqJmQjmnFXYzY3if818xFPl07bDP4GX+eUH/sMjC2Qxjfau4uEVYgsIru6EO0W0qGWxxXkw7qP9kBJNl3wNykA+YJOmCN/d0OjOF2Cy/nGnoYmRZrp5e6euremBuwbXOD5DL7qYJwJXmDSCMMqFDbDpQ1BjSE1R0wFAb+SwEh6m5J8htITfgGt/sNZGggabqVTFQ2MjQZBVIkIWX7FagqXKuJKauvSFljBcrbLdKKkAq7qAgzVLJz2FNdRHXhWj73IhVmMISVESJMQYhgP3h9Df4SZW67cHBwrHB7yq3ErcZtk6+pc9vntsatym2Zr6mwo/emw3l4jn6tHKRqMB5Dhx7LBiYVOB3KD0u05DJX4PTS3vd5WLJQ/W7mHLVp4NseKEA78sdOkD7fzO2lg0CH0Yp6o1UUTO2JM3Ke7EmIzORTcBjJsAXPlUEepUvPXYgy7EMZ6M4WNHCEIQYdqP2FVCwkSDWmwV2upkfb87K98I9kBiXnNYPCAFTy4NkOAvqYIb4dzjPgQFEzmZxFbpihnS3RfrBzu/npOLYl9IT4bSlY/vfR/J9/NNmLkt5ZnX5XLC0Y+Hdhw/ElRstoZI9g5gjOG2ZhtSK9NaDpfyDw7pPifz8avKKFaTCPBYoI9BVRPIiK+Av6dxDN84LYsWKLegdUIHlA86oHqCh8AAvaB+wF+WNZ8wrIqsqLINuqoINsq0MptIalZw==",
        },
        {
            "data": "m=edit&p=7Zbfb7pIEMDf/Suafe0mx4IiktyDtdprz1rbarxKjEGLSgvSL4LtYfzfOzPqyY9tkz406Te5IOPwmWV2ZlhmWf2K7dDhQsGfZnD4h6MsDDpVQ6dT2R89N/Ic84TX42gRhKBwftNq8ZntrRx+9bBoN4L663n9n7URDYfiQokvlcFT6+n0zv/70tVC0eoY3evutavO6381zm715qnejVf9yFnf+uLsqT/szbqDeU39t9kZlpPhjVK5Gs7+WNf7f5asfQyj0iapmUmdJxemxVTG6RRsxJNbc5Ncm0mTJ/dgYlyMOPNjL3KngReE7MCSNmiCcRXU5lEdkB21xg4KBfTOXgf1AdSpG049Z9zeka5pJT3OcO4zuhtV5gdrByeD2+h6GvgTF8HEjqB8q4X7wrgGhlX8GDzH+6FitOVJ/WsZgJNDBqjuMkBNkgEm9r0Z1EbbLTycO8hhbFqYTv+oGkf13tyA7Jgbpml4Kzw/sXuCrFxBoB2BXj2UZw+qah7UcsAgkHIqFB1JOUUEkfQYlUJJj1GNXCyiouSJTtH85wfSEpTcAyaHo1UoXrrgTMMMixTTLFLMpEApiiLFSApUF1IqHVstS6k0MgNrU6A16Ww1qd+atA5CkSYnFKlnoUhdC0UasxDSoIUq901rU4LlU5blo2k9F3EFl58EywPU5TXRJb5h6bVoAaoke/DC8UQjeU5SIVkh2aYxTZIDkg2SZZI6janiK/ullzr9DnxTOJa226WyR+X3Y6OSxZqPc+ekE4S+7UG37cT+xAmP1/cL+8VhsOexVeCNV3E4s6fO2HmzpxEzd9tu2pJhS/KVQV4QvHjuUubhYMpAd74MQkdqQuhA7B+4QpPE1SQIH3Mxvdqel82FPkkyaLfGMygKYUdKXdthGLxmiG9HiwxI7V4ZT84yV8zIzoZoP9u52fxjObYl9sbotDSu/v+B8sM/UPBBKT+to/20cGiNB+EnDedozGNJ2wH6SedJWWX8gyaTsuZ5oaNgsMWmAlTSV4DmWwugYncBWGgwwD7oMeg132YwqnynwakKzQanSvcba1R6Bw==",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(f":- {{ upleft(R, C) }} != {len(puzzle.text)}.")

        for (r, c, d, label), _ in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"black({r}, {c}).")

            if (r + 1, c, d, label) in puzzle.symbol:
                self.add_program_line(f":- edge_top({r + 1}, {c}).")

            if (r, c + 1, d, label) in puzzle.symbol:
                self.add_program_line(f":- edge_left({r}, {c + 1}).")

        all_src = []
        tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_family_photo_size(num, (r, c), adj_type="edge"))

            all_src.append((r, c))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
