"""The Star Battle solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs, validate_direction
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent


class StarBattleSolver(Solver):
    """The Star Battle solver."""

    name = "Star Battle"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VVda9swFH3Pryh61oO+rA+/ZV26l67d1pZRTAhu6q1hKenyMYZD/vuO5OuqZWGlhRUGw7E4kXSPr87RlVbfN/Wy4VLFn/ZccInHBJNe7Yr0CnrOZ+t5Ux7w4WZ9s1gCcH56dMS/1PNVM6hkipXjwbYNZTvk7buyYorx9Eo25u3Hctu+L9sRb88wxDCXt8dAknEFOMrwcxqP6LDrlAL4hDDgJeB0tpzOm8lx1/OhrNpzzuJ33qToCNnt4kfDurD0f7q4vZrFjqt6jcWsbmZ3NLLaXC++bVj/iR1vh126l3vS1TldfZ+u3p+uonRX63r5olS7wN+TDOPdDmJ/QpqTsooZX2ToMzwrt7uYzZYZzTpPZHIEvTKNXcYxgzHF6WsqDh6lQZXac3DxVqf2bWpFaovUHqc5I9CogD0jJStBpYXjWukOSwnsCGOOpjlKAwfCmG9ovvLApsMasYZideC6KDpsEFtQrMF+tYIweCzxFHEP07eKEPdzhy1iHcU68Hvid7EQPGFwBuKMtRCIx4EnEI933Aj6lvfAlHMQwJYwakoQP/QxpA/igANh1JwShC2wIgx+0hBxwI5w4EZ3OWAcmHigoSENDSraFCZ7IWhdAtoKWrvAWiStUYrsXfRLKsLQRPY+QjdJnBL6yCL7pXofwamJU4vstQW2PQa/JX6rsl/RC6eyF67vj36Z7EvvYzqjSGdngXsfsV7X++gfeI3cPOXm7b3v0B7aki9KZv01/NKWMHzRNF9DZ+2zzr3+2J/GkI8GnIY4DTgNcRpFHu3i2RFL5zC1JrU2lZSLxfus8n5UztY9LGecOszH4he552UF/mTGVUEXwaPH/Xt940HFRtdfm4OTxfK2nuMEPrup7xqGC243YD9Zeisd78v/d96r3nlRePHi0vhL+/6JdCpoispoTzm720zqyXSBHQXF/tRv3f5+r5/Hs6f/1dXBwTAe/AI=",
        },
        {
            "url": "https://puzz.link/p?starbattle/15/15/3/31g94h1gk30glmiuum28c52kl8mh0i10o51gh4i1go2h84a4802gt5hah8la6046hc9aign1ga18424a42h8",
            "config": {"stars": 3},
            "test": False,
        },
    ]
    parameters = {"stars": {"name": "Stars", "type": "number", "default": 2}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.param["stars"].isdigit(), "Invalid star count.")
        num_stars = int(puzzle.param["stars"])
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="star__2"))

        self.add_program_line(adjacent(_type=8))
        self.add_program_line(avoid_same_color_adjacent(color="star__2", adj_type=8))

        self.add_program_line(count(num_stars, color="star__2", _type="row"))
        self.add_program_line(count(num_stars, color="star__2", _type="col"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(num_stars, color="star__2", _type="area", _id=i))

        for (r, c, d, _), symbol_name in filter(lambda x: x[0][0] != -1, puzzle.symbol.items()):
            validate_direction(r, c, d)
            if symbol_name == "star__2":
                self.add_program_line(f"star__2({r}, {c}).")
            if symbol_name == "star__0":
                self.add_program_line(f"not star__2({r}, {c}).")

        self.add_program_line(display(item="star__2"))

        return self.program
