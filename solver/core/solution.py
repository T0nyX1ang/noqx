"""Generate solutions for the given problem."""

from typing import List, Optional

from clingo.control import Control
from clingo.solving import Model

from .penpa import Direction, Puzzle, Solution

MAX_SOLUTIONS_TO_FIND = 10


def battleship_refine(solution: Solution) -> Solution:
    """Refine the battleship solution."""
    for (r, c), _ in solution.symbol.items():
        has_top_neighbor = (r - 1, c) in solution.symbol
        has_left_neighbor = (r, c - 1) in solution.symbol
        has_bottom_neighbor = (r + 1, c) in solution.symbol
        has_right_neighbor = (r, c + 1) in solution.symbol

        fleet_name = solution.symbol[(r, c)].split("__")[0]

        # center part
        if {has_top_neighbor, has_bottom_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
            solution.symbol[(r, c)] = f"{fleet_name}__1__0"

        # middle part
        elif (has_top_neighbor and has_bottom_neighbor) or (has_left_neighbor and has_right_neighbor):
            solution.symbol[(r, c)] = f"{fleet_name}__2__0"

        # left part
        elif {has_top_neighbor, has_bottom_neighbor, has_left_neighbor} == {False}:
            solution.symbol[(r, c)] = f"{fleet_name}__3__0"

        # top part
        elif {has_top_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
            solution.symbol[(r, c)] = f"{fleet_name}__4__0"

        # right part
        elif {has_top_neighbor, has_bottom_neighbor, has_right_neighbor} == {False}:
            solution.symbol[(r, c)] = f"{fleet_name}__5__0"

        # bottom part
        elif {has_bottom_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
            solution.symbol[(r, c)] = f"{fleet_name}__6__0"

    return solution


class ClingoSolver:
    """A solver using clingo."""

    def __init__(self):
        """Initialize a solver."""
        self.clingo_instance: Control = Control()
        self.program: str = ""
        self.puzzle: Optional[Puzzle] = None
        self.solutions: List[str] = []

    def register_puzzle(self, puzzle: Puzzle):
        """Register the puzzle to the solution."""
        self.puzzle = puzzle
        print("[Solver] Puzzle registered.")

    def store_solutions(self, model: Model):
        """Get the solution."""
        if self.puzzle is None:
            raise ValueError("Puzzle not registered.")

        solution_data = tuple(str(model).split())  # raw solution converted from clingo
        solution = Solution(self.puzzle)

        for item in solution_data:
            _type, _data = item.replace("(", " ").replace(")", " ").split()
            data = _data.split(",")
            r, c = data[:2]  # ensure the first two elements of data is the row and column

            if _type.startswith("edge_"):
                if _type == "edge_left":
                    solution.edge.add((int(r), int(c), Direction.LEFT))
                elif _type == "edge_top":
                    solution.edge.add((int(r), int(c), Direction.TOP))
                elif _type == "edge_diag_up":
                    solution.edge.add((int(r), int(c), Direction.DIAG_UP))
                elif _type == "edge_diag_down":
                    solution.edge.add((int(r), int(c), Direction.DIAG_DOWN))

            elif _type.startswith("grid_"):
                grid_direction = str(data[2]).replace('"', "")
                if self.puzzle.puzzle_type == "hashi":
                    solution.line.add((int(r), int(c), f"{grid_direction}_{data[3]}"))
                else:
                    solution.line.add((int(r), int(c), grid_direction))

            elif _type.startswith("number"):
                if self.puzzle.puzzle_type == "easyasabc":  # convert penpa number to letter
                    solution.text[(int(r), int(c))] = self.puzzle.param["letters"][int(data[2]) - 1]
                else:
                    solution.text[(int(r), int(c))] = int(data[2])

            elif _type.startswith("content"):
                solution.text[(int(r), int(c))] = str(data[2]).replace('"', "")

            elif _type == "triangle":
                solution.symbol[(int(r), int(c))] = f"tri__{data[2]}"

            elif _type == "gray":
                solution.surface[(int(r), int(c))] = 8
            elif _type == "black":
                solution.surface[(int(r), int(c))] = 4

            else:
                solution.symbol[(int(r), int(c))] = str(_type)

        if self.puzzle.puzzle_type == "battleship":
            solution = battleship_refine(solution)  # refine the battleship solution

        self.solutions.append(str(solution))

    def add_program_line(self, line: str):
        """Add a line to the program."""
        self.program += line + "\n"

    def reset(self):
        """Reset the program."""
        self.clingo_instance = Control()
        self.program = ""
        self.puzzle = None
        self.solutions = []

    def solve(self):
        """Solve the problem."""
        self.clingo_instance.configuration.sat_prepro = 2
        self.clingo_instance.configuration.asp.trans_ext = "dynamic"  # type: ignore
        self.clingo_instance.configuration.asp.eq = 1  # type: ignore
        self.clingo_instance.configuration.solve.models = MAX_SOLUTIONS_TO_FIND  # type: ignore
        self.clingo_instance.add("base", [], self.program)
        self.clingo_instance.ground()
        self.clingo_instance.solve(on_model=self.store_solutions)


solver = ClingoSolver()
