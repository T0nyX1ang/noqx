"""Constant definitions for the site."""

from typing import Dict, List, Union

PYTHON_ANYWHERE = False

cats: Dict[str, str] = {
    "shade": "Shading",
    "region": "Region division",
    "loop": "Loop / Path",
    "num": "Number placement",
    "obj": "Object placement",
    "lsq": "Latin square",
}

types: List[Dict[str, Union[str, List]]] = [
    # 'aho',
    # 'amibo',
    {"value": "akari", "name": "Akari (Light Up)", "cat": "obj"},
    {"value": "aqre", "name": "Aqre", "cat": "shade"},
    {"value": "aquarium", "name": "Aquarium", "cat": "shade"},
    {"value": "balanceloop", "name": "Balance Loop", "cat": "loop"},
    {"value": "battleship", "name": "Battleship", "cat": "obj"},
    {"value": "binairo", "name": "Binairo", "cat": "shade"},
    {"value": "castlewall", "name": "Castle Wall", "cat": "loop"},
    {"value": "cave", "name": "Cave (Corral)", "cat": "shade"},
    {"value": "chocona", "name": "Chocona", "cat": "shade"},
    {"value": "countryroad", "name": "Country Road", "cat": "loop"},
    {"value": "doppelblock", "name": "Doppelblock", "cat": "lsq"},
    {"value": "easyas", "name": "Easy As", "cat": "lsq"},
    {"value": "fillomino", "name": "Fillomino", "cat": "num"},
    {
        "value": "gokigen",
        "name": "Gokigen (Slant)",
        "cat": "obj",
    },  # is this the right category??
    {"value": "haisu", "name": "Haisu", "cat": "loop"},
    {"value": "hashi", "name": "Hashi (Bridges)", "cat": "loop"},
    {"value": "heteromino", "name": "Heteromino", "cat": "region"},
    {"value": "heyawake", "name": "Heyawake", "cat": "shade"},
    {"value": "hitori", "name": "Hitori", "cat": "shade"},
    {"value": "hotaru", "name": "Hotaru Beam", "cat": "loop"},
    {"value": "kakuro", "name": "Kakuro", "cat": "num"},
    {"value": "kurotto", "name": "Kurotto", "cat": "shade"},
    {"value": "kuromasu", "name": "Kuromasu", "cat": "shade"},
    {"value": "lits", "name": "LITS", "cat": "shade"},
    {
        "value": "magnets",
        "name": "Magnets",
        "cat": "obj",
    },  # is this the right category??
    {"value": "masyu", "name": "Masyu", "cat": "loop"},
    {"value": "minesweeper", "name": "Minesweeper", "cat": "obj"},
    {"value": "moonsun", "name": "Moon-or-Sun", "cat": "loop"},
    {"value": "nagare", "name": "Nagare", "cat": "loop", "aliases": ["nagareru"]},
    {"value": "nanro", "name": "Nanro", "cat": "num"},
    {
        "value": "ncells",
        "name": "N Cells",
        "cat": "region",
        "aliases": ["fivecells", "fourcells"],
    },
    {"value": "nonogram", "name": "Nonogram", "cat": "shade"},
    {"value": "norinori", "name": "Norinori", "cat": "shade"},
    {"value": "numberlink", "name": "Numberlink", "cat": "loop"},
    {"value": "nuribou", "name": "Nuribou", "cat": "shade"},
    {"value": "nurikabe", "name": "Nurikabe", "cat": "shade"},
    {"value": "nurimisaki", "name": "Nurimisaki", "cat": "shade"},
    {"value": "onsen", "name": "Onsen", "cat": "loop"},
    {"value": "rippleeffect", "name": "Ripple Effect", "cat": "num"},
    {
        "value": "shakashaka",
        "name": "Shakashaka",
        "cat": "shade",
    },  # is this the right category??
    {"value": "shikaku", "name": "Shikaku", "cat": "region"},
    {
        "value": "shimaguni",
        "name": "Shimaguni (Islands)",
        "cat": "shade",
        "aliases": ["islands"],
    },
    {"value": "skyscrapers", "name": "Skyscrapers", "cat": "lsq"},
    {"value": "slitherlink", "name": "Slitherlink", "cat": "loop"},
    {"value": "spiralgalaxies", "name": "Spiral Galaxies", "cat": "region"},
    {"value": "starbattle", "name": "Star Battle", "cat": "obj"},
    {"value": "statuepark", "name": "Statue Park", "cat": "obj"},
    {"value": "stostone", "name": "Stostone", "cat": "shade"},
    {"value": "sudoku", "name": "Sudoku", "cat": "lsq"},
    {"value": "tapa", "name": "Tapa", "cat": "shade"},
    {"value": "tatamibari", "name": "Tatamibari", "cat": "region"},
    {"value": "tents", "name": "Tents", "cat": "obj"},
    {
        "value": "tll",
        "name": "Tapa-Like Loop",
        "cat": "loop",
        "aliases": ["tapalikeloop", "tapa-like-loop", "tapalike", "tapa-like"],
    },
    {"value": "yajilin", "name": "Yajilin", "cat": "loop"},
    {
        "value": "yajisankazusan",
        "name": "Yajisan-Kazusan",
        "cat": "shade",
        "aliases": ["yk", "yajisan-kazusan", "yajikazu"],
    },
    {"value": "yinyang", "name": "Yin-Yang", "cat": "shade"},
]
