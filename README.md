# Noqx

Extended logic puzzle solver of [Noq](https://github.com/mstang107/noq).

## Current Maintainers

- [@T0nyX1ang](https://github.com/T0nyX1ang): backend, frontend, new solver implementations, bug fixes

- [@zhuyaoyu](https://github.com/zhuyaoyu): (huge) solver optimizations, new solver implementations, bug fixes

## New features

### New features from Noq

- Remove redundant codes and formatting codes.

- New solver backend with new UI design (See issue [#2](https://github.com/T0nyX1ang/noqx/issues/2))

- Change the backend from Django to Starlette with Uvicorn (See issue [#31](https://github.com/T0nyX1ang/noqx/issues/31), [#50](https://github.com/T0nyX1ang/noqx/issues/50)).

- Change the frontend from Noq native to penpa-edit. (See issue [#36](https://github.com/T0nyX1ang/noqx/issues/36)).

- Obtain uniform data structures in every puzzle. (See issue [#88](https://github.com/T0nyX1ang/noqx/issues/84)).

- Deploy the entire solver to Github Pages with the help of `PyScript`.

### New usages from Penpa-edit

- Select puzzle type.

- Show rules in [puzz.link](https://puzz.link/list.html) if possible.

- Choose example puzzle.

- Show/Edit parameters of the solver if possible.

- Solve/Reset the puzzle.

**Note**: if the puzzle is imported from [puzz.link](https://puzz.link/list.html), you will need to change the edit mode to `Problem` to reset the puzzle itself.

## How to run locally

### Use uv with a virtual environment (Recommended)

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first.

- Clone this project and switch to `master` branch.

```bash
    git clone https://github.com/T0nyX1ang/noqx.git
```

- Create a virtual environment (Optional):

```bash
    uv venv
```

- Install non-development packages with uv:

```bash
    uv sync --extra web --no-dev
```

- Run with uv:

```bash
    uv run main.py
```

### Use PIP

- Install requirements (automatically generated by uv):

```bash
    pip install -r requirements.txt
```

- Clone this project and switch to `master` branch.

```bash
    git clone https://github.com/T0nyX1ang/noqx.git
```

- Run locally (based on your system):

```bash
    py -3 main.py
    python3 main.py
```

### Use prebuilt releases (Windows only)

- Download the latest release [here](https://github.com/T0nyX1ang/noqx/releases).

- A new version is released from weekly to monthly.

### Additional Usage

```text
    usage: main.py [-h] [-H HOST] [-p PORT] [-d] [-tl TIME_LIMIT] [-pt PARALLEL_THREADS] [-D]
    usage: main.exe [-h] [-H HOST] [-p PORT] [-d] [-tl TIME_LIMIT] [-pt PARALLEL_THREADS] [-D]

    optional arguments:
      -h, --help            show this help message and exit
      -H HOST, --host HOST  the host to run the server on.
      -p PORT, --port PORT  the port to run the server on.
      -d, --debug           whether to enable debug mode with auto-reloading.
      -tl TIME_LIMIT, --time_limit TIME_LIMIT
                            time limit in seconds. (default = 30)
      -pt PARALLEL_THREADS, --parallel_threads PARALLEL_THREADS
                            parallel threads. (default = 1)
      -D, --enable_deployment
                            Deploy Pyscript for client-side purposes.
```

## How to contribute

### Preparations

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first.

- Clone this project and switch to `dev` branch.

```bash
    git clone https://github.com/T0nyX1ang/noqx.git
    git checkout dev
```

- Install all dependencies with uv:

```bash
    uv sync --all-extras
```

- Install [pre-commit](https://pre-commit.com/) and add commit hooks:

```bash
    uv pre-commit install
```

### Write a new solver

- Create a python file in `solver/` and write solver codes in that file. The functions in `noqx` package are free to use.

- Use the data structures from the puzzle. The atom element of a puzzle is a cell, and the data structures are all crafted around a cell. In detail, a puzzle has the following attributes:

  - `puzzle_name`: the name of the puzzle, should be the same as the filename of the solver.
  - `param`: the parameters of the puzzle.
  - `row`: the number of rows in the puzzle.
  - `col`: the number of columns in the puzzle.
  - `margin`: the margin of the puzzle, the order is a tuple of (`top-margin`, `bottom-margin`, `left-margin`, `right-margin`).
  - `surface`: the shaded cells in the puzzle.
  - `text`: the text clues in the puzzle.
  - `symbol`: the symbols in the puzzle.
  - `edge`: the borders in the puzzle.
  - `line`: the lines in the puzzle.

- Create a class inheriting the base class `noqx.manager.Solver`.

- Implement a `solve` function and write the ASP program needed.

- (Optional) Implement a `refine` function if extra refinement is needed after program solving.

- (Optional) Set static values of the solver, where these values are:

  - `name`: the name of the solver.
  - `category`: the category of the solver, should be `shade` (Shading), `loop` (Loop / Path), `region` (Area Division), `num` (Number), `var` (Variety), `draw` (Drawing), `unk` (Unknown).
  - `examples` (Optional): a list of examples of the solver, each example can be created in two conflicting ways, `data` and `url`:
    - `data`: directly draw the board in noqx and get the data URL by using `Share → Editing URL → Copy`. The URL are suggested to be generated with the following conditions:
      - contains **all** the required `modes` in this puzzle.
      - contains the required `sub-types` in this puzzle.
      - contains necessary initial conditions to pass the coverage tests.
      - set `edit mode` to `solution mode` instead of `problem mode`.
    - `url`: draw the board in [puzz.link](https://puzz.link/list.html) and use `File → Export URL` to get the board URL.
    - `config` (Optional): the configuration of the solver, which will be passed to the solver when it is created, and the keys of `config` are the same as `parameters` keys.
    - `test` (Optional): whether the example is a test case, the default value is `True`, and cannot be used together with `url` way.
    - **Lots of** examples can be found at [pzplus](https://pzplus.tck.mn/db).
  - `parameters` (Optional): the parameters of the solver, which will be passed to the solver when it is created.

- Free to PR now ^\_^

### Test solvers

- Run the tests (with default `unittest` features) with uv:

```bash
    uv run coverage run -m unittest
```

- Check the HTML version of coverage report with uv:

```bash
    uv run coverage html
```

## License

- This project is dual-licensed under [Apache 2.0](./LICENSE.APACHE) and [GPL 3.0](./LICENSE.GPL) (or any later version). You can choose between one of them if you use this project.
