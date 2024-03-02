"""Helper functions for generation solvers and rules."""

import itertools
from typing import Any, Dict, List, Set, Tuple

from .solution import ClingoSolver


def tag_encode(name: str, *data: Any) -> str:
    """Encode a valid tag predicate without spaces or hyphens."""
    tag_data = [name]
    for d in data:  # recommended data sequence: *_type, src_r, src_c, color
        tag_data.append(str(d).replace("-", "_").replace(" ", "_"))

    return "_".join(tag_data)


def canonicalize_shape(shape: Tuple[Tuple[int, int]]) -> Tuple[Tuple[int, int]]:
    """
    Given a (possibly non-canonical) shape representation,

    Return the canonical representation of the shape, a tuple:
        - in sorted order
        - whose first element is (0, 0)
        - whose other elements represent the offsets of the other cells from the first one
    """
    shape = sorted(shape)
    root_r, root_c = shape[0]
    dr, dc = -1 * root_r, -1 * root_c
    return tuple((r + dr, c + dc) for r, c in shape)


def get_variants(shape: Tuple[Tuple[int, int]], allow_rotations: bool, allow_reflections: bool) -> Set[Tuple[Tuple[int, int]]]:
    """
    Get a set of canonical shape representations for a (possibly non-canonical) shape representation.

    allow_rotations = True iff shapes can be rotated
    allow_reflections = True iff shapes can be reflected
    """
    # build a set of functions that transform shapes
    # in the desired ways
    functions = set()
    if allow_rotations:
        functions.add(lambda shape: canonicalize_shape((-c, r) for r, c in shape))
    if allow_reflections:
        functions.add(lambda shape: canonicalize_shape((-r, c) for r, c in shape))

    # make a set of currently found shapes
    result = set()
    result.add(canonicalize_shape(shape))

    # apply our functions to the items in this set
    all_shapes_covered = False
    while not all_shapes_covered:
        new_shapes = set()
        current_num_shapes = len(result)
        for f, s in itertools.product(functions, result):
            new_shapes.add(f(s))
        result = result.union(new_shapes)
        all_shapes_covered = current_num_shapes == len(result)
    return result


def mark_and_extract_clues(
    solver: ClingoSolver,
    original_clues: Dict[Tuple[int, int], Any],
    shaded_color: str = "black",
    safe_color: str = "green",
) -> Dict[Tuple[int, int], int]:
    """
    Mark clues to the solver and extract the clues that are not color-relevant.

    Recommended to use it before performing a bfs on a grid.
    """
    clues = {}  # remove color-relevant clues here
    for (r, c), clue in original_clues.items():
        if isinstance(clue, list):
            if clue[1] == shaded_color:
                solver.add_program_line(f"{shaded_color}({r}, {c}).")
            elif clue[1] == safe_color:
                solver.add_program_line(f"not {shaded_color}({r}, {c}).")
            clues[(r, c)] = int(clue[0])
        elif clue == shaded_color:
            solver.add_program_line(f"{shaded_color}({r}, {c}).")
        elif clue == safe_color:
            solver.add_program_line(f"not {shaded_color}({r}, {c}).")
        else:
            clues[(r, c)] = int(clue)
    return clues


class ConnectivityHelper:
    """A helper class to generate connectivity rules."""

    def __init__(self, name: str, bound_type: str = "grid", color: str = "black", adj_type: int = 4):
        """
        Initialize the connectivity generator.

        Parameter [name]: the name of the generator.
        Parameter [bound_type, color]:
            + 'grid', then the initial {color} cells are bounded in the grid.
            + 'area', then the initial {color} cells are bounded in a certain area.
        Parameter [adj_type]: the type of adjacency, must be one of '4', '8'.
        """
        if bound_type not in ("grid", "area"):
            raise ValueError("Invalid bound type, must be one of 'grid', 'area'.")

        self.name = name
        self.adj_type = adj_type
        self.bound_type = bound_type
        self.color = color
        if self.color is not None:
            self.tag = tag_encode(name, "adj", adj_type, color)
        else:
            self.tag = tag_encode(name, "adj", adj_type)

    def initial(
        self,
        src_cells: List[Tuple[int, int]] = None,
        exclude_cells: List[Tuple[int, int]] = None,
        full_search: bool = False,
        enforce_color: bool = False,
    ) -> str:
        """Generate the initial rule."""
        if self.bound_type == "area":  # judge for area bound type first
            area_min = f"(R, C) = #min{{ (R1, C1): area(A, R1, C1), {self.color}(R1, C1) }}"
            return f"{self.tag}(A, R, C) :- area(A, _, _), {area_min}."

        if src_cells is None:  # use the default initial rule if no source cells are given
            if not full_search:
                return f"{self.tag}(R, C) :- (R, C) = #min{{ (R1, C1): grid(R1, C1), {self.color}(R1, C1) }}."
            return f"{self.tag}(R, C, R, C) :- grid(R, C), {self.color}(R, C)."

        # generate the initial rule from the source cells
        initial = ""
        for r, c in src_cells:
            color_constraint = f" :- {self.color}({r}, {c})" if enforce_color else ""
            if not full_search:
                initial += f"{self.tag}({r}, {c}){color_constraint}.\n"
            else:
                initial += f"{self.tag}({r}, {c}, {r}, {c}){color_constraint}.\n"
                for exclude_r, exclude_c in exclude_cells:
                    initial += f"not {self.tag}({r}, {c}, {exclude_r}, {exclude_c}).\n"
        return initial.strip()

    def propagation(self, full_search: bool = False, extra_constraint: str = "") -> str:
        """Generate the propagation rule."""
        mutual = f"{self.color}(R, C), adj_{self.adj_type}(R, C, R1, C1)"
        if extra_constraint:
            mutual += f", {extra_constraint}"

        if self.bound_type == "area":
            return f"{self.tag}(A, R, C) :- {self.tag}(A, R1, C1), area(A, R, C), {mutual}."

        if not full_search:
            return f"{self.tag}(R, C) :- {self.tag}(R1, C1), grid(R, C), {mutual}."

        return f"{self.tag}(R0, C0, R, C) :- {self.tag}(R0, C0, R1, C1), grid(R, C), {mutual}."

    def constraint(self, full_search: bool = False) -> str:
        """Generate the constraint rule."""
        if self.bound_type == "area":
            return f":- area(A, R, C), {self.color}(R, C), not {self.tag}(A, R, C)."

        if not full_search:
            return f":- grid(R, C), {self.color}(R, C), not {self.tag}(R, C)."

        return f":- grid(R, C), {self.color}(R, C), not {self.tag}(_, _, R, C)."

    def get_tag(self) -> str:
        """Return the tag of the generator."""
        return self.tag
