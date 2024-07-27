"""Constant definitions for the site."""

from typing import Dict, List, Union

CATEGORIES: Dict[str, str] = {
    "shade": "Shading",
    "loop": "Loop / Path",
    "region": "Region division",
    "num": "Number",
    "var": "Variety",
    "draw": "Drawing",
}


PUZZLE_TYPES: Dict[str, Dict[str, Union[str, List[str]]]] = {
    "aqre": {
        "name": "Aqre",
        "cat": "shade",
        "aliases": [],
        "examples": [
            "m=edit&p=7ZTRT5xMFMXf968w8zwPywyMypta7Yvftn7aGEPIhl1RibBjZ9lq2Oz/7rnDrMBC07RNUx8aws2PwzD3wHBm+XWVmJQrHPKAj7mHQyhlT8/37Tl2x1VW5mm4x49W5YM2AM4/nZ3xuyRfpqPIjYpH6+owrC549TGMmMc4Ezg9FvPqIlxX/4XVhFeXuMW4B+28HiSApw1e2/tEJ7XojcETx8AboH6ZHtdXn8OouuKMehzbJwlZob+lzHmg67kuZhkJs6TEiywfsid3Z7m61Y8rN9aLN7w6qq1eDliVjVXC2irRgFV6A7I6z8w8T6fnf8DuYbzZ4JP/D8PTMCLvXxo8aPAyXKNOwjUTgh7Fqnj1ujCxT8JhI8iAhIOtgOc8+/SNrWe2CluvMDmvpK0fbB3bGth6bsecoqfn4XcSioUCM4qgxfjFBNpZlmDfsQDLhiVME0uw79gHB44DsHKs8BO/MXop10uhl3K9FHop10vRs9te8CndeEkRcOyDA8cBeDsn+ZduHok52+y7OX1w4Jh8blnC21svsO+8+eDAcYD522w946Ne2097Yqtvq7KffJ9W+6f+h99f3R/aiWgF3w683a9yPIrY6e19ujfRpkhy5GGyKmap2V5j82FLnU+XK3OXzBEnuzchMdAWdmRHyrV+yrNFd1x2v9AmHbxFYor2A+Nn2tzuzP6c5HlHqPfajlRvDB2pNEh96zoxRj93lCIpHzpCa4fozJQuyq6BMulaTB6TnW5F886bEXth9owkdnb5b2f/Czs7ff7xe8vze7Nj/1xtBmMPeSD5UAcT7vReyKH34kwN+4mGOhBqqLu5htSPNsReuqF9J+A0627GydVuzKlVL+nUqh32KB69Ag=="
        ],
    },
    "aquarium": {"name": "Aquarium", "cat": "shade", "aliases": [], "examples": []},
    "balance": {"name": "Balance Loop", "cat": "loop", "aliases": ["balanceloop"], "examples": []},
    "battleship": {"name": "Battleship", "cat": "var", "aliases": [], "examples": []},
    "binairo": {"name": "Binairo", "cat": "shade", "aliases": [], "examples": []},
    "box": {"name": "Box", "cat": "shade", "aliases": [], "examples": []},
    "canal": {"name": "Canal View", "cat": "shade", "aliases": ["canalview"], "examples": []},
    "castle": {"name": "Castle Wall", "cat": "loop", "aliases": ["castlewall"], "examples": []},
    "cave": {"name": "Cave (Corral)", "cat": "shade", "aliases": [], "examples": []},
    "chocona": {"name": "Chocona", "cat": "shade", "aliases": [], "examples": []},
    "country": {"name": "Country Road", "cat": "loop", "aliases": ["countryroad"], "examples": []},
    "doppelblock": {"name": "Doppelblock", "cat": "num", "aliases": [], "examples": []},
    "easyas": {"name": "Easy As", "cat": "num", "aliases": [], "examples": []},
    "fillomino": {"name": "Fillomino", "cat": "num", "aliases": [], "examples": []},
    "gokigen": {"name": "Gokigen (Slant)", "cat": "draw", "aliases": [], "examples": []},
    "haisu": {"name": "Haisu", "cat": "loop", "aliases": [], "examples": []},
    "hashi": {"name": "Hashiwokakero (Bridges)", "cat": "loop", "aliases": ["bridges"], "examples": []},
    "heteromino": {"name": "Heteromino", "cat": "region", "aliases": [], "examples": []},
    "heyawake": {"name": "Heyawake", "cat": "shade", "aliases": [], "examples": []},
    "hitori": {"name": "Hitori", "cat": "shade", "aliases": [], "examples": []},
    "hotaru": {"name": "Hotaru Beam", "cat": "loop", "aliases": [], "examples": []},
    "jousan": {"name": "Jousan", "cat": "draw", "aliases": [], "examples": []},
    "kakuro": {"name": "Kakuro", "cat": "num", "aliases": [], "examples": []},
    "kurotto": {"name": "Kurotto", "cat": "shade", "aliases": [], "examples": []},
    "kurodoko": {"name": "Kurodoko", "cat": "shade", "aliases": [], "examples": []},
    "lits": {"name": "LITS", "cat": "shade", "aliases": [], "examples": []},
    "lightup": {"name": "Light Up (Akari)", "cat": "var", "aliases": ["akari"], "examples": []},
    "magnets": {"name": "Magnets", "cat": "var", "aliases": [], "examples": []},
    "masyu": {"name": "Masyu", "cat": "loop", "aliases": [], "examples": []},
    "mines": {"name": "Minesweeper", "cat": "var", "aliases": ["minesweeper"], "examples": []},
    "moonsun": {"name": "Moon-or-Sun", "cat": "loop", "aliases": [], "examples": []},
    "nagare": {"name": "Nagareru-Loop", "cat": "loop", "aliases": ["nagareru"], "examples": []},
    "nanro": {"name": "Nanro", "cat": "num", "aliases": [], "examples": []},
    "ncells": {"name": "N Cells", "cat": "region", "aliases": ["fivecells", "fourcells"], "examples": []},
    "nonogram": {"name": "Nonogram", "cat": "shade", "aliases": [], "examples": []},
    "norinori": {"name": "Norinori", "cat": "shade", "aliases": [], "examples": []},
    "numlin": {"name": "Numberlink", "cat": "loop", "aliases": ["numberlink"], "examples": []},
    "nuribou": {"name": "Nuribou", "cat": "shade", "aliases": [], "examples": []},
    "nurikabe": {"name": "Nurikabe", "cat": "shade", "aliases": [], "examples": []},
    "nurimisaki": {"name": "Nurimisaki", "cat": "shade", "aliases": [], "examples": []},
    "onsen": {"name": "Onsen-Meguri", "cat": "loop", "aliases": [], "examples": []},
    "ripple": {"name": "Ripple Effect", "cat": "num", "aliases": ["rippleeffect"], "examples": []},
    "shakashaka": {"name": "Shakashaka", "cat": "var", "aliases": [], "examples": []},
    "shikaku": {"name": "Shikaku", "cat": "region", "aliases": [], "examples": []},
    "shimaguni": {"name": "Shimaguni (Islands)", "cat": "shade", "aliases": ["islands"], "examples": []},
    "simpleloop": {"name": "Simple Loop", "cat": "loop", "aliases": [], "examples": []},
    "skyscrapers": {"name": "Skyscrapers", "cat": "num", "aliases": [], "examples": []},
    "slither": {"name": "Slitherlink", "cat": "loop", "aliases": ["slitherlink"], "examples": []},
    "spiralgalaxies": {"name": "Spiral Galaxies", "cat": "region", "aliases": [], "examples": []},
    "starbattle": {"name": "Star Battle", "cat": "var", "aliases": [], "examples": []},
    "statuepark": {"name": "Statue Park", "cat": "var", "aliases": [], "examples": []},
    "stostone": {"name": "Stostone", "cat": "shade", "aliases": [], "examples": []},
    "sudoku": {"name": "Sudoku", "cat": "num", "aliases": [], "examples": []},
    "tapa": {"name": "Tapa", "cat": "shade", "aliases": [], "examples": []},
    "tasquare": {"name": "Tasquare", "cat": "shade", "aliases": [], "examples": []},
    "tatamibari": {"name": "Tatamibari", "cat": "region", "aliases": [], "examples": []},
    "tents": {"name": "Tents", "cat": "var", "aliases": [], "examples": []},
    "tapaloop": {
        "name": "Tapa-Like Loop",
        "cat": "loop",
        "aliases": ["tapalikeloop", "tapa-like-loop", "tapalike", "tapa-like"],
        "examples": [],
    },
    "yajilin": {"name": "Yajilin", "cat": "loop", "aliases": [], "examples": []},
    "yajikazu": {"name": "Yajisan-Kazusan", "cat": "shade", "aliases": ["yk", "yajisan-kazusan"], "examples": []},
    "yinyang": {"name": "Yin-Yang", "cat": "shade", "aliases": [], "examples": []},
}

# pylint: skip-file
