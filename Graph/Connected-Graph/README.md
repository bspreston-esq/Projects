# Connected Graph

**Category:** Graph

## Problem

Create a program which takes a graph as an input and outputs whether every node is connected or not.

## Solution

Runs an iterative depth-first traversal from each unvisited node, collecting components; the graph is connected when exactly one component covers every vertex.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py A-B B-C C-A D-C
python3 main.py --demo
```

## Example

```text
connected: connected=True components=[['A', 'B', 'C', 'D']]
two components: connected=False components=[['A', 'B'], ['C', 'D']]
isolated node: connected=False components=[['A', 'B', 'C'], ['D']]
```
