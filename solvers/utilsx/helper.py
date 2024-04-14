"""Helper functions for generation solvers and rules."""

from typing import Any, Dict, Tuple


def tag_encode(name: str, *data: Any) -> str:
    """Encode a valid tag predicate without spaces or hyphens."""
    tag_data = [name]
    for d in data:  # recommended data sequence: *_type, src_r, src_c, color
        if d is not None:
            tag_data.append(str(d).replace("-", "_").replace(" ", "_"))

    return "_".join(tag_data)


def mark_and_extract_clues(
    original_clues: Dict[Tuple[int, int], Any],
    shaded_color: str = "black",
    safe_color: str = "green",
) -> Tuple[Dict[Tuple[int, int], int], str]:
    """
    Mark clues to the solver and extract the clues that are not color-relevant.

    Recommended to use it before performing a bfs on a grid.
    """
    clues = {}  # remove color-relevant clues here
    rule = ""
    for (r, c), clue in original_clues.items():
        if isinstance(clue, list):
            if clue[1] == shaded_color:
                rule += f"{shaded_color}({r}, {c}).\n"
            elif clue[1] == safe_color:
                rule += f"not {shaded_color}({r}, {c}).\n"
            clues[(r, c)] = int(clue[0])
        elif clue == shaded_color:
            rule += f"{shaded_color}({r}, {c}).\n"
        elif clue == safe_color:
            rule += f"not {shaded_color}({r}, {c}).\n"
        else:
            clues[(r, c)] = int(clue)
    return clues, rule.strip()
