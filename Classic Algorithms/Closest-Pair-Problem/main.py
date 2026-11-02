#!/usr/bin/env python3
"""Closest pair of points: brute force and O(n log n) divide and conquer."""
import argparse
import math
import random
import time

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def closest_pair_brute(points):
    """O(n^2) reference implementation."""
    if len(points) < 2:
        raise ValueError("need at least two points")
    best = (None, None, float("inf"))
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = distance(points[i], points[j])
            if d < best[2]:
                best = (points[i], points[j], d)
    return best

def closest_pair(points):
    """O(n log n) divide-and-conquer closest pair."""
    if len(points) < 2:
        raise ValueError("need at least two points")
    pts = sorted(points)
    best = [None, None, float("inf")]

    def consider(a, b):
        d = distance(a, b)
        if d < best[2]:
            best[:] = [a, b, d]

    def rec(px):
        n = len(px)
        if n <= 3:
            for i in range(n):
                for j in range(i + 1, n):
                    consider(px[i], px[j])
            return px
        middle = n // 2
        mid_x = px[middle][0]
        left, right = rec(px[:middle]), rec(px[middle:])
        merged = sorted(left + right, key=lambda p: p[1])
        strip = [p for p in merged if abs(p[0] - mid_x) < best[2]]
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and strip[j][1] - strip[i][1] < best[2]:
                consider(strip[i], strip[j])
                j += 1
        return merged

    rec(pts)
    return tuple(best)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--points", type=int, default=2000, help="random points to generate")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        sample_rng = random.Random(args.seed)
        pts = [(sample_rng.uniform(-100, 100), sample_rng.uniform(-100, 100)) for _ in range(8)]
        a, b, d = closest_pair(pts)
        print(f"{len(pts)} sample points -> {a} and {b}, distance {d:.4f}")
        n = 800
        rng = random.Random(1)
        pts = [(rng.random() * 1000, rng.random() * 1000) for _ in range(n)]
        start = time.perf_counter(); brute = closest_pair_brute(pts); brute_ms = (time.perf_counter()-start)*1000
        start = time.perf_counter(); fast = closest_pair(pts); fast_ms = (time.perf_counter()-start)*1000
        print(f"{n} points: brute {brute[2]:.6f} in {brute_ms:.1f} ms, "
              f"divide-and-conquer {fast[2]:.6f} in {fast_ms:.1f} ms, match={abs(brute[2]-fast[2]) < 1e-9}")
        return

    rng = random.Random(args.seed)
    pts = [(rng.random() * 1000, rng.random() * 1000) for _ in range(args.points)]
    a, b, d = closest_pair(pts)
    print(f"Closest pair: {a} and {b}, distance {d:.6f}")

if __name__ == "__main__":
    main()
