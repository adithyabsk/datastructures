# Python Data Structures

[![build](https://github.com/adithyabsk/datastructures/actions/workflows/build.yaml/badge.svg?branch=main)](https://github.com/adithyabsk/datastructures/actions/workflows/build.yaml)
[![coverage](./coverage.svg)](https://github.com/adithyabsk/datastructures/actions/workflows/build.yaml)

* [`Deque` Source](./datastructures/deque.py)
  * [Docs](./docs/deque.md)
* [`FixedHashMap` Source](./datastructures/fixed_hash_map.py)
  * [Docs](./docs/fixed_hash_map.md)
* [`MinHeap`, `MaxHeap`, `PriorityQueue`, `heapsort` Source](./datastructures/heap.py)
  * [Docs](./docs/heap.md)
* [`SimpleGraph`, `dijkstra_path` Source](./datastructures/graph.py)
  * [Docs](./docs/graph.md)

## Installation Instructions

```shell
pip install .
```

### Graph Visualizations (optional)

```shell
pip install .[graph]
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
