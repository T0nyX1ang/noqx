"""The Tapa-like Loop solver."""

from typing import Dict, List, Set, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route

direc = ((-1, -1, Direction.RIGHT), (-1, 0, Direction.RIGHT), (-1, 1, Direction.BOTTOM), (0, 1, Direction.BOTTOM), (1, 1, Direction.LEFT), (1, 0, Direction.LEFT), (1, -1, Direction.TOP), (0, -1, Direction.TOP))  # fmt: skip
direc_outer = ((-1, -1, Direction.LEFT), (-1, 1, Direction.TOP), (1, 1, Direction.RIGHT), (1, -1, Direction.BOTTOM))
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
    constraint += "binary(R, C, D, 0) :- grid(R, C), direction(D), not line_io(R, C, D).\n"
    constraint += "binary(R, C, D, 1) :- grid(R, C), line_io(R, C, D)."
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
    category = "route"
    aliases = ["tapalikeloop", "tapa-like-loop", "tapalike", "tapa-like", "tll"]
    examples = [
        {
            "data": "m=edit&p=7VVNT8JAEL33V5A9z6HbLaXtxSCKlwp+YIxpCClYY2OxWKgxS/jvzk6rLNCDRkI0McsOr292u/N2mGH+UkR5DNxUH+ECfuOwuUvTch2aZjUGySKN/Qa0i8VjliMA6He78BCl8xiMsFo2NJbS82Ub5JkfMosBTc6GIC/9pTz3ZQ/kNboYcOQCRJyBhfB0DW/Jr1CnJLmJuIfYLrfdIZwk+SSNR0HJXPihHABT5xzTbgXZNHuNWfkKep5k03GiiHG0QDXzx2RWeebFffZUVGu52lqki2SSpVnOqmhXINulhKBGglhLEJ8SRL0Eax8S0uQ5zt7qwvfqw19haq5QwMgPlZabNXTX8NpfrlScSyZMVmaQA8aMrxTeFuFwIrjGWIo5OtIYscPYFCbXqBZRQme8bcZ16TCN4SadJjSGO3SaxlikwtYZilo/npdSN5jmdtjcrqGcXaq1S7nbb3eaGzeJF87p2u/IdslaZAeYFZCC7AlZk2yTbEBrTsneku2Qtck6tKal8vqtzP8kHMw3JsVz8deCnQRlCkKKFF8MNRRlH9oczb/HDY2QBVikjV6WT6MUK7VXTMdx/vGMrXJlsDdGMxSq9f53z1/cPVWazINV0n4KO8TbrkoRZB/YrBhFIxTG8J8aPpxYnfVOLOYdx8EFYkcYGu8=",
        },
        {
            "data": "m=edit&p=7VVNb5tAEL3zK6I9z2E/MXCx3DTuhThp4iiKkBXZLlVQcWixqaK1/N8zO5BAAz1UqiqripZ9erydmZ1h0O72R7UsUxC+e1QAHAQOX/s0TRDS5M2YZ7s8jU5gUu0eihIJwMV0Cl+X+TYFL2nMFt7ehpGdgP0UJUwyoCnYAuznaG/PIzsDe41LDARqMTLBQCI9a+ktrTt2WouCI58h17XbHdJ1Vq7z9D6ulcsosXNgbp8P5O0o2xQ/U1aHoPd1sVllTlgtd1jN9iH73qxsqy/Ft6qxFc61ynfZusiLkjXZHsBO6hLigRJUW4J6LUENlyD/Rgl59pgWT0Pph8PpH7A1V1jAfZS4Wm5aGrT0OtofXJ575hvnqZXLHTBrDBoKJyklW0nwgMx0R5LaSePxuKMpNaD55Cq74fSItpCiKxpeO3ek0LzdVvKXbTt2Lk4vnpTBgKiG3Eeyl7YcmbfZyGBACvt7KG564ZTofy1lxK/xsCWCGnNHOCWUhHPsG1hF+JGQExrCmGzOCG8JTwk1oU82I9f5P/o3/kE6iZZ0Gv1+mPf1/3l94SUsxiPuZFaUm2WO59ys2qzS8uUdL5qDx54YzUShi36/e4747nFt4sd2yhxbOnjuLbxn",
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
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))

        if puzzle.param["visit_all"]:
            self.add_program_line("white(R, C) :- grid(R, C).")
        else:
            self.add_program_line(shade_c(color="white"))

        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(direction_to_binary(puzzle.row, puzzle.col))
        self.add_program_line(tapaloop_pattern_rule())

        clue_dict: Dict[Tuple[int, int], List[Union[int, str]]] = {}
        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            fail_false(isinstance(label, str) and label.startswith("tapa"), f"Clue at {r, c} should be set to 'Tapa' sub.")

            if (r, c) not in clue_dict:
                self.add_program_line(f"hole({r}, {c}).")
                self.add_program_line(valid_tapaloop(r, c))
                clue_dict.setdefault((r, c), [])

            clue_dict[(r, c)].append(clue)

        for (r, c), clue in clue_dict.items():
            self.add_program_line(parse_clue(r, c, clue))

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
