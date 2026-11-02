# Eulerian Path

**Category:** Graph

## Problem

Create a program which will take as an input a graph and output either a Eulerian path or a Eulerian cycle, or state that it is not possible. A Eulerian Path starts at one node and traverses every edge of a graph through every node and finishes at another node. A Eulerian cycle is a Eulerian Path that starts and finishes at the same node.

## Solution

Applies Euler's degree conditions (zero odd-degree vertices for a circuit, exactly two for a path) plus a connectivity check over non-isolated vertices, then builds the trail with Hierholzer's stack algorithm.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py A-B B-C C-D D-A A-C
python3 main.py --demo
```

## Example

```text
square + diagonal: Eulerian path -> A -> C -> D -> A -> B -> C
line: Eulerian path -> A -> B -> C -> D
star: no Eulerian path (odd-degree vertices: ['A', 'B', 'C', 'D'])
```
