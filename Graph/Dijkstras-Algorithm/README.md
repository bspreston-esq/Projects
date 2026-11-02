# Dijkstra’s Algorithm

**Category:** Graph

## Problem

Create a program that finds the shortest path through a graph using its edges.

## Solution

Lazy-deletion Dijkstra with a binary heap: distances start at infinity, the closest unvisited node is settled, and its neighbours are relaxed. `previous` pointers reconstruct each shortest path. Negative weights are rejected.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --source A
python3 main.py --demo
```

## Example

```text
A -> A:    0  (A)
A -> B:    3  (A -> C -> B)
A -> C:    2  (A -> C)
A -> D:    8  (A -> C -> B -> D)
A -> E:   10  (A -> C -> B -> D -> E)
A -> F:   13  (A -> C -> B -> D -> E -> F)
```
