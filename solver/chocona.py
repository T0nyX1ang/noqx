"""The Chocona solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import all_rect


class ChoconaSolver(Solver):
    """The Chocona solver."""

    name = "Chocona"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZdLbxs3FIX3/hXBrLkYvkltCje1u3GdtnZQBIJgyIrSGLWhVLaKYgz9957LORxahdv0gaabQNb4kMP7GF59V9T9z7vldq20lT+bVK80Xt6a8tbOlXfP1+XNw+169kId7x7eb7YQSr06PVXvlrf366M5Vy2OHoc8G47V8PVs3ulOdQZv3S3U8N3scfhmNpyo4QK3OpUwdzYuMpAnTf5Q7ot6OU7qHvqcGvIN5Opmu7pdX52NM9/O5sOl6iTOl8VaZHe3+WXdMQ8ZrzZ31zcycb18wMPcv7/5wDv3u7ebn3ZdDbFXw/GY7sUz6dqWrp3Stc+na/77dPNiv8e2f4+Er2Zzyf11k6nJi9njXvJ67GyAKao+VqZzFkPdt/Hhbe/k9jSM+uBulMVhGuq+rG7LtZb1zbk2/nDsjBiYJxPiofuiazPBHppEf5CCjvHwfsri0k0TRouD3MbGHjgwVnLwT8aHj2y8fjLGJuqylW/K9bRcTbleYqfVYMv1q3Lty9WX61lZcyIF6LOyBjtnVGexWdYkagOdqZ2yVlMHaEsdod2ojVdWNrBorHFcYxK0H7XtoSM1YjnGsrD1tLWw9bR1yMEzB/BvA3NwWB+43iGHwBwcniXwWTxiBcbymI+cD4gbGTdIs+mp4T/Rf0DOiTkH2CbaRsTKjBWxJnNNQqzMWAk5Z+acrHI9/ScPzZxThKafHJTTfN6MeT3Ou15DJ2oDnamdcmbM04EUZyI11rN28Kec7akR1xpqxGLt4Bt6zN8Z+LH0Y+DH0o9BPo75mAw97gN8Q3O9RT6e+aCOjnWEnXKsF+ygGdchbmBc1MuxXvABzbge+Ufm7+En0k/APkTuA2rnWDsXkGdinqidY+3gA5p5Rtgm2ibEyoyFerlc553yPWOlAM2cUS/PesEHNHPOXnnN50UdPevo+x46UuN7jHWEP+VNTw1bY6hha2gL1jxZ86idZ+3gD9pRIwc75gB/0Ixl5PsyNx4r18JgZRl1tPxsFB4r19Y2lq3wXpmFH8YqPFauhcfKtTBYWXbCe2UWsTxjedO4Rn2tZyyfGuPCZuVa2Kxch9BYDsJ75Re2gbbRN8Yj1sfYmK28C6eVcXwGwGpjNtmJ04l31N0m2mbXeEetJ95znhjHf2jd+CXvhdmen0n0W3Db+NWVZdvYF2Z1aJxW9lF3x89PYbb2AeG0so9aO9a6MFv7AM5RE/vCbGXfxsa7lZ5AW2cb+8Jv5d1JT0iNZda68FvZF3595bFvfUD4rX0g+MZ+kP4QG8u1Dwi/lf0I/9E0liP9xNz6QBLeK79Yz/oK11NPANdTTwDLLtMW9XWsr3ANnqlT6w9Z2K/89lOvKFyzPxSu2R/QG1pPQH29rvyCce0b17U/oNaetS6M114hXJf+sJcznnx1vyxXV66hfKVHOVr9xcNXOUil8QBlxpPYvz9KfDS3uQ3lWP/cy3++80/uLI7m3cVu+265WuM8fvL2x/WL8832bnmL0fnu7nq9rWP8HNofdb925V0OnO7zL6T/6ReSlKD/W7+TPgGdH0lnjt2V3+DDK9V92F0tr1YbfMiweX96w//BPJr57+c/+fOiIS2OfgM=",
        },
        {
            "url": "https://puzz.link/p?chocona/26/22/885kcco5lc912qccuksc8u9k8cdbs24ujt2ctre2ifbuagd77ah6bbjpubmjvt7n57t4gldt0oa6t0gi3uci41s4icrs32ar3j7cqhjpkk2lik3g3302fuitovkgv3g7tge73ifv7jejuc0r4v3ei4e1o79r01jpqune0kg1ov1f300bf783vukb00fg2mvvvggs0tvovs0g3frku1s0tg7v270064a13422432332444724242322633942221232249322222423462242621324325398321344611532442412253236225",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("gray"))
        self.add_program_line(adjacent())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count(num, color="gray", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(all_rect(color="gray"))
        self.add_program_line(display(item="gray"))

        return self.program
