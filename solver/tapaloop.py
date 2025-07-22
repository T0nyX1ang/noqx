"""The Tapa-like Loop solver."""

from typing import Dict, List, Set, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected

direc = ((-1, -1, "r"), (-1, 0, "r"), (-1, 1, "d"), (0, 1, "d"), (1, 1, "l"), (1, 0, "l"), (1, -1, "u"), (0, -1, "u"))
direc_outer = ((-1, -1, "l"), (-1, 1, "u"), (1, 1, "r"), (1, -1, "d"))
pattern_ref = "())*)**+)**+*++,-.././/0-.././/0--....//..////001122223311222233--....//..////0044555566445555661!2!2!3!2!3!3!7!8!9!9!:!8!9!9!:!-.-.././././/0/045455656454556564444555555556666;;;;<<<<;;;;<<<<1111222222223333;;;;<<<<;;;;<<<<8!8!9!9!9!9!:!:!=!=!>!>!=!=!>!>!-.-.././././/0/045455656454556564444555555556666;;;;<<<<;;;;<<<<4444555555556666????@@@@????@@@@;!;!<!<!<!<!A!A!B!B!C!C!B!B!C!C!12!!23!!23!!37!!;<!!<A!!;<!!<A!!;;!!<<!!<<!!AA!!DD!!EE!!DD!!EE!!88!!99!!99!!::!!BB!!CC!!BB!!CC!!=!!!>!!!>!!!F!!!G!!!H!!!G!!!H!!!-../-.././/0.//045564556455645564455445555665566;;<<;;<<;;<<;;<<4455445555665566??@@??@@??@@??@@;!<!;!<!<!A!<!A!B!C!B!C!B!C!B!C!4545454556565656?@?@?@?@?@?@?@?@????????@@@@@@@@IIIIIIIIIIIIIIII;;;;;;;;<<<<<<<<IIIIIIIIIIIIIIIIB!B!B!B!C!C!C!C!J!J!J!J!J!J!J!J!1212121223232323;<;<;<;<;<;<;<;<;;;;;;;;<<<<<<<<DDDDDDDDDDDDDDDD;;;;;;;;<<<<<<<<IIIIIIIIIIIIIIIID!D!D!D!E!E!E!E!K!K!K!K!K!K!K!K!89!!89!!9:!!9:!!BC!!BC!!BC!!BC!!BB!!BB!!CC!!CC!!KK!!KK!!KK!!KK!!==!!==!!>>!!>>!!JJ!!JJ!!JJ!!JJ!!G!!!G!!!H!!!H!!!L!!!L!!!L!!!L!!!-../-.././/0.//045564556455645564455445555665566;;<<;;<<;;<<;;<<4455445555665566??@@??@@??@@??@@;!<!;!<!<!A!<!A!B!C!B!C!B!C!B!C!4545454556565656?@?@?@?@?@?@?@?@????????@@@@@@@@IIIIIIIIIIIIIIII;;;;;;;;<<<<<<<<IIIIIIIIIIIIIIIIB!B!B!B!C!C!C!C!J!J!J!J!J!J!J!J!4545454556565656?@?@?@?@?@?@?@?@????????@@@@@@@@IIIIIIIIIIIIIIII????????@@@@@@@@MMMMMMMMMMMMMMMMI!I!I!I!N!N!N!N!O!O!O!O!O!O!O!O!;<!!;<!!<A!!<A!!IN!!IN!!IN!!IN!!II!!II!!NN!!NN!!PP!!PP!!PP!!PP!!BB!!BB!!CC!!CC!!OO!!OO!!OO!!OO!!J!!!J!!!Q!!!Q!!!R!!!R!!!R!!!R!!!1223!!!!2337!!!!;<<A!!!!;<<A!!!!;;<<!!!!<<AA!!!!DDEE!!!!DDEE!!!!;;<<!!!!<<AA!!!!IINN!!!!IINN!!!!D!E!!!!!E!S!!!!!K!T!!!!!K!T!!!!!;<;<!!!!<A<A!!!!ININ!!!!ININ!!!!IIII!!!!NNNN!!!!PPPP!!!!PPPP!!!!DDDD!!!!EEEE!!!!PPPP!!!!PPPP!!!!K!K!!!!!T!T!!!!!U!U!!!!!U!U!!!!!8989!!!!9:9:!!!!BCBC!!!!BCBC!!!!BBBB!!!!CCCC!!!!KKKK!!!!KKKK!!!!BBBB!!!!CCCC!!!!OOOO!!!!OOOO!!!!K!K!!!!!T!T!!!!!V!V!!!!!V!V!!!!!=>!!!!!!>F!!!!!!JQ!!!!!!JQ!!!!!!JJ!!!!!!QQ!!!!!!UU!!!!!!UU!!!!!!GG!!!!!!HH!!!!!!RR!!!!!!RR!!!!!!L!!!!!!!W!!!!!!!X!!!!!!!X!!!!!!!-.././/0-.././/012232337!!!!!!!!4455556644555566889999::!!!!!!!!4455556644555566;;<<<<AA!!!!!!!!;!<!<!A!;!<!<!A!=!>!>!F!!!!!!!!!4545565645455656;<;<<A<A!!!!!!!!????@@@@????@@@@BBBBCCCC!!!!!!!!;;;;<<<<;;;;<<<<DDDDEEEE!!!!!!!!B!B!C!C!B!B!C!C!G!G!H!H!!!!!!!!!4545565645455656;<;<<A<A!!!!!!!!????@@@@????@@@@BBBBCCCC!!!!!!!!????@@@@????@@@@IIIINNNN!!!!!!!!I!I!N!N!I!I!N!N!J!J!Q!Q!!!!!!!!!;<!!<A!!;<!!<A!!DE!!ES!!!!!!!!!!II!!NN!!II!!NN!!KK!!TT!!!!!!!!!!BB!!CC!!BB!!CC!!KK!!TT!!!!!!!!!!J!!!Q!!!J!!!Q!!!L!!!W!!!!!!!!!!!4556455645564556;<<A;<<A!!!!!!!!??@@??@@??@@??@@BBCCBBCC!!!!!!!!??@@??@@??@@??@@IINNIINN!!!!!!!!I!N!I!N!I!N!I!N!J!Q!J!Q!!!!!!!!!?@?@?@?@?@?@?@?@ININININ!!!!!!!!MMMMMMMMMMMMMMMMOOOOOOOO!!!!!!!!IIIIIIIIIIIIIIIIPPPPPPPP!!!!!!!!O!O!O!O!O!O!O!O!R!R!R!R!!!!!!!!!;<;<;<;<;<;<;<;<DEDEDEDE!!!!!!!!IIIIIIIIIIIIIIIIKKKKKKKK!!!!!!!!IIIIIIIIIIIIIIIIPPPPPPPP!!!!!!!!P!P!P!P!P!P!P!P!U!U!U!U!!!!!!!!!BC!!BC!!BC!!BC!!KT!!KT!!!!!!!!!!OO!!OO!!OO!!OO!!VV!!VV!!!!!!!!!!JJ!!JJ!!JJ!!JJ!!UU!!UU!!!!!!!!!!R!!!R!!!R!!!R!!!X!!!X!!!!!!!!!!!1223122312231223899:899:!!!!!!!!;;<<;;<<;;<<;;<<==>>==>>!!!!!!!!;;<<;;<<;;<<;;<<BBCCBBCC!!!!!!!!D!E!D!E!D!E!D!E!G!H!G!H!!!!!!!!!;<;<;<;<;<;<;<;<BCBCBCBC!!!!!!!!IIIIIIIIIIIIIIIIJJJJJJJJ!!!!!!!!DDDDDDDDDDDDDDDDKKKKKKKK!!!!!!!!K!K!K!K!K!K!K!K!L!L!L!L!!!!!!!!!;<;<;<;<;<;<;<;<BCBCBCBC!!!!!!!!IIIIIIIIIIIIIIIIJJJJJJJJ!!!!!!!!IIIIIIIIIIIIIIIIOOOOOOOO!!!!!!!!P!P!P!P!P!P!P!P!R!R!R!R!!!!!!!!!DE!!DE!!DE!!DE!!KT!!KT!!!!!!!!!!PP!!PP!!PP!!PP!!UU!!UU!!!!!!!!!!KK!!KK!!KK!!KK!!VV!!VV!!!!!!!!!!U!!!U!!!U!!!U!!!X!!!X!!!!!!!!!!!899:!!!!899:!!!!=>>F!!!!!!!!!!!!BBCC!!!!BBCC!!!!GGHH!!!!!!!!!!!!BBCC!!!!BBCC!!!!JJQQ!!!!!!!!!!!!K!T!!!!!K!T!!!!!L!W!!!!!!!!!!!!!BCBC!!!!BCBC!!!!JQJQ!!!!!!!!!!!!OOOO!!!!OOOO!!!!RRRR!!!!!!!!!!!!KKKK!!!!KKKK!!!!UUUU!!!!!!!!!!!!V!V!!!!!V!V!!!!!X!X!!!!!!!!!!!!!=>=>!!!!=>=>!!!!GHGH!!!!!!!!!!!!JJJJ!!!!JJJJ!!!!LLLL!!!!!!!!!!!!JJJJ!!!!JJJJ!!!!RRRR!!!!!!!!!!!!U!U!!!!!U!U!!!!!X!X!!!!!!!!!!!!!GH!!!!!!GH!!!!!!LW!!!!!!!!!!!!!!RR!!!!!!RR!!!!!!XX!!!!!!!!!!!!!!LL!!!!!!LL!!!!!!XX!!!!!!!!!!!!!!X!!!!!!!X!!!!!!!X!!!!!!!!!!!!!!!"  # fmt: skip  # formula: chr(pattern_idx.value()) + 40 (invalid patterns are "!")
pattern_idx: Dict[Tuple[int, ...], int] = {(0,): 0, (1,): 1, (1, 1): 2, (1, 1, 1): 3, (1, 1, 1, 1): 4, (2,): 5, (1, 2): 6, (1, 1, 2): 7, (1, 1, 1, 2): 8, (3,): 9, (1, 3): 10, (1, 1, 3): 11, (2, 2): 12, (1, 2, 2): 13, (1, 1, 2, 2): 14, (1, 1, 1, 3): 15, (4,): 16, (1, 4): 17, (1, 1, 4): 18, (2, 3): 19, (1, 2, 3): 20, (5,): 21, (1, 5): 22, (2, 2, 2): 23, (1, 2, 2, 2): 24, (1, 1, 2, 3): 25, (2, 4): 26, (1, 2, 4): 27, (3, 3): 28, (1, 3, 3): 29, (1, 1, 5): 30, (6,): 31, (1, 6): 32, (2, 2, 3): 33, (2, 5): 34, (3, 4): 35, (7,): 36, (2, 2, 2, 2): 37, (1, 2, 2, 3): 38, (2, 2, 4): 39, (2, 3, 3): 40, (1, 2, 5): 41, (2, 6): 42, (1, 1, 3, 3): 43, (1, 3, 4): 44, (3, 5): 45, (4, 4): 46, (1, 7): 47, (8,): 48}  # fmt: skip


