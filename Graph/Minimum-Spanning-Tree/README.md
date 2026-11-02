# Minimum Spanning Tree

**Category:** Graph

## Problem

Create a program which takes a connected, undirected graph with weights and outputs the minimum spanning tree of the graph i.e., a subgraph that is a tree, contains all the vertices, and the sum of its weights is the least possible.

## Solution

Implements both classic algorithms: Kruskal sorts edges and adds them when union-find shows they join different components; Prim grows a tree from one vertex using a heap. Both results are cross-checked, and disconnection is reported as an error.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --demo
```

## Example

```text
Kruskal: B-C(1), A-C(2), D-E(2), E-F(3), B-D(5) = 13
Prim:    A-C(2), C-B(1), B-D(5), D-E(2), E-F(3) = 13
Algorithms agree: True
```
