"""Solve Symmetry Area puzzles."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import count_reachable_src, grid_src_color_connected


def fillomino_constraint() -> str:
    """Generate the Fillomino constraints."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")

    # propagation of number
    rule = f"number(R, C, N) :- number(R0, C0, N), {tag}(R0, C0, R, C).\n"
    # this is a huge optimization
    rule += ":- grid(R, C), number(R, C, N1), number(R, C, N2), N1 < N2.\n"

    # same number, adjacent cell, no line
    rule += f':- number(R, C, N), number(R, C + 1, N), edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- number(R, C, N), number(R + 1, C, N), edge(R + 1, C, "{Direction.TOP}").\n'

    # different number, adjacent cell, have line
    rule += f':- number(R, C, N1), number(R, C + 1, N2), N1 != N2, not edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- number(R, C, N1), number(R + 1, C, N2), N1 != N2, not edge(R + 1, C, "{Direction.TOP}").\n'

    # special case for 1
    mutual = [
        f'edge(R, C, "{Direction.TOP}")',
        f'edge(R + 1, C, "{Direction.TOP}")',
        f'edge(R, C, "{Direction.LEFT}")',
        f'edge(R, C + 1, "{Direction.LEFT}")',
    ]
    rule += f"{{ {'; '.join(mutual)} }} = 4 :- number(R, C, 1).\n"
    rule += f"number(R, C, 1) :- {', '.join(mutual)}.\n"
    rule += ":- number(R, C, 1), number(R1, C1, 1), adj_4(R, C, R1, C1).\n"

    return rule


def fillomino_filtered(fast: bool = False) -> str:
    """Generate the Fillomino filtered connection constraints."""
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")
    rule = ""
    tag1 = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    rule += f"have_numberx(R, C) :- grid(R, C), not {tag1}(_, _, R, C).\n"

    rule += f"{tag}(R, C, R, C) :- grid(R, C), have_numberx(R, C).\n"
    rule += f"{tag}(R, C, R0, C0) :- grid(R0, C0), grid(R, C), {tag}(R, C, R1, C1), have_numberx(R0, C0), have_numberx(R, C), adj_edge(R0, C0, R1, C1).\n"

    if fast:
        rule += "{ numberx(R, C, 1..5) } = 1 :- grid(R, C), have_numberx(R, C).\n"
        rule += f":- numberx(R, C, N), #count{{ R1, C1: {tag}(R, C, R1, C1) }} != N.\n"
    else:
        rule += f"{{ numberx(R, C, N) }} = 1 :- grid(R, C), have_numberx(R, C), #count{{ R1, C1: {tag}(R, C, R1, C1) }} = N.\n"
    rule += ":- number(R, C, N), numberx(R1, C1, N), adj_4(R, C, R1, C1)."

    rule += f':- numberx(R, C, N), numberx(R, C + 1, N), edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- numberx(R, C, N), numberx(R + 1, C, N), edge(R + 1, C, "{Direction.TOP}").\n'
    rule += f':- have_numberx(R, C), have_numberx(R, C + 1), numberx(R, C, N), not numberx(R, C + 1, N), not edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- have_numberx(R, C), have_numberx(R + 1, C), numberx(R, C, N), not numberx(R + 1, C, N), not edge(R + 1, C, "{Direction.TOP}").\n'

    return rule


