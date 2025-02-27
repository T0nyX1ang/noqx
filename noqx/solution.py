"""Generate solutions for the given problem."""

from copy import deepcopy

from noqx.puzzle import Color, Direction, Point, Puzzle


class ClingoProgram:
    """A program for clingo."""

    def __init__(self):
        """Initialize a program."""
        self.program: str = ""

    def add_program_line(self, line: str):
        """Add a line to the program."""
        if line != "":
            self.program += line + "\n"

    def reset(self):
        """Clear the program."""
        self.program = ""


def store_solutions(puzzle: Puzzle, model_str: str) -> Puzzle:
    """Get the solution."""
    solution_data = tuple(str(model_str).split())  # raw solution converted from clingo
    solution = deepcopy(puzzle)
    solution.clear()

    for item in solution_data:
        _type, _data = item.replace("(", " ").replace(")", " ").split()
        data = _data.split(",")

        r, c = tuple(map(int, data[:2]))  # ensure the first two elements of data is the row and column

        if _type.startswith("edge_"):
            for d in Direction:
                if _type == f"edge_{d.value}":
                    solution.edge[Point(r, c, d)] = True

        elif _type.startswith("grid_"):
            grid_direction = str(data[2]).replace('"', "")
            if puzzle.puzzle_name == "hashi":
                solution.line[Point(r, c, pos=f"{grid_direction}_{data[3]}")] = True
            else:
                solution.line[Point(r, c, pos=grid_direction)] = True

        elif _type.startswith("number"):
            solution.text[Point(r, c, Direction.CENTER, "normal")] = int(data[2])

        elif _type.startswith("content"):
            solution.text[Point(r, c, Direction.CENTER, "normal")] = str(data[2]).replace('"', "")

        elif _type == "triangle":
            shaka_dict = {'"ul"': "1", '"ur"': "4", '"dl"': "2", '"dr"': "3"}
            solution.symbol[Point(r, c, Direction.CENTER)] = f"tri__{shaka_dict[data[2]]}"

        elif _type == "gray":
            solution.surface[Point(r, c)] = Color.GRAY
        elif _type == "black":
            solution.surface[Point(r, c)] = Color.BLACK

        elif len(data) == 2:
            solution.symbol[Point(r, c, Direction.CENTER)] = str(_type)

        else:  # pragma: no cover
            solution.text[Point(r, c, Direction.CENTER, "normal")] = int(data[2])  # for debugging

    return solution


solver = ClingoProgram()
