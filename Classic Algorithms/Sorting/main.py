#!/usr/bin/env python3
"""Merge sort and bubble sort, implemented from scratch."""
import argparse
import random
import time

def merge_sort(values):
    """Stable top-down merge sort, O(n log n)."""
    if len(values) <= 1:
        return list(values)
    middle = len(values) // 2
    left, right = merge_sort(values[:middle]), merge_sort(values[middle:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def bubble_sort(values):
    """Bubble sort with early exit when a pass makes no swaps, O(n^2) worst case."""
    result = list(values)
    n = len(result)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
        if not swapped:
            break
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("values", nargs="?", help="comma-separated numbers")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        values = [5, 2, 9, 1, 5, 6, -3, 0]
        print("input:      ", values)
        print("merge sort: ", merge_sort(values))
        print("bubble sort:", bubble_sort(values))
        rng = random.Random(7)
        data = [rng.randint(0, 10000) for _ in range(2000)]
        assert merge_sort(data) == sorted(data) == bubble_sort(data)
        start = time.perf_counter(); merge_sort(data); merge_ms = (time.perf_counter() - start) * 1000
        start = time.perf_counter(); bubble_sort(data); bubble_ms = (time.perf_counter() - start) * 1000
        print(f"2000 random ints: merge {merge_ms:.2f} ms, bubble {bubble_ms:.2f} ms")
        return

    raw = args.values or input("Numbers (comma separated): ")
    values = [float(part) if "." in part else int(part) for part in raw.split(",") if part.strip()]
    print("merge: ", merge_sort(values))
    print("bubble:", bubble_sort(values))

if __name__ == "__main__":
    main()