def symmetry_area(fast: bool = False) -> str:
    """Force central symmetry of areas."""

    tag_number = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    tag_numberx = tag_encode("reachable", "grid", "branch", "adj", "edge")

    # number
    rule = f"min_r(R, C, MR) :- clue(R, C), MR = #min {{ R1: grid(R1, C1), {tag_number}(R, C, R1, C1) }}.\n"
    rule += f"max_r(R, C, MR) :- clue(R, C), MR = #max {{ R1: grid(R1, C1), {tag_number}(R, C, R1, C1) }}.\n"
    rule += f"min_c(R, C, MC) :- clue(R, C), MC = #min {{ C1: grid(R1, C1), {tag_number}(R, C, R1, C1) }}.\n"
    rule += f"max_c(R, C, MC) :- clue(R, C), MC = #max {{ C1: grid(R1, C1), {tag_number}(R, C, R1, C1) }}.\n"
    rule += "symm_coord_sum(R, C, SR, SC) :- clue(R, C), min_r(R, C, MINR), max_r(R, C, MAXR), min_c(R, C, MINC), max_c(R, C, MAXC), SR = MINR + MAXR, SC = MINC + MAXC.\n"

    rule += f":- clue(R0, C0), clue(R1, C1), {tag_number}(R0, C0, R1, C1), symm_coord_sum(R0, C0, SR, SC), not symm_coord_sum(R1, C1, SR, SC).\n"
    rule += (
        f":- clue(R, C), symm_coord_sum(R, C, SR, SC), {tag_number}(R, C, R0, C0), not {tag_number}(R, C, SR - R0, SC - C0).\n"
    )

    # numberx
    if not fast:
        rule += "{ min_rx(R, C, MR) : grid(MR, _) } = 1 :- grid(R, C), have_numberx(R, C).\n"
        rule += "{ max_rx(R, C, MR) : grid(MR, _) } = 1 :- grid(R, C), have_numberx(R, C).\n"
        rule += "{ min_cx(R, C, MC) : grid(_, MC) } = 1 :- grid(R, C), have_numberx(R, C).\n"
        rule += "{ max_cx(R, C, MC) : grid(_, MC) } = 1 :- grid(R, C), have_numberx(R, C).\n"

        rule += f"min_rx(R, C, MR) :- have_numberx(R, C), MR = #min {{ R1: grid(R1, C1), {tag_numberx}(R, C, R1, C1) }}, grid(MR, _).\n"
        rule += f"max_rx(R, C, MR) :- have_numberx(R, C), MR = #max {{ R1: grid(R1, C1), {tag_numberx}(R, C, R1, C1) }}, grid(MR, _).\n"
        rule += f"min_cx(R, C, MC) :- have_numberx(R, C), MC = #min {{ C1: grid(R1, C1), {tag_numberx}(R, C, R1, C1) }}, grid(_, MC).\n"
        rule += f"max_cx(R, C, MC) :- have_numberx(R, C), MC = #max {{ C1: grid(R1, C1), {tag_numberx}(R, C, R1, C1) }}, grid(_, MC).\n"

        rule += ":- have_numberx(R, C), adj_edge(R0, C0, R, C), min_rx(R0, C0, MR), not min_rx(R, C, MR).\n"
        rule += ":- have_numberx(R, C), adj_edge(R0, C0, R, C), max_rx(R0, C0, MR), not max_rx(R, C, MR).\n"
        rule += ":- have_numberx(R, C), adj_edge(R0, C0, R, C), min_cx(R0, C0, MC), not min_cx(R, C, MC).\n"
        rule += ":- have_numberx(R, C), adj_edge(R0, C0, R, C), max_cx(R0, C0, MC), not max_cx(R, C, MC).\n"

        # # the following two lines accelerates example 5 but slows example 1 and 4
        # rule += f":- have_numberx(R, C), min_cx(R, C, MINC), max_cx(R, C, MAXC), SC = MINC + MAXC, N1 = #count {{ R1 : grid(R1, C), {tag_numberx}(R, C, R1, C) }}, N2 = #count {{ R1 : grid(R1, SC - C), {tag_numberx}(R, C, R1, SC - C) }}, N1 != N2.\n"
        # rule += f":- have_numberx(R, C), min_rx(R, C, MINR), max_rx(R, C, MAXR), SR = MINR + MAXR, N1 = #count {{ C1 : grid(R, C1), {tag_numberx}(R, C, R, C1) }}, N2 = #count {{ C1 : grid(SR - R, C1), {tag_numberx}(R, C, SR - R, C1) }}, N1 != N2.\n"

        rule += "symm_coord_sumx(R, C, SR, SC) :- grid(R, C), have_numberx(R, C), min_rx(R, C, MINR), max_rx(R, C, MAXR), min_cx(R, C, MINC), max_cx(R, C, MAXC), SR = MINR + MAXR, SC = MINC + MAXC.\n"
        rule += f":- have_numberx(R, C), symm_coord_sumx(R, C, SR, SC), not {tag_numberx}(R, C, SR - R, SC - C).\n"

    return rule


