# Graph from links

**Category:** Graph

## Problem

Create a program that will create a graph or network from a series of links.

## Solution

Reads links in `A-B` form (also accepts `A B`) from arguments, a file, or stdin, and builds an undirected adjacency map with de-duplicated neighbours. It reports vertex/edge counts and per-node degrees, and can emit Graphviz DOT for rendering.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py A-B B-C C-D
python3 main.py --file links.txt --dot
python3 main.py --demo
```

## Example

```text
vertices (4): A, B, C, D
edges (5): A-B, B-C, C-D, D-A, A-C
  A: degree 3 -> B, C, D
  B: degree 2 -> A, C
```
