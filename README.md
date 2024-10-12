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
    uv sync --no-dev
```

- Run with uv:

```bash
    uv run noqx.py
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
    py -3 noqx.py
    python3 noqx.py
```

### Additional Usage

```text
    usage: noqx.py [-h] [-d] [-H HOST] [-p PORT] [-tl TIME_LIMIT]

    optional arguments:
      -h, --help            show this help message and exit
      -H HOST, --host HOST  the host to run the server on.
      -p PORT, --port PORT  the port to run the server on.
      -d, --debug           whether to enable debug mode with auto-reloading.
      -tl TIME_LIMIT, --time_limit TIME_LIMIT
                            time limit in seconds (default = 30).
      -pt PARALLEL_THREADS, --parallel_threads PARALLEL_THREADS
                            parallel threads (default = 1).
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
    uv sync
```

- Install [pre-commit](https://pre-commit.com/) and add commit hooks:

```bash
    uv pre-commit install
```

### How to write a new solver

- First, add the related information in `solver/core/const.py`.
  - (Optional) You can add examples in two ways:
    - One way is to draw the board in [puzz.link](https://puzz.link/list.html) and use `File → Export URL` to get the board URL.
    - Another way is to directly draw the board in noqx and get the data URL by using `Share → Editing URL → Copy`.
- Second, create the corresponding python file in `solver/` and write solver code in that file.

- Free to PR now ^\_^

## License

- This project is licensed under the `GPLv3` License.