class SymmareaSolver(Solver):
    """The Symmetry Area solver."""

    name = "Symmetry Area"
    category = "num"
    aliases = ["symmetryarea"]
    examples = [
        {
            "data": "m=edit&p=7VNNT8JAFLz3V5A9v0O7Wwr0hgheEFQwhDRNU0oVIqRYqDHb9L/79rW1pCEaTUQPZrOT6exsd/bj7Z8TPw7BwibaoIOBjVsWdcM0qetFm64Pm9BuQDc5rKIYCcB4MIAHf7MPNadwuVoqO7bsgryyHcYZUDeYC/LWTuW1LUcgJzjEwEBtiMxgwJH2KzqjccV6uWjoyEcFRzpHGqzjYBN6w1y5sR05BabWuaDZirJt9BKyfBp9B9F2sVbCwj/gZvar9a4Y2SfL6Clh5RIZyG4et38irqjiive44nRc/vNxO26W4bHfYWDPdlT2+4q2Kzqx00zlShkX5U7zu2G8VRMEOawjgRztSjA5y2+4FJrkaFaCRQ5xJFg1R4vXlm2RwywFjGtQ6DnhgJATTnFPIAXhJaFO2CQckqdPOCPsEZqEFnla6lS+dG5niONwTkWYt+b3uas5rL98DBujKN76G3w3o2S7COPyGws109gro+4InGL+1+4v1a66Av2vvcRP4jj4GLiA/JyK6t0lnu8FET42PERlEMpgfWDAP8jx6Yl1/ez7x2J0tTc=",
        },
        {
            "data": "m=edit&p=7VffbxMxDH7vX4HynIdLnKR3fRuj42WMX0MTqqqp6wpMbCp0K0I39X/nS+Lb7WC+Cg2GQKi93OfYTmwntd3Lz+vZaqFNEb9UarzxcaZMjy1Degr+HJ5dnS9Gj/TO+urDcgWg9fO9Pf1udn65GExYajq4rqtRvaPrp6OJskqnx6iprl+Orutno/pA16/BUtpgbh/IKG0Bxy08SvyIdvOkKYAPGAO+BZyfrebni+P9PPNiNKkPtYr7PE7aEaqL5ZeFymqJni8vTs7ixMnsCs5cfjj7xJzL9eny41o1W2x0vZPNHd9hLrXm0o25dLe59vebW003G4T9FQw+Hk2i7W9aWLbw9eh6E+26VlRAlXDW6WQUGZCmJS1I15LU5TqQviU9yKolA0jbkkOQoSXLrm7VMaMMnaVMUXXWMj50tI2Pi5e36PI7+ag/bOnQ9dqErtsm2K5+oO/kXXe/4G/FCZE1Kb5v07iXRpvGQ4Rf15TGJ2ks0ujTuJ9kxmk8SuNuGl0aQ5IZxgP8qSO+vznKWcSjKrVy8VAjsMZqa0EQsEV2cEXGrtDWu4w9tTjK2GHGhm5hB1yyDDKNrXje38LQJV7fDIENY8jHG5pwBUy8Dmwg3pewvuP1HeQDywfYH7I8OavJhxa7Zp4wn+0kW7XzEbM9eGPesbyDfMnzkPGNvId81WKOG97Q5XUQN+JYEfy9WT9iwzbAd2Lf8YauZ12s6TlWmLc8jzcwnxHZG0wOa4bG/ugvzyOexPGkAr6YssUF74XaQJ5lHGzwcX7rfZ1QLijdj//75qaDiRqfvl88OliuLmbnyMEH64uTxaqhUfQ2A/VVpSdlDPe/Dv6hOhiPoHjgVHnfzD1BdG+Sq66fa/VpfTw7ni9x1RDCzOZ8K7E5Bd/NRioXGBSkBTmP95mDdC6xOduL2kjozsjOIJ8hx4imIcWFSmQHVIWhHCkfetmoBRCRLUc5cVb2O1e2Pm0rW871T2Tnkiiyc5UU2blwiuxcS0XLc3mV2FxxxaDmIiyeWK7LArspPxLbolKRuDfF/zZWtryKtVYOagnTKvk6lLippezYNnb/4v2mbXFsW1j6g/rP/kKbvq+P7eSryN2hGPOqV5t7SPFIclsp7p07TVE7N5/i3rkf7WPL1afpWkXTciMr3tTQ6ze3uyI7d8Ci37kpFk3LfbKYuHLrLN613E2L2raP3fTcouW5DRf9zp25xOZmvY9dSI45/EiEhsAIDETiV2lIm2/N9Pzf4wf2g/dz+HMzHXwD",
            "config": {"fast_mode": True},
        },
        {
            "url": "https://pzplus.tck.mn/p?symmarea/10/10/5o2g3mag5g8lah7g7j5g7h2g1hag5h6g6j2g6halbg1g2m5g1o3",
            "config": {"fast_mode": True},
            "test": False,
        },
        {"url": "https://pzplus.tck.mn/p?symmarea/10/10/h1i5j4g4g1g1h1g2g1i1h4g4g1g1j4k1h4i9g1h1i4t1j1l1i1j", "test": False},
        {"url": "https://pzplus.tck.mn/p?symmarea/12/12/z1lbj3k17j736x12p26y15j584j-1bj-14q1u", "test": False},
    ]
    parameters = {"fast_mode": {"name": "Fast Mode", "type": "checkbox", "default": False}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(fillomino_constraint())
        self.add_program_line(fillomino_filtered(fast=puzzle.param["fast_mode"]))
        self.add_program_line(symmetry_area(fast=puzzle.param["fast_mode"]))

        numberx_ub = puzzle.row * puzzle.col - sum({num for _, num in puzzle.text.items() if isinstance(num, int)})
        self.add_program_line(f":- #count{{ R, C: grid(R, C), have_numberx(R, C) }} > {numberx_ub}.")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")
            self.add_program_line(f"clue({r}, {c}).")
            self.add_program_line(grid_src_color_connected(src_cell=(r, c), color=None, adj_type="edge"))
            self.add_program_line(count_reachable_src(target=int(num), src_cell=(r, c), color=None, adj_type="edge"))

            if num == 1:
                self.add_program_line(f'edge({r}, {c}, "{Direction.LEFT}").')
                self.add_program_line(f'edge({r}, {c}, "{Direction.TOP}").')
                self.add_program_line(f'edge({r}, {c + 1}, "{Direction.LEFT}").')
                self.add_program_line(f'edge({r + 1}, {c}, "{Direction.TOP}").')

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))
        self.add_program_line(display(item="number", size=3))
        self.add_program_line(display(item="numberx", size=3))

        return self.program
