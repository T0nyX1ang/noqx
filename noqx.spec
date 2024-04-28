# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ["noqx.py"],
    pathex=[],
    binaries=[],
    datas=[
      ("./static/noq/*", "./static/noq"),
      ("./static/style.css", "./static"),
      ("./templates/*", "./templates"),
      ("./LICENSE", "./")
    ],
    hiddenimports=[
        "noqx",
        "solver.aqre",
        "solver.aquarium",
        "solver.balance",
        "solver.battleship",
        "solver.binairo",
        "solver.canal",
        "solver.castle",
        "solver.cave",
        "solver.chocona",
        "solver.country",
        "solver.doppelblock",
        "solver.easyas",
        "solver.fillomino",
        "solver.gokigen",
        "solver.haisu",
        "solver.hashi",
        "solver.heteromino",
        "solver.heyawake",
        "solver.hitori",
        "solver.hotaru",
        "solver.kakuro",
        "solver.kurodoko",
        "solver.kurotto",
        "solver.lightup",
        "solver.lits",
        "solver.magnets",
        "solver.masyu",
        "solver.mines",
        "solver.moonsun",
        "solver.nagare",
        "solver.nanro",
        "solver.ncells",
        "solver.nonogram",
        "solver.norinori",
        "solver.numlin",
        "solver.nuribou",
        "solver.nurikabe",
        "solver.nurimisaki",
        "solver.onsen",
        "solver.ripple",
        "solver.shakashaka",
        "solver.shikaku",
        "solver.shimaguni",
        "solver.skyscrapers",
        "solver.slither",
        "solver.spiralgalaxies",
        "solver.starbattle",
        "solver.statuepark",
        "solver.stostone",
        "solver.sudoku",
        "solver.tapa",
        "solver.tapaloop",
        "solver.tasquare",
        "solver.tatamibari",
        "solver.tents",
        "solver.yajikazu",
        "solver.yajilin",
        "solver.yinyang",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="noqx",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="noqx",
)
