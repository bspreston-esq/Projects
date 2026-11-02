#!/usr/bin/env python3
"""Build an undirected graph from a list of "A-B" links."""
import argparse
from collections import defaultdict

def build_graph(links):
    """Return adjacency dict and edge list from strings like 'A-B' or 'A B'."""
    adjacency = defaultdict(set)
    edges = []
    for raw in links:
        parts = raw.replace("--", "-").replace(" ", "-").split("-")
        parts = [p.strip() for p in parts if p.strip()]
        if len(parts) != 2:
            raise ValueError(f"invalid link '{raw}'; expected A-B")
        a, b = parts
        if a == b:
            raise ValueError(f"self-loop '{raw}' is not allowed")
        adjacency[a].add(b)
        adjacency[b].add(a)
        edges.append((a, b))
        adjacency.setdefault(b, set())
    return dict(adjacency), edges

def to_dot(adjacency, name="G") -> str:
    lines = [f"graph {name} {{"]
    seen = set()
    for node, neighbours in adjacency.items():
        for other in neighbours:
            edge = tuple(sorted((node, other)))
            if edge not in seen:
                seen.add(edge)
                lines.append(f'  "{node}" -- "{other}";')
    lines.append("}")
    return "\n".join(lines)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("links", nargs="*", help="links such as A-B C-D")
    parser.add_argument("--file", help="read one link per line from a file")
    parser.add_argument("--dot", action="store_true", help="print Graphviz DOT")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        adjacency, edges = build_graph(["A-B", "B-C", "C-D", "D-A", "A-C"])
        print(f"vertices ({len(adjacency)}): {', '.join(sorted(adjacency))}")
        print(f"edges ({len(edges)}): {', '.join('-'.join(e) for e in edges)}")
        for node in sorted(adjacency):
            print(f"  {node}: degree {len(adjacency[node])} -> {', '.join(sorted(adjacency[node]))}")
        return

    links = list(args.links)
    if args.file:
        with open(args.file) as fh:
            links += [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    if not links:
        print("Enter links one per line (blank line to finish):")
        while True:
            line = input("> ").strip()
            if not line:
                break
            links.append(line)
    try:
        adjacency, edges = build_graph(links)
    except ValueError as exc:
        print(f"Error: {exc}")
        return
    print(f"{len(adjacency)} vertices, {len(edges)} edges")
    for node in sorted(adjacency):
        print(f"  {node}: {', '.join(sorted(adjacency[node]))}")
    if args.dot:
        print(to_dot(adjacency))

if __name__ == "__main__":
    main()
