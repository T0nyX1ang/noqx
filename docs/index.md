# Noqx

[Noqx](https://github.com/T0nyX1ang/noqx) is an extended logic puzzle solver of [Noq](https://github.com/mstang107/noq).

- Try it through this [portal](./penpa-edit/){:target="\_blank"}.

## Guide for First-time Users

### Select a puzzle type

- You can fuzzy search the puzzle type in the first dropdown box.

- If you import the puzzle via a `puzz.link` URL, the puzzle type is automatically set.

- If you want to see the examples, you can select them from the second dropdown box.

- You can view the rules of a puzzle externally if it is indexed in `puzz.link`.

- You can change the parameters of a puzzle if the `Show Parameters` button is available.

- If you change the puzzle type, the whole board will be cleared. Please take care.

### Draw the board

- The operations are identical to the original `Penpa+` version.

- If you draw something on the board, the puzzle type and examples cannot be changed. Reset the board if you want to change them.

### Solve the puzzle

- Click on the `Solve` button to solve the puzzle.

- If the puzzle is **being solved**, the puzzle type and examples cannot be changed. If you use the `backend` version, please wait until the solver times out.
  If you use the `static` version, you can reset the puzzle directly.

- If the puzzle is **solved**, you can click on the original `Solve` button to switch between solutions if the puzzle have multiple solutions.
  Meanwhile, the puzzle type and examples cannot be changed. Reset the board if you want to change them.

### Reset the board

- If you feel sure that the puzzle can be discarded, you can click the `Reset` button to clear the board.

- Although the puzzle is reset, the style and size is cached for convenience.

## New features

### New features from `Noq`

- Acquire enhanced efficiency and more solvers (140+ currently).

- Change the backend from `Django` to `Starlette` with `Uvicorn` (See issues [#31](https://github.com/T0nyX1ang/noqx/issues/31) and [#50](https://github.com/T0nyX1ang/noqx/issues/50)).

- Change the frontend to `Penpa+`. (See issue [#36](https://github.com/T0nyX1ang/noqx/issues/36)).

- Obtain uniform data structures in every puzzle. (See issues [#84](https://github.com/T0nyX1ang/noqx/issues/84) and [#109](https://github.com/T0nyX1ang/noqx/issues/109)).

- Deploy the entire solver to GitHub Pages with the help of `PyScript`. No backend server is needed in this mode.

### New usages from `Penpa+`

- Select puzzle type.

- Show rules in [puzz.link](https://puzz.link/list.html) if possible.

- Choose example puzzle.

- Show/Edit parameters of the solver if possible.

- Solve/Reset the puzzle.

## How to contribute

- Make sure the Microsoft Visual C++ Redistributable (v14, 2015-2022) is installed on Windows.

- The `requirements.txt` file is for dependency checking only, and it is very discouraged to use `PIP` in this project.

### Preparations

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first.

- Clone this project and switch to `dev` branch.

```bash
    git clone https://github.com/T0nyX1ang/noqx.git
    git checkout dev
```

- Install all dependencies with `uv`:

```bash
    uv sync --all-extras
```

- Install [pre-commit](https://pre-commit.com/) and add commit hooks:

```bash
    uv pre-commit install
```

### Program Parameters

```text
  usage: uv run main.py [-h] [-H HOST] [-p PORT] [-d] [-tl TIME_LIMIT] [-pt PARALLEL_THREADS] [-B] [-D]

  options:
    -h, --help            show this help message and exit
    -H HOST, --host HOST  the host to run the server on.
    -p PORT, --port PORT  the port to run the server on.
    -d, --debug           whether to enable debug mode with auto-reloading.
    -tl TIME_LIMIT, --time-limit TIME_LIMIT
                          time limit in seconds.
    -pt PARALLEL_THREADS, --parallel-threads PARALLEL_THREADS
                          parallel threads.
    -B, --build-document  build the documentation site.
    -D, --enable-deployment
                          enable deployment for client-side purposes.
```

### Write a new solver

- Create a python file in the `solver` folder and write solver codes in that file. The functions in the `noqx` package are free to use.

- Create a class inheriting the base class `noqx.manager.Solver`. It is recommended to read the [Solver Manager](./noqx/manager.md) section for further reference.

- (Optional) Set the metadata of the solver. It is recommended to read the [Solver Manager](./noqx/manager.md) section for further reference.

- Implement a `solve` function and write the ASP program needed. The data structures are detailed in the `Puzzle Encodings` section, especially in the `noqx.puzzle.Puzzle` class. The useful rules are detailed in the `Useful Rules` section.

- (Optional) Implement a `refine` function if extra refinement is needed after program solving. It is recommended to read the document of the `noqx.manager.store_solution` API for further reference.

- Test the solver manually by running `main.py` with the specified solver and puzzle.

### Test solvers

- Run the tests (with default `unittest` features) with `uv`:

```bash
    uv run coverage run -m unittest
```

- Check the HTML version of coverage report with `uv`:

```bash
    uv run coverage html
```
