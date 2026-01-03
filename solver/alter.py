"""The Alternation solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, count, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent


def alternation_constraint() -> str:
    """Generates a rule to ensure that the colors alternate."""

    # three shapes do not appear in the same row or column
    rule = ":- grid(R, C0), grid(R, C1), grid(R, C2), ox_E__1(R, C0), ox_E__2(R, C1), ox_E__3(R, C2).\n"
    rule += ":- grid(R0, C), grid(R1, C), grid(R2, C), ox_E__1(R0, C), ox_E__2(R1, C), ox_E__3(R2, C).\n"

    # the same row and column does not only contain one of the three shapes
    rule += ":- grid(R, C), ox_E__1(R, C), not ox_E__2(R, _), not ox_E__3(R, _).\n"
    rule += ":- grid(R, C), ox_E__2(R, C), not ox_E__1(R, _), not ox_E__3(R, _).\n"
    rule += ":- grid(R, C), ox_E__3(R, C), not ox_E__1(R, _), not ox_E__2(R, _).\n"

    # color alternation rules
    rule += ":- grid(R, C), ox_E__1(R, C), grid(R, C1), ox_E__1(R, C1), C1 > C, #count { C0: grid(R, C0), ox_E__2(R, C0), C0 > C, C0 < C1; C0: grid(R, C0), ox_E__3(R, C0), C0 > C, C0 < C1 } = 0.\n"
    rule += ":- grid(R, C), ox_E__2(R, C), grid(R, C1), ox_E__2(R, C1), C1 > C, #count { C0: grid(R, C0), ox_E__1(R, C0), C0 > C, C0 < C1; C0: grid(R, C0), ox_E__3(R, C0), C0 > C, C0 < C1 } = 0.\n"
    rule += ":- grid(R, C), ox_E__3(R, C), grid(R, C1), ox_E__3(R, C1), C1 > C, grid(R, C1), #count { C0: grid(R, C0), ox_E__1(R, C0), C0 > C, C0 < C1; C0: grid(R, C0), ox_E__2(R, C0), C0 > C, C0 < C1 } = 0.\n"
    rule += ":- grid(R, C), ox_E__1(R, C), grid(R1, C), ox_E__1(R1, C), R1 > R, grid(R1, C), #count { R0: grid(R0, C), ox_E__2(R0, C), R0 > R, R0 < R1; R0: grid(R0, C), ox_E__3(R0, C), R0 > R, R0 < R1 } = 0.\n"
    rule += ":- grid(R, C), ox_E__2(R, C), grid(R1, C), ox_E__2(R1, C), R1 > R, grid(R1, C), #count { R0: grid(R0, C), ox_E__1(R0, C), R0 > R, R0 < R1; R0: grid(R0, C), ox_E__3(R0, C), R0 > R, R0 < R1 } = 0.\n"
    rule += ":- grid(R, C), ox_E__3(R, C), grid(R1, C), ox_E__3(R1, C), R1 > R, grid(R1, C), #count { R0: grid(R0, C), ox_E__1(R0, C), R0 > R, R0 < R1; R0: grid(R0, C), ox_E__2(R0, C), R0 > R, R0 < R1 } = 0.\n"

    return rule.strip()


class AlterSolver(Solver):
    """The Alternation solver."""

    name = "Alternation"
    category = "var"
    aliases = ["alternation"]
    examples = [
        {
            "data": "m=edit&p=7VTfb7JIFH33r2jmtTdZZlALJPugVrvttta2GleJMWhR6QeOi2C7GP/33hno8kPafml2N33YINfDucO9hwtztn+Glm9DFQ9VAwWoOHT8x1On4qckR98JXNs4gUYYrLiPAOC204GF5W5tuBqtrlu88Xze+GOnBeMxvVDCS2X41Hk6vfd+v3RUn3a6Wu+md+OwZeO3VvOu3j6t98LtILB3dx5tPg3G/UVvuNTZX+3uuBqNb5Xa1Xjxy64x+LViJhomlX2kG1EDogvDJJQAYXhSMoHozthHN0bUhugBUwToBIgXuoEz5y73yRsXXcc3MoTtFA5lXqBWTFIFcTfBCEcI+cu0GV/1DDPqAxF9m/JOAYnHd7ZoJHSJ6zn3Zo4gZlaAo9uunA0BFRPb8JH/CJOldHKAqBGrH/2keizypl7AWL1AJerFQyXq2/+8en1yOOBLuUf9U8MUjzJIoZbCB2OPsSsjlXFk7AmjWIZCOlnCzpBRs4xaLa5R60WmypBhKYPlO7IJk7GPGiBSZTyXUZGxJuO1XNNGORoFDSthIY2BrkgktoEWIw10PUY6TjhJs7+hVgU9uVsFDVUjOquBpqb34MMx7DWUHVsyVmWsSyVnYlZfnyZFdaYmpxC/acJQWTJNyXxtLp8qNqkW+wbUyv8nFZO0H5f2SZf7nuXiF/awsjY2wf1MttydbkN/Yc3tqf1izQNixJaSzeS4dejNbNwUGcrlfOM667IKb6kc6SzX3LdLU4K0Ues7pUSqpNSM+48FTc+W6+afRVptjpo7/tzNU4GPuy5zbfk+f84xnhWsckRmh+Yq2evCMAMrL9H6YRW6eek4DhXyQuSJnxD733y/qfmKF6R82TT+JUf4RI6Jw2Y6RLdANuHUmuKgCX5g8C15pZynx+v/8ynLLcv9D/wzTRbpEhdF9gMjzWTL+Hc8M5Mt8kcGKcQeeySyJTaJbNEpkTo2SySP/BK5dyxTVC26plBVNE7R6sg7RausfZqTyis=",
        },
        {
            "data": "m=edit&p=7VZdT9tIFH3nV1R+7Ujr8fhb2odAk267kIYCYkkUIRMMCXUw6zjAGvHfe+74Gn8kdFfVPrDSyvHM8ZmZe8+9M7n26s91lMVCmvRTvkCPy5a+vi3f1bfJ1/EiT+Lwneit83maAQjxZTAQV1GyisXns/n+Xtp7+ND7497Px2P50Vx/Mk9vBjfvvy5//7RQmRwM/dHB6GBhXfd+29s9dPvv3dF6dZLH94dLuXtzMj6+Gp1eB9Zf/eHYLsZfTOfz+OqX+97JrzsT1jDdeSqCsOiJ4mM4MaQhDAu3NKaiOAyfioOw6IviCEOGkFNhLNdJvpilSZoZFVfslwstwH4NT/U4ob2SlCbwkDHgGWD6eL5bPo3CSXEsDPK7q1cSNJbpfUyOSBc9z9LlxYKIiyhH6lbzxZ0hFAZW68v025qnyumzKHql+rN/qB5GKvUES/WEtqinoFh9/99XH0yfn7EpX6H/PJxQKCc19Gt4FD6hHepW6vYsfDJsF2YsUWfWcKwuE8guI5UJSrYpsqRqCg4G2o2l22OoEIXS7Qfdmrp1dLuv5/QhyFKBsGyYh0P0wPBO2PJqLJXAc81bPmP8Z2zo12stYMUY8x2e72C+w/Ntu41tp8RKNjA0qEoDtFHoWoMDvwGvBaZM6vnklzH9hxXrcYAdnu/Ajst2XNh32b4NbRVW0GyzZkl+q1goD5VmirfSADuOzfYpLtbvQJvLc1zY8dmOD51NHLDmwBVKltqUGdTYUkJZpX30wKV9JWUbS4438BsYmgPW7COuoIwL64RSpTb0QjmlHo35DCgLepqY9x09+DJX6IFLX+hhp4wF/qGBbeLMKMn6Jekv9aB/WWv5yNuLTmCfc+gjhz7nB/VYmVV+ULSbNmWVB8QlWYNJGqq18GVWvpATv/JFdZ732sM++tU+gvf4nBB+OcPYd4/teLSPbJ/OksdrPdLPMUpo5nOLHvGyZpx5xeccPfJW7QXlk3nCfIbRA1f5RCwVb1Ls7MtEnk3W4GMfzeqM4ewFHIuHWF4wcuuxftLscc5dxFXxhF2ygyJxqkvFnm5t3bq6hHhU5n66EP5ctfpbORNkm97o7cv573HTnYnRv7yO3w3TbBkleEMdzaO72MD3gLFKk/PVOruKZvF5/BjNciMsP0maIy3udr28iPFSbVBJmt4li9ttFqqhFrm4vk2zeOsQkTG0vmKKhraYukizy46mhyhJ2rHoz7UWNVtks6RN5Rne2o3nKMvShxazjPJ5i2i84VuW4ttOMvOoLTH6FnW8Let0PO8Yj4a+8WK2/v94e6Mfb7RB5lurXG9Njj7bafaDQlMPdukt5QbsDypOY3Qb/0pxaYx2+Y1KQmI3iwnYLfUEbLekgNqsKiA3Cgu4V2oLWe2WF1LVrTDkaqPIkKtmnZlMd74D",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(colors=["ox_E__1", "ox_E__2", "ox_E__3", "white"]))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(alternation_constraint())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(1, color="ox_E__1", _type="area", _id=i))
            self.add_program_line(count(1, color="ox_E__2", _type="area", _id=i))
            self.add_program_line(count(1, color="ox_E__3", _type="area", _id=i))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            symbol, style = symbol_name.split("__")
            validate_type(symbol, ("ox_B", "ox_E"))
            fail_false(style in ["1", "2", "3", "4", "7", "8"], f"Invalid symbol at ({r}, {c}).")
            if style in ["1", "2", "3"]:
                self.add_program_line(f"ox_E__{style}({r}, {c}).")
            else:
                self.add_program_line(f"white({r}, {c}).")

        self.add_program_line(display(item="ox_E__1"))
        self.add_program_line(display(item="ox_E__2"))
        self.add_program_line(display(item="ox_E__3"))

        return self.program
