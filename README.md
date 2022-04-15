# Python Data Structures

[![build](https://github.com/adithyabsk/datastructures/actions/workflows/build.yaml/badge.svg?branch=main)](https://github.com/adithyabsk/datastructures/actions/workflows/build.yaml)
[![coverage](./coverage.svg)](https://github.com/adithyabsk/datastructures/actions/workflows/build.yaml)

* [Deque](./datastructures/deque.py):
[Docs](./docs/deque.md)
* [Fixed Hash Map](./datastructures/fixed_hash_map.py):
[Docs](./docs/fixed_hash_map.md)
* [Heap](./datastructures/heap.py):
[Docs](./docs/heap.md)

## Installation Instructions

```shell
pip install .
```

## Developers

* Install [`pre-commit`](https://pre-commit.com/)
* Install [`poetry`](https://python-poetry.org/)

Then, inside the repo run:

```shell
pre-commit install
poetry install
```

Run tests:

```shell
pytest
```

View coverage

```shell
open htmlcov/index.html
```

Export requirements

```shell
poetry export -f requirements.txt --output requirements.txt --dev
```
