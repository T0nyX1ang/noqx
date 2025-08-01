"""Manager of all the solvers as a plugin."""

from typing import Any, Dict, List

from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.puzzle.penpa import PenpaPuzzle

modules: Dict[str, "Solver"] = {}


def load_solver(solver_dir: str, solver_name: str):
    "Load a solver from a valid directory."
    if solver_name in modules:
        raise ValueError(f"Solver for {solver_name} already exists.")

    module = __import__(f"{solver_dir}.{solver_name}")
    module_attr = getattr(module, solver_name)

    for attr_name in dir(module_attr):
        attr = getattr(module_attr, attr_name)

        if isinstance(attr, type) and issubclass(attr, Solver) and attr is not Solver:
            puzzle_name = solver_name.lower()
            modules[puzzle_name] = attr()


def list_solver_metadata() -> Dict[str, Any]:
    """List all available solver metadata."""
    metadata = {}
    for puzzle_name, module in modules.items():
        metadata[puzzle_name] = {
            "name": module.name,
            "category": module.category,
            "aliases": module.aliases,
            "examples": module.examples,
            "parameters": module.parameters,
        }

    return metadata


def prepare_puzzle(puzzle_name: str, puzzle_content: str, param: Dict[str, Any]) -> Puzzle:
    """Prepare the puzzle."""
    puzzle = PenpaPuzzle(puzzle_name, puzzle_content, param)
    puzzle.decode()

    return puzzle


def generate_program(puzzle: Puzzle) -> str:
    """Generate the solver program."""
    module = modules[puzzle.puzzle_name]
    return module.solve(puzzle)


def store_solution(puzzle: Puzzle, model_str: str) -> Puzzle:
    """Store and refine the solution."""
    module = modules[puzzle.puzzle_name]

    solution_data = tuple(str(model_str).split())  # raw solution converted from clingo
    solution = PenpaPuzzle(puzzle.puzzle_name, puzzle.content, puzzle.param)
    solution.decode()
    solution.clear()

    for item in solution_data:
        _type, _data = item.replace("(", " ").replace(")", " ").split()
        data = _data.split(",")

        r, c = tuple(map(int, data[:2]))  # ensure the first two elements of data is the row and column

        if _type.startswith("edge_"):
            for d in [Direction.TOP, Direction.LEFT, Direction.TOP_LEFT, Direction.DIAG_UP, Direction.DIAG_DOWN]:
                if _type == f"edge_{d}":
                    solution.edge[Point(r, c, d)] = True

        elif _type.startswith("grid_"):
            grid_direction = str(data[2]).replace('"', "")
            if puzzle.puzzle_name == "hashi":
                solution.line[Point(r, c, label=f"{grid_direction}_{data[3]}")] = True
            else:
                solution.line[Point(r, c, label=grid_direction)] = True

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

    module.refine(solution)
    return solution


class Solver:
    """Base class to create solvers."""

    def __init__(self):
        """Initialize a program."""
        self._program: List[str] = []

    def add_program_line(self, line: str):
        """Add a line to the program."""
        if line != "":
            self._program.append(line.strip())

    @property
    def program(self) -> str:
        """Get the program as a string."""
        return "\n".join(self._program)

    def reset(self):
        """Clear the program."""
        self._program.clear()

    def solve(self, _: Puzzle) -> str:
        """Generate the solver program."""
        raise NotImplementedError("Solver program not implemented.")

    def refine(self, solution: Puzzle) -> Puzzle:
        """Refine the solution."""
        return solution

    name: str = "Unknown"
    category: str = "unk"
    aliases: List[str] = []
    examples: List[Dict[str, Any]] = []
    parameters: Dict[str, Any] = {}