def tapaloop_pattern_rule() -> str:
    """Generate pattern reference dictionary and tapaloop pattern map."""
    return "\n".join(f"valid_tapaloop_map({ord(pattern_ref[v]) - 40}, {v})." for v in range(4096) if pattern_ref[v] != "!")


def clue_in_target(clue: List[Union[int, str]], target: List[int]) -> bool:
    """Check if clue is in target."""
    for c in clue:
        if c == "?":
            continue
        if c not in target:
            return False
        target.remove(c)

    return True


def parse_clue(r: int, c: int, clue: List[Union[int, str]]) -> str:
    """Parse tapa clue to binary pattern."""
    result: Set[int] = set()
    for pattern in filter(lambda x: len(x) == len(clue), pattern_idx.keys()):
        if clue_in_target(clue, list(pattern)):
            result.add(pattern_idx[pattern])

    return "\n".join(f"valid_tapaloop({r}, {c}, {num})." for num in result)


def direction_to_binary(r: int, c: int) -> str:
    """Convert grid direction to numbers."""
    constraint = f"binary(R, C, D, 0) :- -1 <= R, R <= {r}, -1 <= C, C <= {c}, not grid(R, C), direction(D).\n"
    constraint += "binary(R, C, D, 0) :- grid(R, C), direction(D), not grid_direction(R, C, D).\n"
    constraint += "binary(R, C, D, 1) :- grid(R, C), grid_direction(R, C, D)."
    return constraint


