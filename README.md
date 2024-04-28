# Noqx

Extended logic puzzle solver of [Noq](https://github.com/mstang107/noq).

## Current development status

- Remove redundant codes and formatting codes.

- New solver backend with new UI design (See issue [#2](https://github.com/T0nyX1ang/noqx/issues/2))

- Change the backend from Django to FastAPI (See issue [#31](https://github.com/T0nyX1ang/noqx/issues/31)).

## How to run locally

### Use PDM with a virtual environment (Recommended)

- Install [PDM](https://pdm-project.org/latest/) first.

- Install dependencies with PDM:

```bash
    pdm install
```

- Run with PDM:

```bash
    pdm run noqx.py
```

### Use PIP

- Install requirements (automatically generated by PDM):

```bash
    pip install -r requirements.txt
```

- Run locally (based on your system):

```bash
    py -3 noqx.py
    python3 noqx.py
```

### Additional Usage

```text
    usage: noqx.py [-h] [-H HOST] [-p PORT] [-r] [-l LOG_LEVEL]

    optional arguments:
      -h, --help            show this help message and exit
      -H HOST, --host HOST  The host to run the server on.
      -p PORT, --port PORT  The port to run the server on.
      -r, --reload          Whether to reload the server on changes.
      -l LOG_LEVEL, --log-level LOG_LEVEL
                            The log level of the server.
```

## How to contribute

- Install [PDM](https://pdm-project.org/latest/) first.

- Clone this project and switch to `dev` branch.

```bash
    git clone https://github.com/T0nyX1ang/noqx.git
```

- Install dependencies with PDM:

```bash
    pdm install -d
```

- Install [pre-commit](https://pre-commit.com/) and add commit hooks:

```bash
    pre-commit install
```

- Free to PR now ^\_^
