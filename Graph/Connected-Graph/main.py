#!/usr/bin/env python3
"""Check whether an undirected graph is connected and list its components."""
import argparse
from collections import defaultdict

def components(adjacency):
    """Return a list of connected components, each a sorted list of nodes."""
    seen, groups = set(), []
    for start in sorted(adjacency):
        if start in seen:
            continue
        stack, group = [start], []
        seen.add(start)
        while stack:
            node = stack.pop()
            group.append(node)
            for neighbour in adjacency[node]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        groups.append(sorted(group))
    return groups

def is_connected(adjacency) -> bool:
    return bool(adjacency) and len(components(adjacency)) <= 1

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("links", nargs="*", help="edges as A-B")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        cases = {"connected": ["A-B", "B-C", "C-A", "D-C"],
                 "two components": ["A-B", "C-D"],
                 "isolated node": ["A-B", "A-C"]}
        for name, links in cases.items():
            adjacency = defaultdict(set)
            for link in links:
                a, b = link.split("-")
                adjacency[a].add(b); adjacency[b].add(a); adjacency.setdefault(b, set())
            if name == "isolated node":
                adjacency["D"] = set()
            groups = components(adjacency)
            print(f"{name}: connected={is_connected(adjacency)} components={groups}")
        return

    adjacency = defaultdict(set)
    for link in args.links:
        a, b = link.split("-")
        adjacency[a].add(b); adjacency[b].add(a); adjacency.setdefault(b, set())
    print("connected" if is_connected(adjacency) else "not connected")
    for index, group in enumerate(components(adjacency), 1):
        print(f"  component {index}: {', '.join(group)}")

if __name__ == "__main__":
    main()