def valid_tapaloop(r: int, c: int) -> str:
    """Generate rules for a valid tapa-loop clue."""
    num_seg: List[str] = []
    binary_seg: List[str] = []
    for i, (dr, dc, d) in enumerate(direc + direc_outer):
        binary_seg.append(f"{2 ** (11 - i)} * N{i}")
        num_seg.append(f'binary({r + dr}, {c + dc}, "{d}", N{i})')
    rule = f":- not valid_tapaloop({r}, {c}, P), valid_tapaloop_map(P, N), {', '.join(num_seg)}, N = {' + '.join(binary_seg)}."
    return rule


class TapaloopSolver(Solver):
    """The Tapa-like Loop solver."""

    name = "Tapa-Like Loop"
    category = "loop"
    aliases = ["tapalikeloop", "tapa-like-loop", "tapalike", "tapa-like", "tll"]
    examples = [
        {
            "data": "m=edit&p=7ZZrT/JIFMff8ynMvHUSOxSwNDGGq4lBlBUfVhtCBihSGRjsRUmJ390zpyC9afaJG7NPsoEeTn+nPZcZ+BfvOeCuTZmm3rpB4RNeJWbgUTQqeGi7V9/xhW0e0Vrgz6ULDqXX7TadceHZ9PL+qd5c1F5btb9Pyg+6ftedHT81e3dP08Ev1tOcE1frCmN1ddOsi+OL8OFqXnuxW3blxpOTubD5lIcPg8uNWLWNx/mMNS7nDWPGV5r3bPSrL/Xe2VnB2jUyLGzDqhnWaHhhWqRIKB6MDGnYM7fhlRl2aXgLIUIZsA54jNAiuK2DO8C48hoRZBr4XfBL0W334E4cdyLsUSciN6YV9ilRdep4t3LJUr7YJEqB5xO5HDsKjLkP6+XNnfUu4gVTuQh210JCsgyE70ykkK6Cir3RsBaN0MkZQT+MoNxoBOXljKAm+/YIwlnZcpPXfjW//TfYmr9ggJFpqVnuDq5xcG/NLdiuuSW6pu6E3WMUeoaUejUFKgyBGm5Pioqcn8eIniElbJPF0CkiPU6wVpwYBhaLEaZhNT1GWAWrxUgRp1Bfmw+CXcfLs2jUBCmn22alHBSVS6DTLMLO46SCqT5WEhac4bLfo22jLaLtw67QUEfbRKuhLaPt4DUttAO0DbQltBW85lTt62/t/Hfagf2GTaka8G0BrYIxdfQU1P9hq5YeKV3yVf7z2LBgkQ78SI+60l1yAb/UbrAc2+7+HKSSeFKMvMCd8Yk9sjd84hMzkux4JMFWmCOBhJRrpQY5GfahBHQeV9K1c0MK2tPHz1KpUE6qsXSnqZ5euRDJWfBxlkCR/CWQ74K2xc6568rXBFlyf54AMSlPZLJXqcX0ebJFvuCpasvDcrwVyIbgYenqsfv/c+0//FxT26T9mMb9O5JrwWrvRJKG15SsgxEfwWAE/kPRfRB0Mz8IMpsJ/PiA+JuR7hcCdgimcY6MAf1CyWLRPP6JaMWiaZ5RKNVsVqSA5ugU0LRUAcqqFcCMYAH7RLNU1rRsqa7SyqVKZcRLlYrrl0V8vubCWaDSk2HhHQ==",
        },
        {
            "data": "m=edit&p=7ZZta+pKEMff+ynKvu1Ck2y0MVCKj4VivfXWHm8bRFaNNXV12yS2Eul37+xEMU8WLgcO5VBihslvdmdnsvLfBK9r7rtUr6gfs6hGdbgqZgXvslXFW9tdfS8Urn1Ca+twLn1wKP2n3aYzLgKXXj8815uL2nur9t9Z+ZGx++7s9LnZu3+eDn7pPc0787WusFY3t826OL2KHm/mtTe35VZuAzmZC5dPefQ4uN6IVdt6ms/0xvW8Yc34SgterX71rd67uCg5u0KGpW1UtaMaja5shxiE4q2TIY169ja6saMuje4gRKgOrAOeTqgBbuvgDjCuvEYMdQ38LvhmPO0B3InnT4Q76sTk1naiPiVqnTrOVi5ZyjeXxCnweSKXY0+BMQ/hfQVz72UXCdZTuVjvxkJCslyL0JtIIX0FFfugUS1uoVPQAju0oNy4BeUVtKA6++0WhLdy5aao/Gpx+R+wNf9CAyPbUb3cH1zr4N7ZW7Bde0sqZTXTZKp2ClVD0qquEGOwpXukaxYOUxuzR4ap0OXlZYIxVsAqONVIpjPPcQlDT8KyFk9OoGpcXWJZQ9svmxin8uTyGQbWnIGsaPo5Ts8wXDqFrAJUza/BtN24xECm598WK+OLPiDYEh035gFtG62Btg/7RiOGtolWQ1tG28ExLbQDtA20JtoKjjlXO/+//ht/oBzHNFDvjl/ln/jfHB+WHNIBiTvpSn/JBehcd70cu/7+GQ4aEkgxCtb+jE/ckbvhk5DY8YGXjKTYCnOkkJDyRWlpQYZ9KAW9p5X03cKQgu706VgqFSpINZb+NFPTOxci3Qt+DKRQfHikUOjDyZB45r4v31NkycN5CiQOwlQmd5V5mSFPl8gXPLPa8vA6PkpkQ/B2GGym+fNV8I2/CtQ2ad9N/79bOfgPl/4XcnMIZnGB6AD9QncS0SJ+RGIS0SzP6YkqNi8pQAtUBWhWWADltQVgTl6AHVEYlTUrMqqqrM6opXJSo5ZKqo1DQv7ChbdAXSbD0ic=",
            "config": {"visit_all": True},
        },
        {
            "url": "https://puzz.link/p?tapaloop/17/17/g2h3h2yarhajh2x4h2haiyaihaih3xabhajh+2lyaihaih2w3h3h2y3haihabx2hajhaiyajhaihajx2hajhajy2h2h3g",
            "test": False,
        },
    ]
    parameters = {"visit_all": {"name": "Visit all cells", "type": "checkbox", "default": False}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black"))
        self.add_program_line(grid(puzzle.row, puzzle.col))

        if puzzle.param["visit_all"]:
            self.add_program_line("tapaloop(R, C) :- grid(R, C), not black(R, C).")
        else:
            self.add_program_line("{ tapaloop(R, C) } :- grid(R, C), not black(R, C).")

        self.add_program_line(direction("lurd"))
        self.add_program_line(fill_path(color="tapaloop"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="tapaloop", adj_type="loop"))
        self.add_program_line(single_loop(color="tapaloop"))
        self.add_program_line(direction_to_binary(puzzle.row, puzzle.col))
        self.add_program_line(tapaloop_pattern_rule())

        clue_dict: Dict[Tuple[int, int], List[Union[int, str]]] = {}
        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            fail_false(isinstance(label, str) and label.startswith("tapa"), f"Clue at {r, c} should be set to 'Tapa' sub.")

            if (r, c) not in clue_dict:
                self.add_program_line(f"black({r}, {c}).")
                self.add_program_line(valid_tapaloop(r, c))
                clue_dict.setdefault((r, c), [])

            clue_dict[(r, c)].append(clue)

        for (r, c), clue in clue_dict.items():
            self.add_program_line(parse_clue(r, c, clue))

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_direction", size=3))

        return self.program
