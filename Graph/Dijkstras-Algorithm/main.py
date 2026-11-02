#!/usr/bin/env python3
"""Dijkstra's shortest-path algorithm with a binary heap."""
import argparse
import heapq
from collections import defaultdict

def dijkstra(adjacency, source):
    """Return (distances, previous) shortest-path trees from source."""
    distances = {node: float("inf") for node in adjacency}
    previous = {node: None for node in adjacency}
    if source not in adjacency:
        raise ValueError(f"unknown source '{source}'")
    distances[source] = 0
    queue = [(0, source)]
    visited = set()
    while queue:
        distance, node = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        for neighbour, weight in adjacency[node].items():
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights")
            candidate = distance + weight
            if candidate < distances[neighbour]:
                distances[neighbour] = candidate
                previous[neighbour] = node
                heapq.heappush(queue, (candidate, neighbour))
    return distances, previous

def path_to(previous, target):
    path = []
    while target is not None:
        path.append(target)
        target = previous[target]
    return path[::-1]

def build(edges):
    adjacency = defaultdict(dict)
    for a, b, weight in edges:
        adjacency[a][b] = min(adjacency[a].get(b, float("inf")), weight)
        adjacency[b][a] = min(adjacency[b].get(a, float("inf")), weight)
    return adjacency

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="A")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    edges = [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5),
             ("C", "D", 8), ("C", "E", 10), ("D", "E", 2), ("D", "F", 6), ("E", "F", 3)]
    adjacency = build(edges)
    if args.demo:
        distances, previous = dijkstra(adjacency, "A")
        for node in sorted(distances):
            route = " -> ".join(path_to(previous, node))
            print(f"A -> {node}: {distances[node]:>4}  ({route})")
        return

    try:
        distances, previous = dijkstra(adjacency, args.source)
    except ValueError as exc:
        print(f"Error: {exc}")
        return
    for node in sorted(distances):
        print(f"{args.source} -> {node}: {distances[node]} via {' -> '.join(path_to(previous, node))}")

if __name__ == "__main__":
    main()
