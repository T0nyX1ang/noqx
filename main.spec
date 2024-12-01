# -*- mode: python ; coding: utf-8 -*-

import os

hiddle_imports = ["main", "_cffi_backend"]

for file in os.listdir("solver"):
    if file.endswith(".py") and file != "__init__.py":
        hiddle_imports.append(f"solver.{file[:-3]}")


block_cipher = None


a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[("./static/*", "./static"), ("./LICENSE.GPL", "./")],
    hiddenimports=hiddle_imports,
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
    name='main',
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
    name='noqx',
)
