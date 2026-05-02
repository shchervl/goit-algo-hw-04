# goit-algo-hw-04

## Setup

Requires Python 3.12+.

With `uv`:

```bash
uv sync
```

Or with plain `python3`:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Tasks

### Task 1 — Sort files by extension

Recursively copies files from a source directory into a destination directory, sorted into subdirectories by file extension.

```bash
uv run task_01/task_01.py <source> [destination]
# or
python3 task_01/task_01.py <source> [destination]
```

- `source` — required, path to the source directory
- `destination` — optional, defaults to `dist`

```bash
# examples
uv run task_01/task_01.py ./my_folder
uv run task_01/task_01.py ./my_folder ./output
```

### Task 2 — Koch snowflake

Draws a Koch snowflake fractal using turtle graphics. Prompts for recursion depth on launch.

```bash
uv run task_02/task_02.py
# or
python3 task_02/task_02.py
```

### Task 3 — Sorting algorithm benchmark

Benchmarks insertion sort, merge sort, and Python's built-in Timsort across multiple array sizes and prints a comparison table with conclusions.

```bash
uv run task_03/task_03.py
# or
python3 task_03/task_03.py
```
