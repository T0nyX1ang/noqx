# Noqx

Extended logic puzzle solver of Noq.

## Current development status

- Remove redundant codes.

- New solver API with new visualizations:

  - [x] Minesweeper
  - [x] Hitori
  - [x] Yin-Yang
  - [x] Binairo
  - [x] Kuromasu
  - [x] Nurikabe
  - [x] Kurotto
  - [x] Norinori
  - [x] Heyawake
  - [x] Nurimisaki
  - [x] Aqre
  - [x] Tents
  - [x] Stostone
  - [x] Shimaguni
  - [x] Aquarium
  - [x] Lits
  - [x] Statue Park
  - [x] Chocona

## How to run locally

- Install [PDM](https://pdm-project.org/latest/) first.

- Install dependencies with PDM:

```bash
    pdm install
```

- Run Django with PDM:

```bash
    pdm run manage.py runserver
```

## Noq (Original Project)

Noq is currently accessible on the web at [noq.solutions](https://www.noq.solutions/), formerly at [mstang.xyz/noq](https://www.mstang.xyz/noq). It is powered by Django and runs on a PythonAnywhere web server.

The solver guide can be found [here](./solvers/utils/README.md).
