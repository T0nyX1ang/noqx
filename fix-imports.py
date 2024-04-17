"""This file fixes the hidden imports for pyinstaller."""

import os

print("import noqx")

for files in os.listdir("solvers"):
    if files.endswith(".py") and not files.startswith("__"):
        print(f"import solvers.{files[:-3]}")
