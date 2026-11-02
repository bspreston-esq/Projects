#!/usr/bin/env python3
"""Decide whether a graph has an Eulerian path/circuit and construct it."""
import argparse
from collections import defaultdict

def build_adjacency(edges):
    adjacency = defaultdict(list)
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    return adjacency

def connected_ignoring_isolated(adjacency):
    nodes = [n for n, nbrs in adjacency.items() if nbrs]
    if not nodes:
        return True
    seen, stack = {nodes[0]}, [nodes[0]]
    while stack:
        node = stack.pop()
        for neighbour in adjacency[node]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return len(seen) == len(nodes)

def eulerian_kind(adjacency):
    """Return 'circuit', 'path' or None (plus odd-degree vertices)."""
    odd = [n for n, nbrs in adjacency.items() if len(nbrs) % 2]
    if not connected_ignoring_isolated(adjacency):
        return None, odd
    if len(odd) == 0:
        return "circuit", odd
    if len(odd) == 2:
        return "path", odd
    return None, odd

def hierholzer(adjacency, start):
    """Return an Eulerian trail using Hierholzer's algorithm (edge-consuming)."""
    graph = {node: list(neighbours) for node, neighbours in adjacency.items()}
    stack, trail = [start], []
    while stack:
        node = stack[-1]
        if graph.get(node):
            neighbour = graph[node].pop()
            graph[neighbour].remove(node)
            stack.append(neighbour)
        else:
            trail.append(stack.pop())
    return trail[::-1]

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("links", nargs="*", help="edges as A-B")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        cases = {
            "square + diagonal": ["A-B", "B-C", "C-D", "D-A", "A-C"],
            "line": ["A-B", "B-C", "C-D"],
            "star": ["A-B", "A-C", "A-D"],
            "disconnected": ["A-B", "C-D"],
        }
        for name, links in cases.items():
            edges = [tuple(link.split("-")) for link in links]
            adjacency = build_adjacency(edges)
            kind, odd = eulerian_kind(adjacency)
            if kind is None:
                print(f"{name}: no Eulerian path (odd-degree vertices: {odd or 'none'})")
            else:
                start = odd[0] if kind == "path" else next(iter(adjacency))
                print(f"{name}: Eulerian {kind} -> {' -> '.join(hierholzer(adjacency, start))}")
        return

    edges = [tuple(link.split("-")) for link in args.links]
    adjacency = build_adjacency(edges)
    kind, odd = eulerian_kind(adjacency)
    if kind is None:
        print("No Eulerian path or cycle exists.")
    else:
        start = odd[0] if kind == "path" else next(iter(adjacency))
        print(f"Eulerian {kind}: {' -> '.join(hierholzer(adjacency, start))}")

if __name__ == "__main__":
    main()
