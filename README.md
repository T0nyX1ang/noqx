# Noqx

- Extended logic puzzle solver of [Noq](https://github.com/mstang107/noq) with enhanced efficiency.

- Detailed documents are listed in this [introduction](./docs/index.md).

## Current Maintainers

- [@T0nyX1ang](https://github.com/T0nyX1ang): backend, frontend, refactor, new solver implementations, bug fixes, documents

- [@zhuyaoyu](https://github.com/zhuyaoyu): (huge) solver optimizations, new solver implementations, bug fixes

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

## License

- This project is dual-licensed under [Apache 2.0](./LICENSE.APACHE) and [GPL 3.0](./LICENSE.GPL) (or any later version). You can choose between one of them if you use this project.
