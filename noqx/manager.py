"""Manager of all the solvers as a plugin."""

import importlib
import pkgutil
from copy import deepcopy
from types import ModuleType
from typing import Any, Dict, List

from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.puzzle.penpa import PenpaPuzzle

modules: Dict[str, ModuleType] = {}


def load_solvers(solver_dir: str):
    """Load the solvers from a valid directory."""
    puzzle_names: List[str] = []
    for module_info in pkgutil.iter_modules([solver_dir]):
        puzzle_names.append(module_info.name)

    for pt in sorted(puzzle_names):
        modules[pt] = importlib.import_module(f"{solver_dir}.{pt}")


def list_solver_metadata() -> Dict[str, Any]:
    """List all available solver metadata."""
    metadata = {}
    for puzzle_name, module in modules.items():
        if hasattr(module, "__metadata__"):
            metadata[puzzle_name] = module.__metadata__
        else:
            metadata[puzzle_name] = {
                "name": puzzle_name.capitalize().replace("_", " "),
                "category": "unk",
                "aliases": [],
                "examples": [],
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
    if not hasattr(module, "program"):
        raise NotImplementedError("Solver program not implemented.")

    return module.program(puzzle)


def store_solution(puzzle: Puzzle, model_str: str) -> Puzzle:
    """Store and refine the solution."""
    module = modules[puzzle.puzzle_name]

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

    if hasattr(module, "refine"):  # refine the solution if possible
        module.refine(solution)

    return solution
